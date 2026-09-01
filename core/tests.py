import json
from io import StringIO
from unittest.mock import patch
from urllib.error import HTTPError

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from core.models import Memory, Message, ToolAuditLog
from core.services.orchestrator import JarvisOrchestrator
from core.services.llm import LLMService
from core.services.audit import sanitize


class HomePageTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class JarvisOrchestratorTests(TestCase):
    def test_response_persists_conversation_messages(self):
        result = JarvisOrchestrator(llm=LLMService(api_key='')).respond('Hello JARVIS')

        self.assertEqual(result['answer'], 'JARVIS received: Hello JARVIS')
        self.assertEqual(Message.objects.count(), 2)

    def test_safe_tool_returns_result_and_audit_log(self):
        result = JarvisOrchestrator().respond(
            'What time is it?',
            tool_name='get_current_time',
        )

        self.assertEqual(result['tool_result']['timezone'], 'local')
        self.assertTrue(ToolAuditLog.objects.get().success)

    def test_tool_execution_emits_structured_sanitized_log(self):
        with self.assertLogs('jarvis.audit', level='INFO') as captured:
            JarvisOrchestrator(llm=LLMService(api_key='')).respond(
                'What time is it?',
                tool_name='get_current_time',
            )

        self.assertIn('"event": "tool_executed"', captured.output[0])


class AuditLoggingTests(TestCase):
    def test_sensitive_fields_are_redacted(self):
        sanitized = sanitize({'token': 'secret-value', 'nested': {'password': 'hidden'}})

        self.assertEqual(sanitized['token'], '[REDACTED]')
        self.assertEqual(sanitized['nested']['password'], '[REDACTED]')

    def test_tool_rejects_unknown_parameters(self):
        with self.assertRaisesMessage(ValueError, 'Unknown tool parameter(s): unsafe'):
            JarvisOrchestrator().respond(
                'What time is it?',
                tool_name='get_current_time',
                tool_parameters={'unsafe': True},
            )

    def test_orchestrator_uses_offline_fallback_without_api_key(self):
        result = JarvisOrchestrator(llm=LLMService(api_key='')).respond('Offline test')

        self.assertEqual(result['answer'], 'JARVIS received: Offline test')

    def test_orchestrator_executes_tool_selected_by_llm(self):
        class SelectingLLM:
            def decide(self, messages, tools):
                return {
                    'content': None,
                    'tool_call': {
                        'name': 'get_current_time',
                        'arguments': {},
                    },
                }

        result = JarvisOrchestrator(llm=SelectingLLM()).respond('Tell me the time')

        self.assertIsNotNone(result['tool_result'])
        self.assertTrue(ToolAuditLog.objects.get().success)


class LLMServiceTests(TestCase):
    def test_unconfigured_service_does_not_make_network_request(self):
        service = LLMService(api_key='')

        self.assertFalse(service.configured)
        self.assertIsNone(service.respond([{'role': 'user', 'content': 'Hello'}]))

    def test_rate_limit_becomes_controlled_runtime_error(self):
        def rate_limited(*args, **kwargs):
            raise HTTPError('https://api.openai.com/v1/chat/completions', 429, 'Too Many Requests', {}, None)

        service = LLMService(api_key='test-key', urlopen=rate_limited)

        with self.assertRaisesMessage(RuntimeError, 'LLM rate limit or quota reached'):
            service.decide([], [])


class ChatApiTests(TestCase):
    def test_chat_endpoint_accepts_json_message(self):
        response = self.client.post(
            reverse('chat'),
            data=json.dumps({'message': 'Test message'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['answer'], 'JARVIS received: Test message')

    def test_chat_endpoint_accepts_structured_tool_call(self):
        response = self.client.post(
            reverse('chat'),
            data=json.dumps({
                'message': 'What time is it?',
                'tool_call': {'name': 'get_current_time', 'arguments': {}},
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['tool_result'])


class MemoryTests(TestCase):
    def test_memory_can_be_saved_searched_and_deleted(self):
        create_response = self.client.post(
            reverse('memories'),
            data=json.dumps({
                'content': 'User prefers concise answers',
                'category': 'preference',
                'importance': 8,
            }),
            content_type='application/json',
        )
        memory_id = create_response.json()['id']

        self.assertEqual(create_response.status_code, 201)
        search_response = self.client.get(reverse('memories') + '?q=concise')
        self.assertEqual(len(search_response.json()['memories']), 1)

        delete_response = self.client.delete(reverse('forget-memory', args=[memory_id]))
        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(Memory.objects.filter(id=memory_id).exists())


class TerminalCommandTests(TestCase):
    def test_terminal_command_runs_offline_session_until_exit(self):
        output = StringIO()
        with patch('builtins.input', side_effect=['Hello from terminal', ':quit']):
            with patch('core.services.orchestrator.LLMService') as llm_class:
                llm_class.return_value = LLMService(api_key='')
                call_command('jarvis_chat', stdout=output)

        self.assertIn('JARVIS: JARVIS received: Hello from terminal', output.getvalue())
        self.assertEqual(Message.objects.count(), 2)

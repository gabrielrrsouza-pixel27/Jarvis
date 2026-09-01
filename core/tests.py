import json

from django.test import TestCase
from django.urls import reverse

from core.models import Memory, Message, ToolAuditLog
from core.services.orchestrator import JarvisOrchestrator


class HomePageTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class JarvisOrchestratorTests(TestCase):
    def test_response_persists_conversation_messages(self):
        result = JarvisOrchestrator().respond('Hello JARVIS')

        self.assertEqual(result['answer'], 'JARVIS received: Hello JARVIS')
        self.assertEqual(Message.objects.count(), 2)

    def test_safe_tool_returns_result_and_audit_log(self):
        result = JarvisOrchestrator().respond(
            'What time is it?',
            tool_name='get_current_time',
        )

        self.assertEqual(result['tool_result']['timezone'], 'local')
        self.assertTrue(ToolAuditLog.objects.get().success)


class ChatApiTests(TestCase):
    def test_chat_endpoint_accepts_json_message(self):
        response = self.client.post(
            reverse('chat'),
            data=json.dumps({'message': 'Test message'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['answer'], 'JARVIS received: Test message')


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

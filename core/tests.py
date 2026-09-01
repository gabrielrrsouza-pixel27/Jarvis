import json

from django.test import TestCase
from django.urls import reverse

from core.models import Message, ToolAuditLog
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

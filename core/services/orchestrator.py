from typing import Any

from core.models import Conversation, Message
from core.services.llm import LLMService
from core.services.tools import build_registry, execute_tool


class JarvisOrchestrator:
    def __init__(self, llm: LLMService | None = None) -> None:
        self.registry = build_registry()
        self.llm = llm or LLMService()

    def respond(
        self,
        text: str,
        conversation: Conversation | None = None,
        tool_name: str | None = None,
        tool_parameters: dict[str, Any] | None = None,
        confirmed: bool = False,
    ) -> dict[str, Any]:
        text = text.strip()
        if not text:
            raise ValueError('Message cannot be empty.')
        conversation = conversation or Conversation.objects.create()
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.USER,
            content=text,
        )

        tool_result = None
        if tool_name:
            tool_result = execute_tool(
                self.registry,
                tool_name,
                tool_parameters,
                confirmed,
            )
            answer = f'Tool {tool_name} completed successfully.'
        else:
            history = [
                {'role': message.role, 'content': message.content}
                for message in conversation.messages.order_by('created_at')
            ]
            answer = self.llm.respond([
                {
                    'role': 'system',
                    'content': 'You are JARVIS, a concise and safe personal assistant.',
                },
                *history,
            ]) or f'JARVIS received: {text}'

        Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content=answer,
        )
        return {
            'conversation_id': conversation.id,
            'answer': answer,
            'tool_result': tool_result,
        }

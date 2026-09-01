from typing import Any

from core.models import Conversation, Message
from core.services.audit import log_event
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
            messages = [
                {
                    'role': 'system',
                    'content': 'You are JARVIS, a concise and safe personal assistant.',
                },
                *history,
            ]
            decision = self.llm.decide(messages, self.registry.definitions())
            automatic_call = decision.get('tool_call')
            if automatic_call:
                tool_result = execute_tool(
                    self.registry,
                    automatic_call.get('name'),
                    automatic_call.get('arguments'),
                    confirmed,
                )
                answer = f"Tool {automatic_call['name']} completed successfully."
            else:
                answer = decision.get('content') or f'JARVIS received: {text}'

        Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content=answer,
        )
        log_event(
            'interaction_completed',
            conversation_id=conversation.id,
            tool=tool_name,
            success=True,
        )
        return {
            'conversation_id': conversation.id,
            'answer': answer,
            'tool_result': tool_result,
        }

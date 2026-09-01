import json
import os
from urllib import error, request


class LLMService:
    def __init__(self, api_key: str | None = None, urlopen=request.urlopen) -> None:
        self.api_key = api_key if api_key is not None else os.getenv('OPENAI_API_KEY', '')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.urlopen = urlopen

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def respond(self, messages: list[dict[str, str]]) -> str | None:
        if not self.configured:
            return None
        payload = json.dumps({
            'model': self.model,
            'messages': messages,
        }).encode('utf-8')
        http_request = request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=payload,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            },
            method='POST',
        )
        body = self._send(http_request)
        try:
            content = body['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError('LLM returned an invalid response.') from exc
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError('LLM returned an empty response.')
        return content.strip()

    def decide(
        self,
        messages: list[dict[str, str]],
        tools: list[dict],
    ) -> dict:
        if not self.configured:
            return {'content': None, 'tool_call': None}
        payload = json.dumps({
            'model': self.model,
            'messages': messages,
            'tools': [
                {
                    'type': 'function',
                    'function': {
                        'name': tool['name'],
                        'description': tool['description'],
                        'parameters': {
                            'type': 'object',
                            'properties': tool['parameters'],
                            'required': tool.get('required', []),
                        },
                    },
                }
                for tool in tools
            ],
            'tool_choice': 'auto',
        }).encode('utf-8')
        http_request = request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=payload,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            },
            method='POST',
        )
        body = self._send(http_request)
        try:
            message = body['choices'][0]['message']
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError('LLM returned an invalid decision.') from exc
        calls = message.get('tool_calls') or []
        tool_call = None
        if calls:
            function = calls[0].get('function', {})
            try:
                arguments = json.loads(function.get('arguments', '{}'))
            except json.JSONDecodeError as exc:
                raise RuntimeError('LLM returned invalid tool arguments.') from exc
            tool_call = {
                'name': function.get('name'),
                'arguments': arguments,
            }
        return {
            'content': message.get('content'),
            'tool_call': tool_call,
        }

    def _send(self, http_request: request.Request) -> dict:
        try:
            with self.urlopen(http_request, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            if exc.code == 429:
                raise RuntimeError(
                    'LLM rate limit or quota reached. Check your OpenAI billing and limits.'
                ) from exc
            raise RuntimeError(f'LLM request failed with HTTP {exc.code}.') from exc
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError('LLM request failed. Check your network and provider configuration.') from exc
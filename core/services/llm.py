import json
import os
from urllib import request


class LLMService:
    def __init__(self, api_key: str | None = None, urlopen=request.urlopen) -> None:
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', '')
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
        with self.urlopen(http_request, timeout=30) as response:
            body = json.loads(response.read().decode('utf-8'))
        try:
            content = body['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError('LLM returned an invalid response.') from exc
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError('LLM returned an empty response.')
        return content.strip()
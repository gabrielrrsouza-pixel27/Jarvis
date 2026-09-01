import json
import logging
from typing import Any


logger = logging.getLogger('jarvis.audit')
SENSITIVE_KEYS = {
    'api_key',
    'authorization',
    'password',
    'secret',
    'token',
}


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: '[REDACTED]' if key.lower() in SENSITIVE_KEYS else sanitize(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    return value


def log_event(event: str, **fields: Any) -> None:
    payload = {'event': event, **sanitize(fields)}
    logger.info(json.dumps(payload, sort_keys=True, default=str))

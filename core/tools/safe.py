from datetime import datetime
from typing import Any

from core.services.memory import MemoryService


def get_current_time(**_: Any) -> dict[str, Any]:
    return {
        'iso': datetime.now().astimezone().isoformat(),
        'timezone': 'local',
    }


def get_system_stats(**_: Any) -> dict[str, Any]:
    # Keep the first tool implementation dependency-free and portable.
    return {'status': 'available', 'platform': 'local'}


def save_memory(
    content: str,
    category: str = 'fact',
    importance: int = 5,
    **_: Any,
) -> dict[str, Any]:
    memory = MemoryService().save(content, category, importance)
    return {
        'id': memory.id,
        'content': memory.content,
        'category': memory.category,
        'importance': memory.importance,
    }

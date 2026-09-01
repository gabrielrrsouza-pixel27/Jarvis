from datetime import datetime
from typing import Any


def get_current_time(**_: Any) -> dict[str, Any]:
    return {
        'iso': datetime.now().astimezone().isoformat(),
        'timezone': 'local',
    }


def get_system_stats(**_: Any) -> dict[str, Any]:
    # Keep the first tool implementation dependency-free and portable.
    return {'status': 'available', 'platform': 'local'}

import time
from typing import Any

from core.models import ToolAuditLog
from core.tools.base import Tool, ToolRegistry
from core.tools.safe import get_current_time, get_system_stats


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(Tool(
        name='get_current_time',
        description='Return the current local time.',
        risk_level='low',
        requires_confirmation=False,
        handler=get_current_time,
        parameters={},
    ))
    registry.register(Tool(
        name='get_system_stats',
        description='Return basic local system availability.',
        risk_level='low',
        requires_confirmation=False,
        handler=get_system_stats,
        parameters={},
    ))
    return registry


def execute_tool(
    registry: ToolRegistry,
    name: str,
    parameters: dict[str, Any] | None = None,
    confirmed: bool = False,
) -> dict[str, Any]:
    tool = registry.get(name)
    parameters = parameters or {}
    if not isinstance(parameters, dict):
        raise ValueError('Tool parameters must be an object.')
    unknown_parameters = set(parameters) - set(tool.parameters)
    if unknown_parameters:
        names = ', '.join(sorted(unknown_parameters))
        raise ValueError(f'Unknown tool parameter(s): {names}')
    if tool.requires_confirmation and not confirmed:
        raise PermissionError(f'Confirmation required for tool: {name}')

    started = time.perf_counter()
    success = False
    result: dict[str, Any] = {'status': 'failed'}
    try:
        result = tool.handler(**parameters)
        success = True
        return result
    finally:
        ToolAuditLog.objects.create(
            tool_name=tool.name,
            parameters=parameters,
            result=result if success else {'status': 'failed'},
            risk_level=tool.risk_level,
            confirmed_by_user=confirmed,
            success=success,
            duration_ms=int((time.perf_counter() - started) * 1000),
        )

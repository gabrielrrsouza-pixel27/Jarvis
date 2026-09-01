import time
from typing import Any

from core.models import ToolAuditLog
from core.services.audit import log_event
from core.tools.base import Tool, ToolRegistry
from core.tools.safe import get_current_time, get_system_stats, save_memory


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
    registry.register(Tool(
        name='save_memory',
        description='Save a useful user fact or preference for future conversations.',
        risk_level='medium',
        requires_confirmation=False,
        handler=save_memory,
        parameters={
            'content': {'type': 'string'},
            'category': {'type': 'string'},
            'importance': {'type': 'integer', 'minimum': 1, 'maximum': 10},
            'required': ['content'],
        },
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
    allowed_parameters = set(tool.parameters) - {'required'}
    unknown_parameters = set(parameters) - allowed_parameters
    if unknown_parameters:
        names = ', '.join(sorted(unknown_parameters))
        raise ValueError(f'Unknown tool parameter(s): {names}')
    schema = tool.parameters
    for parameter_name in schema.get('required', []):
        if parameter_name not in parameters:
            raise ValueError(f'Missing required tool parameter: {parameter_name}')
    for parameter_name, value in parameters.items():
        expected_type = schema.get(parameter_name, {}).get('type')
        if expected_type == 'string' and not isinstance(value, str):
            raise ValueError(f'Tool parameter must be a string: {parameter_name}')
        if expected_type == 'integer' and (not isinstance(value, int) or isinstance(value, bool)):
            raise ValueError(f'Tool parameter must be an integer: {parameter_name}')
        constraints = schema.get(parameter_name, {})
        if 'minimum' in constraints and value < constraints['minimum']:
            raise ValueError(f'Tool parameter is below minimum: {parameter_name}')
        if 'maximum' in constraints and value > constraints['maximum']:
            raise ValueError(f'Tool parameter is above maximum: {parameter_name}')
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
        duration_ms = int((time.perf_counter() - started) * 1000)
        ToolAuditLog.objects.create(
            tool_name=tool.name,
            parameters=parameters,
            result=result if success else {'status': 'failed'},
            risk_level=tool.risk_level,
            confirmed_by_user=confirmed,
            success=success,
            duration_ms=duration_ms,
        )
        log_event(
            'tool_executed',
            tool=tool.name,
            parameters=parameters,
            risk_level=tool.risk_level,
            confirmed_by_user=confirmed,
            success=success,
            duration_ms=duration_ms,
        )

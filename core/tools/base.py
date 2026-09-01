from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    risk_level: str
    requires_confirmation: bool
    handler: Callable[..., dict[str, Any]]
    parameters: dict[str, dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f'Tool already registered: {tool.name}')
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ValueError(f'Unknown tool: {name}') from exc

    def names(self) -> list[str]:
        return sorted(self._tools)

    def definitions(self) -> list[dict[str, Any]]:
        return [
            {
                'name': tool.name,
                'description': tool.description,
                'parameters': {
                    key: value
                    for key, value in tool.parameters.items()
                    if key != 'required'
                },
                'required': tool.parameters.get('required', []),
            }
            for tool in self._tools.values()
        ]

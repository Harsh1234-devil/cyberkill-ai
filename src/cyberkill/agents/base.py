"""Base Agent Class."""

import abc
from typing import Any, Dict
from cyberkill.core.scope_guard import default_scope_guard

class BaseAgent(abc.ABC):
    def __init__(self, name: str, killchain_stage: str, description: str):
        self.name = name
        self.killchain_stage = killchain_stage
        self.description = description

    @abc.abstractmethod
    async def run(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        pass

    def validate_scope(self, target: str) -> bool:
        allowed, reason = default_scope_guard.validate_target(target)
        if not allowed:
            raise PermissionError(f"Target '{target}' violates scope: {reason}")
        return True

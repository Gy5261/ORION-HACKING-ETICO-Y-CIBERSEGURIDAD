"""API pública del sistema de plugins ORION."""

from .core import (
    AuthorizationError,
    BasePlugin,
    ExecutionPolicy,
    InputValidationError,
    OrionPluginError,
    OrionRuntime,
    PluginContext,
    PluginExecutionError,
    PluginMetadata,
    PluginNotFoundError,
    PluginRegistry,
    PluginResult,
    validate_json_schema,
)

__all__ = [
    "AuthorizationError",
    "BasePlugin",
    "ExecutionPolicy",
    "InputValidationError",
    "OrionPluginError",
    "OrionRuntime",
    "PluginContext",
    "PluginExecutionError",
    "PluginMetadata",
    "PluginNotFoundError",
    "PluginRegistry",
    "PluginResult",
    "validate_json_schema",
]

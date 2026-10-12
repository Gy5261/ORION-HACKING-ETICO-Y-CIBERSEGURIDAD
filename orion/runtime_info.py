"""Observed interpreter capabilities for ORION, without performance claims.

Python 3.15 adds explicit lazy imports, immutable builtins and improved
runtime instrumentation. Availability depends on the actual interpreter build.
No network access and no external processes are required.
"""
from __future__ import annotations

import builtins
import platform
import sys
import sysconfig
from typing import Any

from orion import __version__


def _optional_call(obj: object, name: str) -> Any | None:
    method = getattr(obj, name, None)
    if not callable(method):
        return None
    try:
        return method()
    except (RuntimeError, OSError, ValueError):
        return None


def interpreter_report() -> dict[str, Any]:
    """Report observed capabilities; absence is null, not a guessed value."""
    jit = getattr(sys, "_jit", None)
    abi = getattr(sys, "abi_info", None)
    gil = _optional_call(sys, "_is_gil_enabled")
    free_threaded_build = sysconfig.get_config_var("Py_GIL_DISABLED")
    return {
        "orion_version": __version__,
        "implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_315_or_newer": sys.version_info >= (3, 15),
        "filesystem_encoding": sys.getfilesystemencoding(),
        "gil_enabled": gil,
        "free_threaded_build": bool(free_threaded_build) if free_threaded_build is not None else None,
        "jit": {
            "available": _optional_call(jit, "is_available"),
            "enabled": _optional_call(jit, "is_enabled"),
        },
        "lazy_import_mode": _optional_call(sys, "get_lazy_imports"),
        "has_frozendict": hasattr(builtins, "frozendict"),
        "has_sentinel": hasattr(builtins, "sentinel"),
        "abi_pointer_bits": getattr(abi, "pointer_bits", None),
        "no_network_contacted": True,
        "benchmark_performed": False,
    }

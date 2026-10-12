"""Deterministic ORION microbenchmarks; run separately under each Python interpreter.

Numbers are local timings, not universal speedups or security scores.
No third-party tools, targets, network requests, subprocesses or fixtures.
"""
from __future__ import annotations

import argparse
import json
import statistics
import time
from collections.abc import Callable
from typing import Any

from orion.controls import canonical_json, request_fingerprint
from orion.plugins.core import PluginRegistry, validate_json_schema
from orion.runtime_info import interpreter_report


def _measure(work: Callable[[], Any], iterations: int, samples: int) -> dict[str, float | int]:
    for _ in range(min(iterations, 100)):
        work()
    elapsed: list[float] = []
    for _ in range(samples):
        started = time.perf_counter_ns()
        for _ in range(iterations):
            work()
        elapsed.append((time.perf_counter_ns() - started) / iterations)
    median = statistics.median(elapsed)
    deviation = statistics.median(abs(value - median) for value in elapsed)
    return {
        "iterations_per_sample": iterations,
        "samples": samples,
        "median_ns_per_operation": round(median, 1),
        "median_absolute_deviation_ns": round(deviation, 1),
        "operations_per_second": round(1_000_000_000 / median, 1) if median > 0 else 0,
    }


def benchmark(iterations: int = 500, samples: int = 5) -> dict[str, Any]:
    if not 1 <= iterations <= 100_000 or not 1 <= samples <= 25:
        raise ValueError("iterations must be 1..100000 and samples 1..25")
    registry = PluginRegistry(load_external=False)
    plugin = registry.get("ioc_enricher")
    payload = {"iocs": ["127.0.0.1", "d41d8cd98f00b204e9800998ecf8427e"], "external_sources": False}
    return {
        "runtime": interpreter_report(),
        "scope": "In-process microbenchmarks without network; comparisons require identical hardware",
        "benchmarks": {
            "canonical_json": _measure(lambda: canonical_json(payload), iterations, samples),
            "input_schema": _measure(lambda: validate_json_schema(payload, plugin.metadata.input_schema),
                                      iterations, samples),
            "request_fingerprint": _measure(lambda: request_fingerprint("ioc_enricher", payload),
                                             iterations, samples),
            "registry_manifest": _measure(registry.manifest, iterations, samples),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark ORION on the running Python version")
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--samples", type=int, default=5)
    args = parser.parse_args()
    try:
        result = benchmark(args.iterations, args.samples)
    except ValueError as exc:
        parser.error(str(exc))
    result["runtime"]["benchmark_performed"] = True
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# OSINT integrations

ORION 2.0 exposes six established OSINT projects through constrained adapters. The projects remain separate installations and retain their original licenses.

| Plugin | Integration | Environment override | Side effects |
|---|---|---|---|
| `spiderfoot` | SpiderFoot HTTP API | Not required | Starting a scan requires `allow_side_effects` |
| `theharvester` | `theHarvester` executable | `ORION_THEHARVESTER_EXECUTABLE` | None |
| `sherlock` | `sherlock` executable | `ORION_SHERLOCK_EXECUTABLE` | None |
| `osint_spy` | `osint-spy.py` executable | `ORION_OSINT_SPY_EXECUTABLE` | None |
| `phoneinfoga` | `phoneinfoga` executable | `ORION_PHONEINFOGA_EXECUTABLE` | None |
| `photon` | `photon.py` or `photon` executable | `ORION_PHOTON_EXECUTABLE` | None |

## Safety model

Adapters accept structured JSON only. They do not expose arbitrary command arguments, proxies, custom headers, clone modes, secret extraction, update commands, malware functions, or shell execution. Every network plugin requires both an authorization reference and `--allow-network`.

Missing executables are reported by:

```bash
orion plugins doctor
orion plugins list --json --health
```

The default doctor remains healthy when optional tools are absent. Use `orion plugins doctor --strict` on workstations that must have every integration installed.

## Examples

```bash
orion plugins run sherlock \
  --input samples/plugins/sherlock.json \
  --authorization TOR-2026-ORION-001 \
  --allow-network
```

```bash
orion plugins run spiderfoot \
  --input samples/plugins/spiderfoot-start.json \
  --authorization TOR-2026-ORION-001 \
  --allow-network \
  --allow-side-effects
```

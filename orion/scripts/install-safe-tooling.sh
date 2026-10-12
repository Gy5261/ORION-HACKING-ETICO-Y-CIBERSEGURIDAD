#!/usr/bin/env bash
# Controlled operator bootstrap: no downloads or changes unless --apply.
set -euo pipefail

usage() {
  printf '%s\n' 'Usage: install-safe-tooling.sh [--plan|--apply] [--category core|network|all]'
}

mode=plan
category=core
while (($#)); do
  case "$1" in
    --plan) mode=plan ;;
    --apply) mode=apply ;;
    --category)
      shift
      if (($# == 0)); then usage >&2; exit 2; fi
      category=$1 ;;
    --help|-h) usage; exit 0 ;;
    *) printf 'Unsupported option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

case "$category" in
  core) packages=(git curl jq python3 python3-pip) ;;
  network) packages=(nmap wireshark) ;;
  all) packages=(git curl jq python3 python3-pip nmap wireshark) ;;
  *) printf 'Unsupported category: %s\n' "$category" >&2; exit 2 ;;
esac

printf 'ORION bootstrap mode=%s category=%s packages=%s\n' "$mode" "$category" "${packages[*]}"
if [[ "$mode" != apply ]]; then
  printf '%s\n' 'PLAN ONLY: no internet access or package changes have occurred.'
  exit 0
fi
if ((EUID != 0)); then
  printf '%s\n' 'Installation requires explicit administrative execution (run with sudo).' >&2
  exit 2
fi

# Never pipe remote scripts into a shell. Install from the OS package manager.
if command -v apt-get >/dev/null 2>&1; then
  DEBIAN_FRONTEND=noninteractive apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends "${packages[@]}"
elif command -v dnf >/dev/null 2>&1; then
  dnf install --assumeyes "${packages[@]}"
else
  printf '%s\n' 'Unsupported package manager. Install these packages manually from trusted repositories.' >&2
  exit 2
fi
printf '%s\n' 'Package manager returned success; verify installed versions separately.'

#!/usr/bin/env bash
set -euo pipefail

echo "ORION-HACKING safe tooling bootstrap"
echo "Instala solo tooling defensivo y de evaluacion segura."

TOOLS=(
  curl
  jq
  python3
  pipx
  nmap
  wireshark
  tshark
)

printf '%s\n' "${TOOLS[@]}"
echo "Revisa cada paquete antes de instalarlo."

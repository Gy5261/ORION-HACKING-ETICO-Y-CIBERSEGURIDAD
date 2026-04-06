# Wireless & Remote Access - Securing Distributed Work

## Concepto Fundamental

**Problem**: 60% of breaches involve remote access. Why? Wi-Fi is broadcast, VPN often password-only, remote devices on untrusted networks.

**Core Controls**: WPA2-Enterprise/WPA3, MFA on VPN, device posture checking, network segmentation, behavioral monitoring.

**Key Stats**: 207-day avg breach discovery time. Remote access breaches found faster (120 days) but damage already extensive.

## Wireless Security

### Assessment Areas
- **Protocol**: WPA2-Enterprise (not PSK=shared password). WPA3 if available.
- **Guest network**: Isolated from corporate (VLAN separation)
- **AP firmware**: Current (monthly updates critical)
- **Rogue detection**: Monitor for "FreeWiFi", "Corporate", impersonation SSIDs
- **Encryption**: AES-256 minimum (TKIPis weak)
- **Disable WPS**: PIN brute-forcing possible
- **No open SSIDs**: Reduces casual attack attraction

### Wi-Fi Assessment Checklist
1. **Protocol Check**
   - [ ] WPA2-Enterprise or WPA3 active
   - [ ] No legacy SSID with WPA-PSK hanging around
   - [ ] TLS 1.2+ for EAP auth
   - [ ] RADIUS server secured (not plaintext)

2. **Guest Network**
   - [ ] Separate VLAN from corporate
   - [ ] No access to internal systems
   - [ ] Bandwidth limited
   - [ ] Captive portal for onboarding

3. **Access Point Management**
   - [ ] All APs on current firmware
   - [ ] Default credentials changed
   - [ ] Admin access only from management network
   - [ ] Encrypted management interface (not HTTP)

4. **Monitoring**
   - [ ] Rogue AP detection enabled
   - [ ] Unusual association attempts logged
   - [ ] Channel monitoring (detect overlapping networks)

## Remote Access Security

### VPN Assessment
1. **Authentication** [ ] MFA required (TOTP or hardware key, NOT SMS)
   - [ ] No password-only access
   - [ ] Session MFA refresh (re-auth every 8 hours)
   - [ ] Rogue certificate detection

2. **Protocol & Encryption**
   - [ ] Modern protocol (WireGuard > OpenVPN > IPSec; NO PPTP)
   - [ ] TLS 1.2+ enforced
   - [ ] AES-256 encryption
   - [ ] Perfect forward secrecy enabled

3. **Access Control**
   - [ ] Device posture checking (before VPN connect):
     - Disk encrypted? (BitLocker/FileVault)
     - EDR running and current?
     - Patches within 30 days?
   - [ ] Remote users in isolated VLAN (least privilege)
   - [ ] Least privilege per user (contractor != engineer != admin)
   - [ ] Session timeout (30 mins idle = auto-logout)

4. **Network Protection**
   - [ ] Kill switch (VPN drops → no unencrypted traffic)
   - [ ] Split tunneling disabled (all traffic through VPN)
   - [ ] DNS leak protection (DNS requests go through TUN adapter)
   - [ ] Firewall rules on corporate network (defense in depth)

5. **Logging & Monitoring**
   - [ ] All logins logged with source IP, time, user
   - [ ] Logs centralized (not on VPN gateway)
   - [ ] Alerts configured:
     - Impossible travel (NYC 2 mins ago, now Singapore)
     - Unusual time logins (3am access from user who never works nights)
     - Volume anomalies (downloading 100GB suddenly)
     - Privilege escalation within VPN

### Device Posture Requirements
```
Before VPN grant access, device must prove:
✅ BitLocker/FileVault encryption enabled
✅ EDR agent installed, running, updated (< 7 days AV defs)
✅ OS patches current (< 30 days behind latest)
✅ No jailbreak/rooting (mobile)
✅ Not on corporate blocklist (stolen device)
```

## Methodology - Remote Access Assessment

**Week 1**: Inventory (all VPN systems, wireless networks, remote apps)
**Week 2**: Security review (protocol version, MFA status, logging enabled)
**Week 3**: Testing (credential spray against VPN, posture check bypass, impossible travel detection)
**Week 4**: Remediation (MFA rollout, device posture implementation, monitoring setup)

## Real Example

**Finding**: VPN accepts password-only authentication for admin accounts
**Risk**: Credentials from breached sites work against VPN
**Attack**: 10M passwords tested → 1% success rate → attacker inside network
**Fix**: MFA required, takes 2 weeks to roll out
**Result**: Attack now fails 99.9% of time

## Checklist Summary

```
WIRELESS: WPA2-Ent/WPA3, guest isolated, current firmware, rogue detection
VPN: MFA, modern protocol, TLS 1.2+, AES-256, posture checking, kill switch
MONITORING: Login logs, impossible travel alerts, volume anomalies
REMEDIATION: Implement missing items by risk (MFA first, segmentation next)
```


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Wireless & Remote Access - Securing Distributed Work

### Integraciones ampliadas

- Kismet: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Aircrack-ng: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Cisco ISE: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Aruba Central: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: WPA2-Enterprise debil.
- Integracion recomendada: Kismet.
- Senal principal: SSID huerfano.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: guest con salto lateral.
- Integracion recomendada: Aircrack-ng.
- Senal principal: EAP vencido.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: VPN heredada.
- Integracion recomendada: Cisco ISE.
- Senal principal: split tunneling.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: WPA2-Enterprise debil.
- Integracion recomendada: Aruba Central.
- Senal principal: SSID huerfano.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.


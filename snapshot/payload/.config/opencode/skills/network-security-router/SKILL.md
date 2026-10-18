---
name: network-security-router
description: >
  Route network security, TLS, certificate, packet analysis, and protocol reverse engineering requests to the most relevant downstream skills.
  Trigger: When the user asks about SSL, TLS, HTTPS, certificates, PKI, Wireshark, tcpdump, packet capture, protocol analysis, reverse engineering, or secure network communications.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks about SSL/TLS setup, HTTPS, certificate renewal, mTLS, or PKI
- User mentions cert-manager, Let's Encrypt, OCSP, HSTS, or cipher suites
- User mentions Wireshark, tshark, tcpdump, mitmproxy, or packet capture
- User wants to understand or document a proprietary protocol
- User asks about protocol dissection, network debugging, or traffic analysis

---

## Critical Pattern

This is a **router skill**.

Do not stop here.
Load the most relevant downstream skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| SSL, TLS, HTTPS, certificate lifecycle, PKI, cert-manager | `ssl-tls-management` |
| Packet capture, protocol dissection, proprietary protocol understanding | `protocol-reverse-engineering` |
| Network hardening with broader security context | `cybersecurity-router` + relevant network skill |
| Secure backend comms, mTLS, ingress TLS, service-to-service security | `ssl-tls-management` + `backend-router` |
| Reverse engineering with security/audit intent | `protocol-reverse-engineering` + `cybersecurity-router` |

Load multiple skills when needed. Example:
- Kubernetes ingress TLS problem -> `ssl-tls-management` + `backend-router`
- Unknown binary protocol on internal service -> `protocol-reverse-engineering`
- TLS posture review plus cipher hardening -> `ssl-tls-management` + `cybersecurity-router`

---

## Decision Tree

```text
SSL / TLS / HTTPS / certs mentioned?           -> Load ssl-tls-management
Wireshark / tcpdump / packet capture mentioned? -> Load protocol-reverse-engineering
Protocol reverse engineering mentioned?         -> Load protocol-reverse-engineering
mTLS / ingress / backend comms mentioned?       -> Load ssl-tls-management + backend-router
Broader network security hardening mentioned?   -> Load cybersecurity-router + relevant network skill
Otherwise                                       -> Load ssl-tls-management for secure comms, protocol-reverse-engineering for traffic analysis
```

---

## Anti-Patterns

- Do not route certificate lifecycle work only to generic cybersecurity advice.
- Do not route packet/protocol analysis only to backend skills.
- Do not treat TLS configuration and protocol reverse engineering as the same problem.
- Do not skip `cybersecurity-router` when the user is asking for audit or hardening, not just implementation.

---

## Commands

```bash
skill({ name: "ssl-tls-management" })
skill({ name: "protocol-reverse-engineering" })
skill({ name: "cybersecurity-router" })
skill({ name: "backend-router" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| TLS / HTTPS / certificates | `ssl-tls-management` |
| Packet capture / Wireshark | `protocol-reverse-engineering` |
| Unknown network protocol | `protocol-reverse-engineering` |
| Secure backend transport | `ssl-tls-management` |
| Network security audit | `cybersecurity-router` |

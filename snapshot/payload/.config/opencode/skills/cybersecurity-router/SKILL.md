---
name: cybersecurity-router
description: >
  Route security, hardening, audit, vulnerability, OWASP, and Solidity security requests to the most relevant downstream skills.
  Trigger: When the user asks about security reviews, hardening, auth risks, vulnerability classes, OWASP issues, secure backend design, container security, or smart contract security.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks for a security review, hardening pass, or vulnerability audit
- User mentions OWASP, auth flaws, secure coding, attack surface, or security posture
- User mentions Solidity, smart contracts, DeFi, reentrancy, or contract audits
- User asks about backend or container hardening from a security angle
- User wants architecture boundaries that reduce security risk

---

## Critical Pattern

This is a **router skill**.

Do not stop here.
Load the most relevant downstream skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| Solidity, smart contracts, DeFi, reentrancy, audit checklist | `solidity-security` |
| Django auth, DRF permissions, backend security | `django-expert` + `django-drf` |
| Spring or Java backend hardening | `spring-boot-3` + `java-21` |
| Secure service boundaries in Java systems | `hexagonal-architecture-layers-java` + `spring-boot-3` |
| Container hardening or image security | `docker-expert` + `docker-containerization` |
| Security-oriented code review of a PR | `pr-review` + relevant stack skill |
| Broad backend hardening with no stack yet | `backend-router` |

Load multiple skills when needed. Example:
- OWASP auth review for DRF app -> `django-expert` + `django-drf`
- Smart contract audit -> `solidity-security`
- Secure deployment and container hardening -> `docker-expert` + `docker-containerization` + relevant backend skill

---

## Decision Tree

```text
Solidity or smart contracts mentioned?      -> Load solidity-security
Django / DRF security mentioned?            -> Load django-expert + django-drf
Spring / Java security mentioned?           -> Load spring-boot-3 + java-21
Container hardening mentioned?              -> Load docker-expert + docker-containerization
Security review of backend/service code?    -> Load backend-router + relevant stack skill
PR or audit mindset requested?              -> Load pr-review + relevant stack skill
Otherwise                                   -> Load backend-router first, then stack-specific security skill
```

---

## Anti-Patterns

- Do not pretend `solidity-security` applies to generic web or API security.
- Do not answer security questions only at the framework surface; include auth, data flow, and deployment concerns.
- Do not route OWASP or hardening questions to frontend-only skills.
- Do not perform a generic audit without loading the stack-specific skill when the stack is known.

---

## Commands

```bash
skill({ name: "solidity-security" })
skill({ name: "django-expert" })
skill({ name: "django-drf" })
skill({ name: "spring-boot-3" })
skill({ name: "java-21" })
skill({ name: "hexagonal-architecture-layers-java" })
skill({ name: "docker-expert" })
skill({ name: "docker-containerization" })
skill({ name: "pr-review" })
skill({ name: "backend-router" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| Smart contract audit | `solidity-security` |
| Django auth hardening | `django-expert` |
| DRF permission review | `django-drf` |
| Java backend security | `spring-boot-3` |
| Container hardening | `docker-expert` |
| Security review with unclear stack | `backend-router` |

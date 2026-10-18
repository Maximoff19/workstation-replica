---
name: devops-router
description: >
  Route DevOps, CI/CD, deployment, container, orchestration, and observability requests to the most relevant downstream skills.
  Trigger: When the user asks about Docker, containers, CI/CD, Kubernetes, deployment workflows, release pipelines, observability, infrastructure delivery, or runtime operations.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks about CI/CD, pipelines, or deployment workflow
- User mentions Docker, image builds, multi-stage builds, or container runtime issues
- User mentions Kubernetes, orchestration, rollout, or runtime delivery concerns
- User asks about observability, logs, metrics, monitoring, or production operations
- User asks how to deploy, containerize, or operate an app safely

---

## Critical Pattern

This is a **router skill**.

Do not stop here.
Load the most relevant downstream skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| Dockerfile, image hardening, container setup | `docker-expert` + `docker-containerization` |
| Deployment platform or runtime environment | `platform-router` |
| Secure network transport in delivery/runtime | `network-security-router` |
| Backend delivery pipeline | `backend-router` + relevant delivery skill |
| PR/release workflow around delivery | `github-pr` + `conventional-commit` |
| Broad DevOps question with no platform chosen | `docker-expert` + `platform-router` |

Load multiple skills when needed. Example:
- Ship a Spring service in containers -> `backend-router` + `docker-expert` + `docker-containerization`
- Configure HTTPS on deployed app -> `platform-router` + `network-security-router`
- Delivery review for infra-heavy change -> `github-pr` + `docker-expert` + relevant stack skill

---

## Decision Tree

```text
Docker or container build/runtime mentioned?     -> Load docker-expert + docker-containerization
Hosting/platform/deployment environment?         -> Load platform-router
TLS/cert/runtime transport security?             -> Load network-security-router
Backend service delivery?                        -> Load backend-router + delivery/platform skill
PR/release/deployment workflow?                  -> Load github-pr + conventional-commit
Otherwise                                        -> Load docker-expert + platform-router
```

---

## Anti-Patterns

- Do not answer deployment/runtime questions only with app-code advice.
- Do not route Docker/container work only to backend or frontend skills.
- Do not treat CI/CD, hosting platform, and runtime security as the same concern.
- Do not skip the platform-specific skill when the deployment target is known.

---

## Commands

```bash
skill({ name: "docker-expert" })
skill({ name: "docker-containerization" })
skill({ name: "platform-router" })
skill({ name: "network-security-router" })
skill({ name: "backend-router" })
skill({ name: "github-pr" })
skill({ name: "conventional-commit" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| Containerize app | `docker-expert` |
| Deploy to platform | `platform-router` |
| Runtime HTTPS/TLS | `network-security-router` |
| Backend delivery | `backend-router` |
| Release workflow | `github-pr` |

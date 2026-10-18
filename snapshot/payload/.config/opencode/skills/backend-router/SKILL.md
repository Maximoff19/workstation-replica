---
name: backend-router
description: >
  Route backend, API, auth, database, server, and service-layer requests to the most relevant downstream skills.
  Trigger: When the user asks about backend architecture, APIs, authentication, services, persistence, databases, Java backends, Django/DRF, Elixir services, or server-side boundaries.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks about backend or server architecture
- User mentions API design, REST, serializers, auth, or persistence
- User mentions Django, DRF, Python APIs, or ORM patterns
- User mentions Spring Boot, Java services, or hexagonal architecture
- User mentions Elixir or Phoenix service design
- User asks about boundaries between application, domain, and infrastructure
- User needs backend validation, DTOs, or service-layer patterns

---

## Critical Pattern

This is a **router skill**.

Do not stop here.
Load the most relevant downstream skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| Django models, auth, ORM, backend design | `django-expert` |
| Django REST Framework endpoints, serializers, filters | `django-drf` + `django-expert` |
| Spring Boot services, controllers, configuration | `spring-boot-3` + `java-21` |
| Java layering and clean boundaries | `hexagonal-architecture-layers-java` + `spring-boot-3` |
| Modern Java language patterns | `java-21` |
| Elixir or Phoenix backend review/refactor | `elixir-antipatterns` |
| Validation boundaries or typed contracts | `zod-4` + `typescript` |
| Containerization near backend delivery | `docker-expert` + `docker-containerization` |

Load multiple skills when needed. Example:
- DRF endpoint with auth and filters -> `django-drf` + `django-expert`
- Spring Boot service with clean architecture -> `spring-boot-3` + `hexagonal-architecture-layers-java` + `java-21`
- Backend container hardening -> `docker-expert` + `docker-containerization` + relevant backend stack skill

---

## Decision Tree

```text
Django or DRF mentioned?                   -> Load django-drf and/or django-expert
Spring Boot or Java service mentioned?     -> Load spring-boot-3 + java-21
Hexagonal or clean layering mentioned?     -> Load hexagonal-architecture-layers-java
Elixir or Phoenix mentioned?               -> Load elixir-antipatterns
API auth, ORM, service boundaries?         -> Load stack-specific backend skill first
Containerization near backend runtime?     -> Load docker-expert + docker-containerization
Otherwise                                  -> Load django-expert for Python backends or spring-boot-3 + java-21 for Java backends
```

---

## Anti-Patterns

- Do not answer backend questions with frontend-only patterns.
- Do not route Java backend work without `java-21` when modern Java language features matter.
- Do not treat auth, persistence, and service boundaries as the same concern.
- Do not pick a framework-agnostic answer when the user already named a concrete stack.
- Do not stop at this router when a stack-specific skill clearly exists.

---

## Commands

```bash
skill({ name: "django-expert" })
skill({ name: "django-drf" })
skill({ name: "spring-boot-3" })
skill({ name: "java-21" })
skill({ name: "hexagonal-architecture-layers-java" })
skill({ name: "elixir-antipatterns" })
skill({ name: "docker-expert" })
skill({ name: "docker-containerization" })
skill({ name: "zod-4" })
skill({ name: "typescript" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| Django backend | `django-expert` |
| DRF API | `django-drf` |
| Spring Boot API | `spring-boot-3` |
| Java architecture | `hexagonal-architecture-layers-java` |
| Elixir service review | `elixir-antipatterns` |
| Backend containers | `docker-expert` |

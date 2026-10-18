---
name: platform-router
description: >
  Route platform, cloud, hosting, and environment-specific deployment requests to the most relevant downstream skills.
  Trigger: When the user asks about hosting platforms, cloud services, deployment targets, environments, Firebase, Vercel, Convex, mobile/desktop/web platforms, or infrastructure-specific platform setup.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks about where/how to host or deploy an application
- User mentions Vercel, Firebase, Convex, cloud platform setup, or environment config
- User asks about web vs mobile vs desktop platform constraints
- User needs deployment target decisions based on app type
- User asks about platform-specific infrastructure or runtime capabilities

---

## Critical Pattern

This is a **router skill**.

Do not stop here.
Load the most relevant downstream skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| Web platform UX or browser-facing app shape | `web` + `frontend-router` |
| Mobile/iOS/React Native platform constraints | `mobile-router` |
| Desktop app or Electron platform | `electron` |
| Frontend hosting with modern React/Next stack | `nextjs-15` + `frontend-router` |
| App platform services like Firebase backend/app stack | `backend-router` + relevant platform/service skill |
| Deployment/hosting infrastructure with runtime concerns | `devops-router` |
| Platform-specific security/transport layer | `network-security-router` |

Load multiple skills when needed. Example:
- Next.js app on a managed platform -> `nextjs-15` + `frontend-router` + `devops-router`
- Mobile app with platform-native UX -> `mobile-router`
- Electron app that also needs web UI patterns -> `electron` + `frontend-router`

---

## Decision Tree

```text
Mobile / iOS / React Native / Expo mentioned?   -> Load mobile-router
Desktop / Electron mentioned?                   -> Load electron
Web platform / browser app mentioned?           -> Load web + frontend-router
Next.js platform/hosting question?              -> Load nextjs-15 + frontend-router
Deployment target / managed platform mentioned? -> Load devops-router
TLS / certs / transport concerns?               -> Load network-security-router
Otherwise                                       -> Load devops-router + frontend-router
```

---

## Anti-Patterns

- Do not answer platform questions as if all runtimes were interchangeable.
- Do not route hosting/deployment target questions only to frontend or backend code skills.
- Do not ignore device/runtime constraints when the platform is the core problem.
- Do not treat mobile, desktop, and web UX constraints as the same thing.

---

## Commands

```bash
skill({ name: "web" })
skill({ name: "frontend-router" })
skill({ name: "mobile-router" })
skill({ name: "electron" })
skill({ name: "nextjs-15" })
skill({ name: "backend-router" })
skill({ name: "devops-router" })
skill({ name: "network-security-router" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| Web app platform | `frontend-router` |
| Mobile platform | `mobile-router` |
| Desktop platform | `electron` |
| Deployment target | `devops-router` |
| Platform transport security | `network-security-router` |

---
name: frontend-router
description: >
  Route frontend, UI, web, React, Next.js, Tailwind, Angular, and design-system requests to the most relevant downstream skills.
  Trigger: When the user asks about frontend architecture, UI implementation, web design, React, Next.js, Angular, Tailwind, styling, forms, state, accessibility, or visual refinement.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks about frontend or web UI architecture
- User mentions React, JSX, hooks, or client-side components
- User mentions Next.js, App Router, server components, or frontend data fetching
- User mentions Angular, standalone components, signals, or forms
- User mentions Tailwind, styling systems, design systems, or responsive UI
- User asks for UX refinement, accessibility, or web platform design guidance
- User needs frontend state management, form validation, or animation routing

---

## Critical Pattern

This is a **router skill**.

Do not stop here.
Load the most relevant downstream skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| General web UI, accessibility, responsive design | `web` + `universal-ui` |
| React component, JSX, hooks | `react-19` + `typescript` |
| Next.js App Router, server/client boundaries | `nextjs-15` + `react-19` + `typescript` |
| Tailwind styling or design tokens | `tailwind-4` + relevant framework skill |
| Angular architecture or components | `angular-architecture` + `angular-core` |
| Angular forms and validation | `angular-forms` + `angular-core` |
| Angular performance, lazy loading, SSR | `angular-performance` + `angular-core` |
| Zod validation in frontend forms or data boundaries | `zod-4` + `typescript` |
| Zustand state management | `zustand-5` + `react-19` + `typescript` |
| Frontend motion, transitions, scroll animation | `animation-router` + relevant framework skill |
| UX/UI audit or professional polish | `universal-ui` + `web` |

Load multiple skills when needed. Example:
- Next.js form with Zod and Tailwind -> `nextjs-15` + `react-19` + `zod-4` + `tailwind-4`
- Angular form-heavy flow -> `angular-core` + `angular-forms` + `angular-architecture`
- React UI needing motion polish -> `react-19` + `animation-router` + `universal-ui`

---

## Decision Tree

```text
React or JSX mentioned?                    -> Load react-19 + typescript
Next.js or App Router mentioned?           -> Load nextjs-15 + react-19 + typescript
Angular mentioned?                         -> Load angular-core (+ angular-architecture as needed)
Tailwind or styling system mentioned?      -> Load tailwind-4 + framework skill
Validation or schemas mentioned?           -> Load zod-4 + typescript
State store mentioned?                     -> Load zustand-5 + react-19 + typescript
Accessibility / responsive web UI?         -> Load web + universal-ui
Motion or animation mentioned?             -> Load animation-router + framework skill
Otherwise                                  -> Load web + universal-ui first
```

---

## Anti-Patterns

- Do not answer frontend requests with backend-only architecture advice.
- Do not route React or Next.js work without `typescript` when the repo uses TS.
- Do not use `tailwind-4` alone for framework-specific UI implementation.
- Do not treat accessibility or responsive UI as optional for web interfaces.
- Do not stop at this router when a downstream framework skill clearly applies.

---

## Commands

```bash
skill({ name: "web" })
skill({ name: "universal-ui" })
skill({ name: "react-19" })
skill({ name: "nextjs-15" })
skill({ name: "typescript" })
skill({ name: "tailwind-4" })
skill({ name: "zod-4" })
skill({ name: "zustand-5" })
skill({ name: "angular-architecture" })
skill({ name: "angular-core" })
skill({ name: "angular-forms" })
skill({ name: "angular-performance" })
skill({ name: "animation-router" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| Generic web UI | `web` |
| UI polish / audit | `universal-ui` |
| React app | `react-19` |
| Next.js app | `nextjs-15` |
| Angular app | `angular-core` |
| Tailwind styling | `tailwind-4` |
| Frontend animation | `animation-router` |

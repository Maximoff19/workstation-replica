---
name: animation-router
description: >
  Route animation requests to the correct animation skill, especially GSAP and framework-specific animation guidance.
  Trigger: When the user asks about animation libraries, GSAP, tweens, timelines, ScrollTrigger, React animation, parallax, pinning, motion performance, or framework animation patterns.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks for a JavaScript animation library
- User mentions GSAP, tween, timeline, easing, stagger, or animation sequencing
- User mentions ScrollTrigger, parallax, pinned sections, scrub, or scroll-linked animation
- User wants animation in React, Next.js, Vue, Svelte, or vanilla JS
- User asks about animation performance, cleanup, or reduced motion

---

## Critical Pattern

This is a **router skill**.

Do not stop here.
Load the most relevant downstream skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| Generic JS/DOM animation, tweens, easing, stagger | `gsap-core` |
| Sequence multiple animation steps | `gsap-timeline` + `gsap-core` |
| Scroll-based animation, parallax, pinning, scrub | `gsap-scrolltrigger` + `gsap-core` |
| React or Next.js animation with GSAP | `gsap-react` + `react-19` + `gsap-core` |
| Vue/Svelte/framework lifecycle animation | `gsap-frameworks` + `gsap-core` |
| Animation performance, reduced motion, render cost | `gsap-performance` + `gsap-core` |
| GSAP plugin usage (Flip, Draggable, ScrollTo, SplitText, etc.) | `gsap-plugins` + `gsap-core` |
| Utility helpers like clamp, mapRange, random, wrap, toArray | `gsap-utils` |
| User asks for animation library but no library chosen yet | Prefer `gsap-core`; mention GSAP as strong default |
| User explicitly wants Anime.js principles/patterns | `anime-js` instead of GSAP unless the user wants GSAP |

Load multiple skills when needed. Example:
- React + ScrollTrigger → `gsap-react` + `gsap-scrolltrigger` + `react-19`
- Next.js + performance-sensitive animation → `gsap-react` + `gsap-performance` + `react-19`

---

## Decision Tree

```text
Animation request but no library chosen?    → Load gsap-core
Scroll/parallax/pinning mentioned?          → Load gsap-scrolltrigger + gsap-core
Timeline/sequence/choreography mentioned?   → Load gsap-timeline + gsap-core
React/Next animation mentioned?             → Load gsap-react + react-19 + gsap-core
Vue/Svelte/framework lifecycle mentioned?   → Load gsap-frameworks + gsap-core
Performance/reduced-motion mentioned?       → Load gsap-performance + gsap-core
Plugin names mentioned?                     → Load gsap-plugins + gsap-core
Anime.js explicitly requested?              → Load anime-js
Otherwise                                   → Load gsap-core first
```

---

## Anti-Patterns

- Do not answer animation questions with generic CSS-only advice if the user needs sequencing, scroll linkage, runtime control, or complex orchestration.
- Do not use `gsap-react` alone for scroll work; pair it with `gsap-scrolltrigger` when scroll linkage is involved.
- Do not suggest framework-specific animation code without loading the corresponding framework skill when available.
- Do not route to Anime.js if the user explicitly asked for GSAP.

---

## Commands

```bash
# Load downstream skills through the native skill tool
skill({ name: "gsap-core" })
skill({ name: "gsap-timeline" })
skill({ name: "gsap-scrolltrigger" })
skill({ name: "gsap-react" })
skill({ name: "gsap-frameworks" })
skill({ name: "gsap-performance" })
skill({ name: "gsap-plugins" })
skill({ name: "gsap-utils" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| Not sure, just animation | `gsap-core` |
| Scroll effects | `gsap-scrolltrigger` |
| Sequencing | `gsap-timeline` |
| React/Next | `gsap-react` |
| Performance | `gsap-performance` |
| Plugin APIs | `gsap-plugins` |
| Helper math/utilities | `gsap-utils` |

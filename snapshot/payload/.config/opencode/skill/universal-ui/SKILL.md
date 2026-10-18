---
name: universal-ui
description: >
  Refina interfaces generadas por IA o mal disenadas y las convierte en
  interfaces profesionales, consistentes y usables en cualquier tecnologia o
  plataforma. Trigger: When improving an existing UI, auditing weak UX/UI
  decisions, or refactoring generated interfaces without assuming a SaaS web dashboard.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "3.0"
---

## Role

Senior Product Designer + Interface Architect + UX Specialist.

## Mission

Analyze existing interfaces and refactor them to improve UX, UI, visual
hierarchy, navigation, accessibility, and consistency.

This skill must work across any technology stack and adapt to context before
proposing changes.

Never assume the interface is a web SaaS dashboard.

---

## Phase 1 - Context Analysis (REQUIRED)

Before proposing changes, identify:

- Product type
- Platform
- User type
- System goal

### Rules

- Understand context before applying design patterns.
- Avoid applying SaaS dashboard patterns to every interface.
- Never redesign the interface without understanding the product context.

---

## Core Principles

### 1. Visual Hierarchy

The interface must clearly show which elements matter most.

Hierarchy is established through:

- Size
- Color
- Position
- Spacing
- Typographic weight

- Avoid interfaces where every element competes for attention.
- Never use the same size and visual weight for all elements.

### 2. Consistency

All components must follow the same visual language.

This includes:

- Buttons
- Inputs
- Cards
- Tabs
- Tables
- Modals
- Icons

- Avoid mixing unrelated visual styles in one interface.
- Never use multiple button styles or multiple icon systems without a clear system reason.

### 3. Color System

Use a coherent palette.

Minimum recommended structure:

- Primary
- Secondary
- Gray scale
- Success
- Warning
- Danger

- Avoid oversaturated colors or random combinations.
- Never use more than 3 primary colors in the same interface.

### 4. Iconography

Use one consistent icon system.

- Avoid icons with conflicting visual styles.
- Never mix icon libraries or use emojis in professional interfaces.

### 5. Spacing

Use a consistent spacing scale.

Recommended scale:

- 4
- 8
- 16
- 24
- 32
- 48
- 64

- Avoid arbitrary spacing with no relation to a system.
- Never use random spacing values per component.

### 6. Typography

Typography must follow a clear hierarchy.

Example levels:

- Hero
- Title
- Subtitle
- Body
- Caption

- Avoid too many font sizes.
- Never use more than two type families in the same interface.

### 7. Information Density

Adapt density to the product type.

- Marketing: less density
- Operational tools: higher density, but structured

- Avoid overloaded interfaces or empty layouts with no purpose.
- Never remove critical information only for aesthetics.

### 8. Noise Reduction

Remove unnecessary elements. Every component must have a clear function.

- Avoid decorative icon overload or redundant buttons.
- Never add purely decorative elements with no functional value.

### 9. Information Grouping

Related elements must be grouped visually.

Use:

- Cards
- Sections
- Panels
- Tabs

- Avoid spreading related information across disconnected areas.
- Never separate elements that belong to the same interaction flow.

### 10. Actions

Primary actions must be visible. Secondary actions should live in contextual menus.

- Avoid interfaces with too many visible buttons.
- Never show every possible action at the same time.

### 11. Interface States

Every interface must contemplate:

- Normal
- Loading
- Empty
- Error
- Success
- Disabled

- Avoid designing only for the ideal state.
- Never leave users without feedback when errors happen.

### 12. Accessibility

The interface must be accessible to all users.

- Adequate contrast
- Clear labels
- Visible feedback

- Avoid interfaces that depend only on color.
- Never use insufficient text contrast or controls that are too small.

### 13. Forms

Forms must be clear and easy to complete.

- Avoid overly long or confusing forms.
- Never show errors without explaining how to fix them.

### 14. Navigation

Navigation must reflect the user's mental model.

- Avoid menus with too many options.
- Never create deep and unnecessary navigation structures.

### 15. Data Visualization

Data must help users understand information.

- Avoid showing numbers without context.
- Never use charts as decoration.

### 16. Internationalization

Interfaces must support different languages and formats.

- Avoid designs that depend on extremely short text.
- Never create layouts that break when content is translated.

---

## Delivery Rules

When analyzing an interface, always return:

1. Diagnosis of problems
2. UX impact of those problems
3. Structural improvement proposal
4. Component reorganization
5. Recommendations adapted to the detected stack

---

## Decision Tree

```text
Is the product context unknown?        -> Identify product, platform, user, and goal first
Is the UI generated or inconsistent?   -> Audit hierarchy, consistency, spacing, and actions
Is the interface operational?          -> Increase density carefully, preserve critical information
Is the interface marketing-oriented?   -> Reduce density, strengthen storytelling and calls to action
Is the stack already defined?          -> Adapt recommendations to existing components and constraints
Otherwise                              -> Refine the current UI without forcing a new visual paradigm
```

---

## Output Format

Use this structure when responding:

```text
Context detected:
- Product type
- Platform
- User type
- System goal

Problems found:
- ...

Impact on UX:
- ...

Structural improvements:
- ...

Component reorganization:
- ...

Stack-adapted recommendations:
- ...
```

---

## Objective

Transform disordered or AI-generated interfaces into:

- Professional interfaces
- Clear experiences
- Consistent systems
- Production-ready UI

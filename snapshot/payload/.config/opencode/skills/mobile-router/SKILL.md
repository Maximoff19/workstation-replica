---
name: mobile-router
description: >
  Route mobile and iOS requests to the correct platform skill, especially React Native and native iOS/SwiftUI guidance.
  Trigger: When the user asks about iOS, SwiftUI, Apple HIG, React Native, Expo, mobile app UI, SF Symbols, Dynamic Type, or platform-specific mobile design and implementation patterns.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- User asks about mobile app architecture or UI
- User mentions iOS, SwiftUI, Apple HIG, SF Symbols, Dynamic Type, sheets, TabView, or NavigationStack
- User mentions React Native, Expo, NativeWind, React Navigation, or cross-platform mobile UI
- User wants native-feeling mobile interfaces
- User asks about platform-specific mobile conventions, gestures, accessibility, or adaptive layouts

---

## Critical Pattern

This is a **router skill**.

Do not stop at this skill.
Load the most relevant downstream platform skill(s) before writing code.

Preferred routing:

| User intent | Load these skills |
|---|---|
| Native iOS UI, SwiftUI, Apple HIG, SF Symbols, Dynamic Type | `mobile-ios-design` |
| Cross-platform mobile app with JS/TS | `react-native` + `typescript` |
| Expo, React Navigation, NativeWind | `react-native` + `typescript` + `tailwind-4` |
| Mobile UX refinement without framework lock-in | `universal-ui` + `mobile-ios-design` |
| iOS-flavored design for RN app | `react-native` + `mobile-ios-design` |
| Mobile app with animation needs | `animation-router` + relevant mobile skill |

Load multiple skills when needed. Example:
- React Native app that must feel native on iPhone → `react-native` + `mobile-ios-design`
- Expo app with polished UI and NativeWind → `react-native` + `tailwind-4` + `universal-ui`
- SwiftUI interface with motion polish → `mobile-ios-design` + `animation-router`

---

## Decision Tree

```text
SwiftUI / Apple HIG / SF Symbols mentioned?   → Load mobile-ios-design
React Native / Expo mentioned?                → Load react-native + typescript
NativeWind / mobile styling mentioned?        → Load react-native + tailwind-4
Need native-feeling mobile UX?                → Load mobile-ios-design (+ universal-ui if refining UX)
Need cross-platform mobile app?               → Load react-native + typescript
Need mobile animations?                       → Load animation-router + mobile skill
Otherwise                                     → Load react-native for app code, mobile-ios-design for iOS UX
```

---

## Anti-Patterns

- Do not answer iOS/SwiftUI questions with web-only UI advice.
- Do not route native iOS design questions only to `react-native`.
- Do not route cross-platform app implementation only to `mobile-ios-design` when real app code needs `react-native`.
- Do not ignore accessibility, tap target size, Dynamic Type, or platform navigation conventions in mobile answers.

---

## Commands

```bash
# Load downstream skills through the native skill tool
skill({ name: "mobile-ios-design" })
skill({ name: "react-native" })
skill({ name: "typescript" })
skill({ name: "tailwind-4" })
skill({ name: "universal-ui" })
skill({ name: "animation-router" })
```

---

## Quick Reference

| Situation | First skill to load |
|---|---|
| Native iOS / SwiftUI | `mobile-ios-design` |
| React Native app | `react-native` |
| Expo / NativeWind | `react-native` |
| iOS UX refinement | `mobile-ios-design` |
| Mobile motion / transitions | `animation-router` |

---
name: figma-use
description: >
  Wrapper skill for the Figma MCP server guide skill. Load this before any `use_figma`
  write action or unique read that executes JavaScript in the Figma file context.
metadata:
  upstream_skill_path: "/Users/batimoff/.agents/skills/figma-use/SKILL.md"
  upstream_references_path: "/Users/batimoff/.agents/skills/figma-use/references"
  library: shared
---

## Purpose

This is a local wrapper so OpenCode can discover the installed `figma-use` skill.

## Canonical Source

- Skill: `/Users/batimoff/.agents/skills/figma-use/SKILL.md`
- References: `/Users/batimoff/.agents/skills/figma-use/references`

## Usage Rule

- ALWAYS load this skill before any `use_figma` tool call.
- Treat the upstream skill file and references directory as the source of truth.
- If you need detailed API guidance, read the canonical files above instead of relying on memory.

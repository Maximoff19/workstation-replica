---
name: system-prompts-leaks
description: >
  Use the local System Prompts Leaks reference repo when the user asks about leaked system prompts,
  Codex/OpenCode prompt text, model instruction comparisons, or historical agent prompt archives.
license: CC0-1.0 (reference repository content)
metadata:
  author: batimoff-local
  version: "1.0"
  repo_path: "/Users/batimoff/.config/ai-references/system_prompts_leaks"
---

## When to Use

- User asks for leaked or archived system prompts
- User wants to compare Codex, ChatGPT, Claude, Gemini, Grok, OpenCode, or Copilot prompts
- User references the `system_prompts_leaks` repository
- User wants a local reference instead of browsing GitHub manually

---

## Local Source of Truth

Primary repo path:

`/Users/batimoff/.config/ai-references/system_prompts_leaks`

Useful top-level folders:

- `Anthropic/`
- `Google/`
- `Misc/`
- `OpenAI/`
- `Perplexity/`
- `xAI/`

High-value files:

- `Misc/opencode.md`
- `OpenAI/codex/`
- `OpenAI/gpt-5.5-thinking.md`
- `Anthropic/claude-code.md`

---

## Workflow

1. Search the LOCAL repo first, not the web.
2. Use file search to locate the exact provider/model file.
3. Read the exact file and cite the path in the answer.
4. Make it explicit when content comes from a community-maintained archive rather than an official vendor publication.
5. If authenticity is uncertain, say so clearly. Do not oversell leaked text as guaranteed ground truth.

---

## Anti-Patterns

- Do not claim the archive is official unless the file itself says it is an official publication.
- Do not answer from memory when the user asks for exact prompt text.
- Do not confuse Codex CLI prompts with ChatGPT web prompts.
- Do not cite stale summaries when the local repo has the exact file.

---

## Quick Reference

| Need | Where to look |
|---|---|
| OpenCode prompt | `Misc/opencode.md` |
| Codex prompts | `OpenAI/codex/` |
| ChatGPT prompts | `OpenAI/` |
| Claude / Claude Code | `Anthropic/` |
| Gemini / Antigravity | `Google/` |
| Grok | `xAI/` |

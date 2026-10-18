---
name: gentleman-guardian-angel
description: >
  Integrate Gentleman Guardian Angel (GGA) for AI-powered code review using OpenCode or other providers.
  Trigger: When setting up GGA, pre-commit AI review, AGENTS.md review rules, or evaluating plugin vs MCP integration with OpenCode.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Setting up `gga` in a repository
- Using `PROVIDER="opencode"` in `.gga`
- Designing `AGENTS.md` rules for pre-commit review
- Evaluating whether GGA should run as CLI, OpenCode plugin wrapper, or MCP bridge
- Adding AI review to local hooks or CI

---

## Critical Patterns

### Pattern 1: Treat GGA as a Review Gate, Not as a Replacement

GGA is an AI review layer.

It does **not** replace:
- tests
- linting
- type checking
- human review

Use this order:

```text
format/lint/typecheck/test
        ↓
GGA AI review
        ↓
git commit / PR
```

### Pattern 2: Start Small With Rules

Bad `AGENTS.md` creates noisy failures.

Start with high-signal rules only:
- no debug logs
- no dead commented code
- no unrelated changes in one commit
- no `any` in TypeScript
- validate external input
- keep UI free of business logic

Avoid fluffy rules like:
- "write cleaner code"
- "follow best practices"
- "make it scalable"

### Pattern 3: Official Integration = CLI + Hooks

GGA is officially a CLI workflow:

```text
gga init
gga install
gga run
gga run --pr-mode
```

Do **not** pretend it is already a native OpenCode plugin or MCP server.

### Pattern 4: OpenCode Integration Strategy

Use this decision model:

| Need | Best Option |
|---|---|
| Fast adoption in a repo | Native GGA CLI + `PROVIDER="opencode"` |
| OpenCode-native UX | Build a thin OpenCode plugin wrapper over `gga` |
| Cross-client tool interoperability | Build an MCP bridge that shells out to `gga` |

Best default: **plugin wrapper over CLI**, not a full rewrite.

### Pattern 5: Be Careful With Nested OpenCode Calls

If GGA uses:

```bash
PROVIDER="opencode"
```

then GGA will invoke OpenCode CLI during review.

This is valid, but watch for:
- latency
- auth/model mismatches
- prompt drift between interactive OpenCode and CLI OpenCode

If stability matters more than purity, consider:

```bash
PROVIDER="claude"
# or
PROVIDER="gemini"
```

while still using OpenCode as the main coding environment.

---

## Decision Tree

```text
Need immediate value in one repo?        → Install GGA and use PROVIDER="opencode"
Need OpenCode commands/tools UX?         → Build thin plugin wrapper over gga CLI
Need real MCP tools for many clients?    → Build MCP bridge around gga CLI
Need deterministic quality checks?       → Keep lint/test/typecheck before GGA
Otherwise                                → Start with CLI integration first
```

---

## Code Examples

### Example 1: Minimal `.gga` for OpenCode

```bash
PROVIDER="opencode"
RULES_FILE="AGENTS.md"
STRICT_MODE="true"
TIMEOUT="300"
FILE_PATTERNS="*.ts,*.tsx,*.js,*.jsx,*.py"
EXCLUDE_PATTERNS="node_modules/*,dist/*,build/*,*.lock"
```

### Example 2: Pin OpenCode model explicitly

```bash
PROVIDER="opencode:anthropic/claude-opus-4-5"
RULES_FILE="AGENTS.md"
STRICT_MODE="true"
```

### Example 3: High-signal `AGENTS.md`

```markdown
# Review Rules

## Architecture
- No business logic inside UI components
- Keep module boundaries clear

## TypeScript
- No any
- Validate external input

## Hygiene
- No debug logs
- No commented dead code
- No unrelated changes in the same commit

## Output Contract
- PASS when compliant
- FAIL with exact file paths and reasons when non-compliant
```

### Example 4: OpenCode plugin wrapper shape

```typescript
// Pseudocode only
export const GGAPlugin = async (ctx) => {
  return {
    tools: {
      gga_run: async () => shell("gga run"),
      gga_pr_review: async () => shell("gga run --pr-mode"),
      gga_install_hook: async () => shell("gga install"),
      gga_config: async () => shell("gga config"),
    },
  };
};
```

### Example 5: MCP bridge shape

```text
OpenCode → MCP tool → local bridge → gga CLI
```

Use MCP only when multiple MCP clients need the same capability.

---

## Commands

```bash
# Install GGA (recommended)
brew install gentleman-programming/tap/gga

# Initialize per-repo config
gga init

# Install native git hook
gga install

# Review staged files
gga run

# Review full PR diff
gga run --pr-mode

# Show effective config
gga config

# Check cache
gga cache status
```

---

## Anti-Patterns

### Don't pretend AI review is deterministic

```text
Bad: "GGA replaces tests"
Good: "GGA complements tests with standards enforcement"
```

### Don't start with giant rule files

```text
Bad: 150 vague rules nobody can satisfy consistently
Good: 10-20 precise, high-signal rules
```

### Don't build MCP first unless interoperability is required

```text
Bad: Re-architect the tool before proving value
Good: CLI integration first, wrapper second, MCP only if justified
```

---

## Quick Reference

| Goal | Recommended approach |
|---|---|
| Use GGA today in one repo | `gga` CLI + git hook |
| Use OpenCode as provider | `PROVIDER="opencode"` |
| Improve UX inside OpenCode | local plugin wrapper |
| Share capability with other MCP clients | MCP bridge |
| Reduce false positives | smaller `AGENTS.md` + stricter output contract |

## Resources

- GGA repo: `https://github.com/Gentleman-Programming/gentleman-guardian-angel`
- Key concepts: `.gga`, `AGENTS.md`, `gga install`, `gga run`, `gga run --pr-mode`

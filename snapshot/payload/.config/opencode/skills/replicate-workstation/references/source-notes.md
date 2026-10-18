# Source snapshot notes

Inspected on 2026-10-18. The live exported files and manifest take precedence if
the source changes later. These notes intentionally contain no credential values.

## Appearance

| Application | Observed configuration |
|---|---|
| Neovim | LazyVim; `gentleman-kanagawa-blur`, transparent backgrounds in other installed themes |
| OpenCode | Custom `themes/gentleman.json`; selected theme persisted as `gentleman` in UI state |
| Ghostty | `Citruszest`, `IosevkaTerm NF` at 14 pt, opacity 0.95, blur radius 20, custom cursor shader |
| tmux | Kanagawa theme, status at top, `Ctrl+a` prefix, vi copy mode |

OpenCode's `tui.json` did not explicitly select a theme. The exported copy gains
the selected UI-state theme so a fresh computer does not revert to a default.
The original file is untouched. Existing duplicate Ghostty theme entries remain.
Fonts are not bundled: install the same Nerd Font separately. OS compositors can
render transparency, blur, and shaders differently.

## Keymap smoke tests

`<leader>` is whatever the restored LazyVim setup resolves at runtime; verify it
instead of assuming the default. Keep all plugin specs because many define keys.

| Context | Representative source mappings |
|---|---|
| Neovim | `Ctrl+s` custom save; `Ctrl+c` returns to normal mode; insert `Ctrl+b` deletes to word end |
| Pane navigation | `Ctrl+h/j/k/l`, `Ctrl+\\`, `Ctrl+Space` via nvim-tmux-navigation |
| Files/buffers | `-` opens Oil; `<leader>bq` closes other buffers |
| Search | Visual `<leader>sg` / `<leader>sG` search selected text |
| OpenCode inside Neovim | `<leader>aa` toggle; `as` select; `ai` ask; `aI` ask with context; `ab` buffer |
| Ghostty | `Alt+v/d` splits; `Alt+h/j/k/l` navigation; `Shift+Enter` sends its configured escape sequence |
| tmux | `Ctrl+a`, then `v` / `d` splits |

## Non-file dependencies and caveats

- Source versions: Neovim 0.11.6, OpenCode 1.18.34, Node.js 23.11.0, npm 10.9.2.
  The export records available versions again. Do not upgrade as part of migration.
- Local MCPs need Node/npx, Engram, and CodeGraph. The Engram executable path was
  Homebrew-specific. No binary or memory database is copied.
- Figma Desktop's MCP points to localhost port 3845. It requires Figma Desktop
  running on the destination; copying the URL does not provide that service.
- OAuth-backed services (including Vercel, Firebase, Notion, and Atlassian) need
  fresh authorization. One MCP had an inline API key; the exported copy uses a
  named environment reference instead. Never recover it from backups for transfer.
- Several MCP and plugin packages use `latest`, version ranges, or remote URLs.
  Config equality does not pin those services. Review package locks and installed
  versions; report any dependency that cannot be reproduced exactly.
- Neovim plugins include Copilot, Claude, Gemini, Avante, CodeCompanion, Obsidian,
  and OpenCode integrations; account sessions and the Obsidian vault are excluded.
- The `obsidian-memory` OpenCode plugin records session content into an Obsidian
  vault. Review and explicitly accept that behavior before starting copied plugins.
- Agents exist both inline and as Markdown files, and some prompts/permissions
  conflict. Preserve them; do not redesign the user's agents during replication.
- Referenced external repositories (for example system-prompt archives) are not
  bundled. Copying a skill that points at a repo does not copy that repo.
- Existing tmux Linux clipboard fallback uses `clip`; standard Linux may need
  `wl-copy` or `xclip`. Review that explicit platform change with the user.
- Native macOS terminal shortcuts, fish paths, and clipboard integration may need
  adaptation on Linux/WSL. Do not claim that these work without checking them.

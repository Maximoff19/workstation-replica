---
name: replicate-workstation
description: >
  Clone or migrate this user's Neovim and OpenCode configuration to another PC,
  including nvim keymaps, themes, agents, all installed skills, plugins, profiles,
  and MCP definitions. Use for replicar configuracion, clonar opencode, migrar nvim,
  otra PC, same keybindings, workstation backup, or restoring a replica bundle.
metadata:
  version: "1.0.0"
  author: batimoff
---

# Replicate Neovim and OpenCode

Recreate the **actual exported files**, not an approximation written from memory.
This skill includes a Python 3.9+ standard-library tool to export, inspect, restore,
and verify a portable ZIP. A skill alone cannot recover files on another computer:
**transfer the bundle as well as these instructions**.

## Safety contract

- Work directly. Do not delegate or launch another agent.
- Never print, commit, transfer, or request credential values. The exporter
  substitutes recognizable credentials with environment references and excludes
  authentication stores, histories, caches, mobile tokens, and old backups.
  Detection is best-effort, not a guarantee: inspect privately before sharing.
- Do not change the source installation, model selection, agent prompts, keymaps,
  permissions, or themes to make it easier to export. Preserve conflicts too;
  explain them rather than silently fixing them.
- Restore defaults to **dry run**. Review the plan before using `--apply`.
  Applying replaces the selected configuration roots, backing up existing roots
  first. It does not merge old skills or silently keep conflicting plugins.
- Never install packages, run copied plugins, or start copied MCP servers before
  reviewing their code and permissions. This configuration allows broad access.
- Do not promise identical runtime behavior: credentials, installed binaries,
  provider access, hardware, terminal rendering, and unpinned remote packages are
  not cloned. Native Windows needs manual adaptation; prefer Linux/WSL or macOS.

## Quick path: source computer

Locate `scripts/replica.py` relative to this skill. The default installed path is:

```bash
python3 "$HOME/.config/opencode/skills/replicate-workstation/scripts/replica.py" export --output "$HOME/workstation-replica.zip"
python3 "$HOME/.config/opencode/skills/replicate-workstation/scripts/replica.py" inspect --bundle "$HOME/workstation-replica.zip"
```

Export refuses to overwrite an existing bundle. Pick a new name for each snapshot.
Transfer the ZIP privately, for example by USB or an authenticated file transfer.
There is no repository URL to clone unless the user creates one separately.

## Quick path: destination computer

1. Obtain Python 3 and the ZIP. Review its top-level `SKILL.md`, `replica.py`,
   `manifest.json`, and `references/source-notes.md` before executing copied code.
   Extract only those top-level instructions/tool files into a working directory
   with your trusted archive viewer; the tool reads payload files directly from ZIP.
2. Inspect and plan using the extracted tool:

   ```bash
   python3 replica.py inspect --bundle workstation-replica.zip
   python3 replica.py restore --bundle workstation-replica.zip
   ```

3. Review replacement roots, required environment variable **names**, and missing
   dependencies. Close Neovim/OpenCode/terminal processes that could rewrite config.
   Then apply the reviewed plan:

   ```bash
   python3 replica.py restore --bundle workstation-replica.zip --apply
   python3 replica.py verify --bundle workstation-replica.zip
   ```

   Add `--terminal` to **both** restore and verify only if Ghostty, tmux, and Zellij
   settings should also replace the destination's terminal configuration.
   `--home /absolute/destination/home` is available for isolated testing, not for
   installing into another user's account without their permission.

4. Read the printed backup location. If rollback is necessary, close applications,
   move the newly installed managed roots aside, and move the corresponding roots
   from that backup back to their original locations. A previously absent root has
   no backup and must instead be removed after preserving any new local changes.
5. Follow [runtime setup](references/runtime-setup.md), then quit and restart
   OpenCode. Configuration-time files are not refreshed in a running session.

## Scope and fidelity

| Included | How fidelity is preserved |
|---|---|
| `~/.config/nvim/` | All Lua, plugin specs, spelling files, `lazy-lock.json`, LazyVim settings |
| `~/.config/opencode/` | Runtime/TUI JSON, AGENTS.md, agent(s), command(s), both skill directories, plugins, prompts, profiles, themes, package manifests/locks |
| `~/.agents/skills/`, `~/.claude/skills/` | Complete trees, including shared references, scripts, and assets; symlinks are materialized |
| Selected OpenCode UI preferences | Allowlisted presentation/profile preferences from `kv.json`; never session/model/auth history |
| Optional terminal roots | Ghostty themes/shaders/keybinds, Zellij, `.tmux.conf`, tmux config assets |
| Inventory | Source executable versions, MCP names, inline agents, skill names and paths, hashes, omissions, secret variable names |

User-home paths are rewritten on restore, including paths in prompts and skills.
Absolute Homebrew MCP executable paths become executable names resolved through
the destination PATH. tmux's Homebrew fish path is adapted if necessary. Other
platform-specific paths are not guessed or rewritten indiscriminately.

Non-default `XDG_CONFIG_HOME`, `XDG_STATE_HOME`, `NVIM_APPNAME`, `OPENCODE_CONFIG*`,
or `OPENCODE_TUI_CONFIG` are not handled by this snapshot tool: export fails when
these overrides are active. Explicitly configured external skill paths, local
plugin paths outside captured roots, project `.opencode/` overrides, external
reference repos, vault content, fonts, OS services, and binaries need a separate
reviewed transfer/install. Built-in skills ship with OpenCode rather than files.

The ZIP's manifest hashes detect accidental changes; they are **not a signature**
or proof that an untrusted bundle is safe. Keep it private even after redaction:
prompts, paths, server URLs, and permission rules can be personal information.

## Completion gate

- Report managed roots, indexed skills, and every omitted/unavailable component.
- Run the tool's `verify`, then the runtime checks. Hash verification proves file
  fidelity after documented transformations, not MCP connectivity or plugin health.
- Confirm the configured Neovim colorscheme and OpenCode theme visually.
- Check representative keymaps with `:verbose nmap` and `:verbose imap`; mappings
  can also be defined in plugin specs, not just `config/keymaps.lua`.
- Confirm MCP connection status only after the user reconnects each account.
- State what still needs login, environment variables, OS-specific adjustment, or
  manual installation. Never claim the other PC was configured without testing it.

## Resources

- [Source-specific notes](references/source-notes.md)
- [Runtime setup and verification](references/runtime-setup.md)
- Export/restore tool: `scripts/replica.py`
- Regression tests: `scripts/test_replica.py` (`python3 -m unittest discover -s scripts -v`)

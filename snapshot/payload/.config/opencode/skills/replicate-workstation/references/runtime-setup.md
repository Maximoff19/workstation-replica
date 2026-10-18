# Restore runtime dependencies after restoring files

The restore tool never runs package managers or executes copied configuration.
Inspect the bundle and its permissions before continuing. Installation requires
network access and must be approved in the destination environment.

## 1. Match the environment

Read `manifest.json` for observed executable versions. Install Neovim, OpenCode,
Git, Python 3.9+, Node/npm, Bun if needed by plugins, ripgrep, fd, and build tools using
the destination OS's trusted package manager. Install Engram and CodeGraph from
their official distributions if keeping those MCPs enabled. Use the same versions
when available; document any mismatch rather than selecting a different model.

The original Node version is not a recommendation to use an unsupported runtime.
If unavailable or unsupported, agree on a supported alternative and test it.

If copying terminal roots, also install Ghostty, tmux, fish, Zellij, and
**IosevkaTerm Nerd Font**. Fonts and terminal compositor behavior are not in ZIP.

## 2. Install locked dependencies

In `~/.config/opencode`, review `package.json` and lifecycle scripts before running
`npm ci` when `package-lock.json` is present. If only a Bun lock exists, review the
installed Bun version and use its frozen-lockfile install. Do not delete lockfiles
to make an installation succeed. OpenCode's separate npm plugins may use ranges
or `latest`; these are not made reproducible merely by copying `package-lock.json`.

Restore Neovim plugins from the captured lockfile, **not** `Lazy sync` or update:

```bash
nvim --headless '+Lazy! restore' +qa
```

Run interactively if startup/build steps require interaction. Review `:Lazy` and
`:checkhealth` afterward. Install LSP servers, Treesitter parsers, and debug
adapters through the restored configuration's managers as needed. They are not
binary-compatible payloads in the snapshot.

For tmux, install TPM from its official repository if absent, review the plugin
list, then use TPM to install those plugins. Plugin revisions without a lockfile
remain a fidelity limitation. Zellij plugin binaries included in configuration
still need review before execution.

## 3. Reconnect accounts privately

The `inspect` command lists required environment variable names. Set them through
the OS's trusted credential/environment workflow; never paste their values into
chat or commit them. OpenCode's `{env:VARIABLE}` interpolation works in JSON
configuration. Placeholders in other file formats are deliberate review markers:
replace them with the format's appropriate environment lookup before runtime.

Use OpenCode's connection UI for providers and MCP OAuth as appropriate to the
installed version. Authenticate Firebase and other CLIs separately. Start Figma
Desktop's local MCP if required. No login, subscription, token, or provider/model
availability is transferred by this skill.

## 4. Verify after restarting

```bash
python3 replica.py verify --bundle workstation-replica.zip
```

Use `--terminal` here only if it was used for restore. Verification compares
transformed payload bytes and checks for extra config files, excluding generated
dependency/cache/history files. It is intended to run **before** runtime installers
change configuration or lockfiles; rerun afterward and review legitimate drift.

In Neovim:

```vim
:echo g:colors_name
:echo mapleader
:verbose nmap <C-s>
:verbose nmap <leader>aa
:verbose imap <C-b>
:checkhealth
```

Expect `gentleman-kanagawa-blur` unless the captured source changed. Confirm the
OpenCode theme is `gentleman`, agents/commands/skills are visible, and MCP status
matches the manifest after reconnecting. Check terminal colors, font glyphs,
splits, clipboard, and modifier keys manually on the actual destination.

Report file verification separately from runtime health, service connectivity,
and visual confirmation. Never equate an offline restore test with a working PC.

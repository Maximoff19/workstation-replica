# Reproduce the terminal prompt symbol

The source uses **Starship** initialized from Fish. Its prompt character is
`󰭟` (Unicode **U+F0B5F**), not a separate image or a Ghostty application icon.

- [starship.toml](starship.toml) is the exact captured Starship configuration.
- [prompt-symbol.txt](../assets/prompt-symbol.txt) contains the single symbol.
- The source terminal selects **IosevkaTerm NF**, size 14. Install a compatible
  IosevkaTerm Nerd Font and select it in Ghostty so the private-use glyph renders.
  Font binaries are not included. A missing glyph usually appears as a box.

## Download and install

Download to the working directory first; this does not replace live configuration:

```bash
curl --fail --location --proto '=https' --tlsv1.2 \
  https://raw.githubusercontent.com/Maximoff19/workstation-replica/main/terminal/starship.toml \
  --output starship.toml
```

Install Starship from its official distribution, review the downloaded file,
back up any existing `~/.config/starship.toml`, and place this file at that path.
If `STARSHIP_CONFIG` is set, use its configured path instead.

For Fish, ensure this line appears **once** in `~/.config/fish/config.fish`:

```fish
starship init fish | source
```

Do not add a second initialization when it already exists. Restart Fish after
configuration. No shell-history, universal-variable, credential, or full Fish
configuration file is published by this addition.

## Captured appearance

```toml
[character]
success_symbol = "[󰭟 ](fg:green)"
error_symbol = "[󰭟 ](fg:red)"
```

The captured palette is `catppuccin`: success is `#a6e3a1`, error is `#f38ba8`.
The full file also preserves directory, Git branch, language-version, and time
formatting. It was captured with Starship 1.24.2.

These prompt files were added after the v1.0.0 release. Download them separately:
the original configuration ZIP does not restore Starship or change the shell.

# Caelestia-CLI (Matt's fork)

Personal fork of [`caelestia-dots/cli`](https://github.com/caelestia-dots/cli).
Origin: `git@github.com:mattmaddux/Caelestia-CLI.git`. Upstream remote is kept
but full divergence from upstream is expected — do not assume PR-back.

The companion shell fork lives at `~/Dev/Caelestia-Shell/`. Dotfiles repo is
at `~/.dotfiles/` (already merged off the Caelestia dots fork; that one is
gone).

## What this is

Python CLI (entry point `caelestia`). Provides:

- `caelestia shell ...` — IPC into the Quickshell-based shell
- `caelestia scheme` — Material You color generation, writes runtime theme
  files consumed by the shell, btop, hyprland, GTK/Qt, terminals, etc.
- `caelestia wallpaper`, `screenshot`, `record`, `clipboard`, `emoji`,
  `toggle`, `resizer` — misc desktop helpers

Build: hatchling + hatch-vcs. Python ≥ 3.13. Runtime deps: `pillow`,
`materialyoucolor`. External binaries listed in `README.md`.

Theme outputs land in `~/.local/state/caelestia/theme/` and a few system
paths (gitignored in `~/.dotfiles/.gitignore`: `.config/btop/themes/`,
`.config/hypr/scheme/current.conf`).

## Current state

- Fresh fork, no local changes yet.
- System is currently running the AUR `caelestia-cli` package, not this fork.

## Immediate goals (in order)

1. **Dockerize the build.** Produce a wheel + fish completions without
   installing build tooling on the host. Matt builds everything in Docker as
   a rule — keep the host clean.
   - Inputs: this repo mounted in.
   - Outputs (to a `dist/` or similar on the host):
     - `caelestia-*.whl`
     - `completions/caelestia.fish` (already in tree, just needs to be
       picked up)
   - Base image: Arch is fine (matches host); python:3.13-slim also works
     since this is pure Python.
   - Build deps inside container: `python-build`, `python-installer`,
     `python-hatch`, `python-hatch-vcs`.
   - The build needs git history present (hatch-vcs derives version from
     tags) — don't shallow-clone in a way that hides tags.

2. **Install path off the system package.** Once the wheel builds cleanly:
   - `sudo pacman -Rns caelestia-cli` (confirm with Matt first)
   - Install the locally-built wheel into a user/site location, OR set up a
     `pipx`-style isolated install. Decide based on how the shell fork ends
     up calling `caelestia`.
   - Drop `completions/caelestia.fish` into
     `/usr/share/fish/vendor_completions.d/` or a user-local equivalent.

3. **Verify parity with stock.** Smoke-test: `caelestia shell -s`,
   `caelestia scheme set -n dynamic`, `caelestia wallpaper -r`,
   `caelestia screenshot`. The shell fork should keep working unchanged.

4. **Then customization.** No specific changes queued yet — wait for Matt.

## Conventions / things to know

- **Fish-first.** Matt uses fish as login shell. Any helper scripts in this
  repo or alongside the Docker build should be fish, not bash, unless
  there's a reason.
- **Don't chain Bash commands with `&&` in tool calls** — issue separate
  Bash calls (each auto-approves under Matt's permission settings). This
  applies to agent tool use, not to scripts on disk.
- **Confirm before installing system packages or running `pacman -R`.**
- **Matt commits and pushes himself.** Stage changes, write good messages,
  but don't `git commit` or `git push` unless explicitly asked.
- Theme runtime outputs are deliberately gitignored in `~/.dotfiles/` —
  don't try to track them.
- Hardware: ROG Flow Z13 (CachyOS / Hyprland / Caelestia). External
  monitor enumerates as DP-1, DP-2, or HDMI-A-1 depending on USB-C port —
  matters if you touch anything monitor-related (probably won't here).

## Pointers

- Shell fork: `~/Dev/Caelestia-Shell/` (has its own AGENTS.md)
- Dotfiles: `~/.dotfiles/`
- Upstream issues/PRs: https://github.com/caelestia-dots/cli
- Quickshell docs: https://quickshell.outfoxxed.me

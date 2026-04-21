# npm Global Install Failing Silently on macOS

## Symptoms
- `curl -fsSL https://install.sh | bash` fails with "npm install failed"
- Installer log files are empty — no error output at all
- Script retries and fails again with no useful diagnostics

## Root Cause
`/usr/local/lib/node_modules` is owned by root, so npm can't write to it
without sudo. The installer runs silently (`--silent` flag), so the
EACCES permission error never surfaces in its log.

## Fix
Point npm to a user-owned prefix instead:

```bash
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Then retry the installer.

## Debugging Tip
If an installer's log is empty, bypass it and run npm directly with
full verbosity to see the real error:

```bash
npm install -g <package> --loglevel verbose 2>&1 | tail -80
```

## Related
- cmake missing: `brew install cmake` (needed for packages that build
  llama.cpp or other native binaries)
- If brew isn't on PATH: `eval "$(/opt/homebrew/bin/brew shellenv)"`
  and add that line to ~/.zshrc
* URL: https://www.reddit.com/r/ClaudeAI/comments/1kduobf/claude_code_still_charging_me_despite_having_max/

# QUOTE:

# CC CLI Clean Reinstall MacOS

12 Nov 2025

Jon Chun

Complete uninstallation and reinstallation fixed it. Here are the exact steps if you're on macOS:

1. **Completely uninstall Claude Code and remove all traces:**

\# Uninstall the package  
npm uninstall \-g u/anthropic-ai/claude-code

\# Remove all configuration files  
rm \-rf \~/.claude

\# Clean the npm cache  
npm cache clean \--force

rm \-rf \~/.npm/\_cacache/content-\*/\*claude\*

1. **Install the latest version:**

\# Install the latest version  
npm install \-g @anthropic-ai/claude-code@latest

1. **Start Claude Code and select the Claude app option:**

\# Start Claude  
claude

You should now see both login options:

1. Anthropic Console (API usage billing)  
2. Claude app (requires Max subscription)

Select option 2, and you'll be able to use Claude Code with your Max plan without additional API charges.

Hope this helps anyone else stuck with the same problem\!











# Grok4 (20251112):

# PROMPT #1:

###DIRECTIONS:
Complete uninstallation and reinstallation fixed it. Here are the exact steps if you're on macOS:

1. Completely uninstall Claude Code and remove all traces:

# Uninstall the package
npm uninstall -g u/anthropic-ai/claude-code
# Remove all configuration files
rm -rf ~/.claude
# Clean the npm cache
npm cache clean --force
rm -rf ~/.npm/_cacache/content-*/*claude*

1. Install the latest version:

# Install the latest version
npm install -g @anthropic-ai/claude-code@latest

1. Start Claude Code and select the Claude app option:

# Start Claude
claude
You should now see both login options:

1. Anthropic Console (API usage billing)

2. Claude app (requires Max subscription)

Select option 2, and you'll be able to use Claude Code with your Max plan without additional API charges.
Hope this helps anyone else stuck with the same problem!
 
###TERMINAL:
❯ claude --version
2.0.37 (Claude Code)
❯ which -a claude
/Users/jonc/.local/bin/claude
❯ claude doctor
 Diagnostics
 └ Currently running: native (2.0.37)
 └ Path: /Users/jonc/.local/bin/claude
 └ Invoked: /Users/jonc/.local/share/claude/versions/2.0.37
 └ Config install method: native
 └ Auto-updates: default (true)
 └ Search: OK (bundled)
 Press Enter to continue…
❯ npm list -g --depth=0 | grep 'anthropic'
❯ brew list | grep 'anthropic'
❯ npm list -g --depth=1 | grep 'anthropic'
❯ npm list -g --depth=2 | grep 'anthropic'
│ │ ├── @anthropic-ai/sdk@0.54.0
    ~/code/sentimentarcs  on   main ?1 
 
###INSTRUCTIONS:
Given these ###DIRECTIONS to completely remove CC CLI from a MacOS system at the CLI within ghossty/oh-my-zsh/powerline10k and this ###TERMINAL - please think hard to refine and customize step-by-step instructions to ensure a full removal and clean reinstall of CC CLI as of Nov 12, 2025

# RESPONSE #1:

### Refined Steps for Complete Removal and Clean Reinstall of Claude Code CLI on macOS

As of November 12, 2025, Claude Code CLI (version 2.0.37 in your current setup) supports multiple installation methods: native (your current method, as shown by `claude doctor` output with "native" install and paths in `~/.local/share/claude` and `~/.local/bin/claude`), NPM, and Homebrew. Your terminal output confirms a native installation (no global NPM package for `@anthropic-ai/claude-code` and no Brew formula), with a lingering `@anthropic-ai/sdk` dependency possibly from partial installs or other tools.

The provided directions focus on NPM-based uninstall/reinstall, which has resolved similar auth/billing issues for users with Pro/Max subscriptions by allowing selection of the "Claude app" login option (subscription-based, no extra API charges). However, since your install is native, we'll customize the steps to fully remove native traces first, then clean any NPM/Homebrew overlaps, and reinstall via NPM (as in directions) for consistency and to enable the subscription login fix. This avoids potential native installer bugs reported in 2025 (e.g., intermittent disappearance or auth glitches).

**Warnings**:
- These steps permanently delete files—back up `~/.claude/` if you have custom configs.
- Run in your Ghostty terminal with Oh My Zsh/Powerlevel10k (no special adjustments needed, as it's just zsh).
- After removal, restart your terminal or run `source ~/.zshrc` to refresh PATH.
- If you prefer native reinstall (recommended by Anthropic docs), replace the reinstall step with: `curl -fsSL https://claude.ai/install.sh | bash -s latest`.
- Ensure Node.js is installed (v18+); if not, install via `brew install node` or https://nodejs.org.

#### Step 1: Verify Current Installation and Backup (Optional)
- Run these to confirm paths and back up configs:
  ```
  claude doctor
  which -a claude
  ls -la ~/.local/bin/claude ~/.local/share/claude ~/.claude
  cp -r ~/.claude ~/claude-backup-$(date +%Y%m%d)  # Optional backup
  ```

#### Step 2: Uninstall Native Installation
- Remove the CLI binary and shared data (specific to native method):
  ```
  rm -f ~/.local/bin/claude
  rm -rf ~/.local/share/claude
  ```
- This targets your invoked path from `claude doctor` and eliminates versions like 2.0.37.

#### Step 3: Remove Configuration and Cache Files
- Clear all Claude Code configs, caches, and potential residuals:
  ```
  rm -rf ~/.claude
  rm -f ~/.claude.json
  rm -rf ~/Library/Application\ Support/claude-code
  rm -rf ~/.cache/claude-code
  rm -rf ~/.config/claude-code
  ```
- These cover common locations from community reports and prevent auth conflicts.

#### Step 4: Clear macOS Keychain Entries
- Remove stored credentials (OAuth tokens or API keys) to avoid "invalid bearer token" errors:
  ```
  security delete-generic-password -a ${USER} -s "Claude Code" || true
  security delete-generic-password -a ${USER} -s "Claude Code-credentials" || true
  ```
- The `|| true` ignores "not found" errors safely.

#### Step 5: Clean NPM Traces (Even If Not Primary Install)
- Uninstall any global package and clear caches (addresses the lingering `@anthropic-ai/sdk` and potential overlaps):
  ```
  npm uninstall -g @anthropic-ai/claude-code
  npm cache clean --force
  rm -rf ~/.npm/_cacache/content-*/*claude*
  ```
- If permission errors occur, avoid `sudo`—fix NPM permissions with: `mkdir -p ~/.npm-global && npm config set prefix '~/.npm-global'` (add to `~/.zshrc` if needed).

#### Step 6: Check for Homebrew or Other Residuals
- Uninstall if any Brew formula exists (your `brew list` is empty, but safe to run):
  ```
  brew uninstall --cask claude-code || true
  brew uninstall anthropic/tap/claude-code || true
  ```
- Search system-wide for any missed files (optional, may take time):
  ```
  find ~ -name "*claude-code*" 2>/dev/null
  sudo find / -name "*claude-code*" 2>/dev/null  # If needed, enter password
  ```
- Manually remove any relevant findings (e.g., rm paths).

#### Step 7: Verify Complete Removal
- Confirm no traces:
  ```
  which claude  # Should output nothing
  claude --version  # Should error: command not found
  echo $PATH | grep claude  # Should be empty
  ```
- If `claude` still exists, check `~/.zshrc` or `~/.zprofile` for aliases/exports and remove them.

#### Step 8: Reinstall via NPM (To Enable Subscription Login Fix)
- Install the latest version:
  ```
  npm install -g @anthropic-ai/claude-code@latest
  ```
- This should place the binary in `~/.npm-global/bin/claude` or similar—add to PATH if needed: `export PATH="$HOME/.npm-global/bin:$PATH"` in `~/.zshrc`, then `source ~/.zshrc`.

#### Step 9: Start and Configure Claude Code CLI
- Launch the CLI:
  ```
  claude
  ```
- You'll see login options:
  1. Anthropic Console (API usage billing) – Avoid if you want subscription-only.
  2. Claude app (requires Max/Pro subscription) – Select this for your $20/mo plan, no extra charges.
- Follow the browser popup to log in with your Claude.ai account.
- Test: Send "hello" in the CLI prompt—no 401 errors.

#### Step 10: Post-Reinstall Verification
- Check version and setup:
  ```
  claude --version  # Should show latest (e.g., >2.0.37)
  claude doctor  # Confirm NPM install method
  ```
- If issues persist, migrate to native post-NPM: `claude migrate-installer`.

This customized process ensures a thorough clean (addressing your native setup) while following the directions' NPM approach for the billing fix. If you encounter errors (e.g., during NPM install), share output for further tweaks.
# Provider Attribution Settings

How to stop AI coding tools from adding `Co-authored-by` lines (or changing the author name) in your Git commits.

| Tool | Adds branding by default? | Where to Change It | How to Turn It Off |
| :--- | :--- | :--- | :--- |
| [**Aider**](https://aider.chat) (CLI) | **Yes** *(changes author name)* | `.aider.conf.yml` or CLI flag | `--no-attribute-author`<br>`--no-attribute-committer` |
| [**Antigravity**](https://antigravity.google/docs/cli/gcli-migration/) (`agy` CLI / IDE) | **No** | `~/.gemini/antigravity/settings.json` | No action needed |
| [**Claude Code**](https://claude.com) (CLI / IDE) | **Yes** | `~/.claude/settings.json`<br>*(or `.claude/settings.json`)* | `"attribution": { "commit": "", "pr": "", "sessionUrl": false }`* |
| [**Codex**](https://github.com) (CLI) | **No** | `~/.codex/config.toml` | No action needed |
| [**Cursor**](https://cursor.com) (CLI) | **Yes** | `~/.cursor/cli-config.json` | `"attribution": { "attributeCommitsToAgent": false }` |
| [**Cursor**](https://cursor.com) (Desktop IDE) | **Yes** | `Settings > Git & Pull Requests` | Turn off **Commit Attribution** and **PR Attribution** |
| [**GitHub Copilot**](https://github.com) (CLI) | **Yes** | `~/.copilot/settings.json` | `"includeCoAuthoredBy": false` |
| [**GitHub Copilot**](https://visualstudio.com) (VS Code) | **Yes** | `settings.json` | `"git.addAICoAuthor": "off"` |
| [**OpenCode**](https://github.com) (CLI) | **Yes** | `~/.config/opencode/oh-my-opencode.json` | `"commit": { "include_co_authored_by": false }`** |

*\*Replaces the older `includeCoAuthoredBy` setting in Claude Code.*  
*\*\*Applies to the Oh-My-OpenCode plugin. Core OpenCode does not have a setting to disable this yet, so use the `commit-msg` hook instead.*

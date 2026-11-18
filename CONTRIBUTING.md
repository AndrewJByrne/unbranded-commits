# Contributing

Contributions that keep the provider reference table and hook patterns up to date are welcome.

## Guidelines

- **Provider Settings ([`providers.md`](providers.md)):** Add or update rows with the tool name, surface, config file path, and exact key/value pair. Include a link to official documentation or release notes in the pull request description when available.
- **Hook Patterns ([`commit-msg`](commit-msg) and [`commit-msg-warn`](commit-msg-warn)):** Add new tool identifiers to the `AI_PATTERN` variable if a tool injects `Co-authored-by:` or `Made-with:` trailers by default. The variable is duplicated in both scripts, so update both. Names match as whole words.
- **Issues:** Open an issue if a documented configuration key has been deprecated or no longer prevents trailer injection.

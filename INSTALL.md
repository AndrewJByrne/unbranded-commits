# Install

Run these from the root of a clone of this repo. Pick one script:

- `commit-msg` replaces vendor trailers with `Assisted-by: AI`.
- `commit-msg-warn` stops the commit and shows the vendor lines.

```sh
mkdir -p ~/.git-hooks
cp commit-msg ~/.git-hooks/commit-msg   # or: cp commit-msg-warn ~/.git-hooks/commit-msg
chmod +x ~/.git-hooks/commit-msg
git config --global core.hooksPath ~/.git-hooks
```

## Check it works

```sh
printf 'test\n\nCo-authored-by: Cursor <c@cursor.com>\n' > /tmp/msg
~/.git-hooks/commit-msg /tmp/msg; cat /tmp/msg
```

`commit-msg` prints the message with `Assisted-by: AI` in place of the Cursor line. `commit-msg-warn` prints the vendor line and exits 1.

## Before you install

- `cp` overwrites any existing `~/.git-hooks/commit-msg`.
- A global `core.hooksPath` replaces every repo's own `.git/hooks`. Repos that use a hook manager (Husky, pre-commit, lefthook) won't run this script unless that tool is set up to call it.
- Only `commit-msg` is installed. If you rely on other global hooks (such as `pre-commit`), add them to `~/.git-hooks` too.

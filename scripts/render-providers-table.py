#!/usr/bin/env python3
"""Render the table in providers.md to a PNG (handy for pasting into Medium).

Usage:
    python3 -I scripts/render-providers-table.py
    python3 -I scripts/render-providers-table.py --only "Claude Code,Cursor (CLI)"
    python3 -I scripts/render-providers-table.py -o assets/providers-table.png

Needs only Python 3, Google Chrome and ImageMagick (magick or convert).
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS = """
body { margin: 0; padding: 32px; background: #fff; color: #1f2328;
       font: 15px/1.5 -apple-system, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }
table { border-collapse: collapse; }
th, td { border: 1px solid #d0d7de; padding: 8px 14px; text-align: left; vertical-align: top; }
th { background: #f6f8fa; font-weight: 600; }
tr:nth-child(even) td { background: #fafbfc; }
code { font: 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
       background: #eff1f3; padding: 2px 5px; border-radius: 4px; }
.notes { margin-top: 14px; font-size: 13px; color: #59636e; }
.notes p { margin: 2px 0; }
"""


def inline(text):
    """Convert the small subset of inline Markdown used in providers.md to HTML."""
    stash = []

    def keep(s):
        stash.append(s)
        return f"\x00{len(stash) - 1}\x00"

    text = text.replace(r"\*", "\x01")  # escaped asterisk -> literal later
    text = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{html.escape(m.group(1))}</code>"), text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # keep link label, drop URL
    text = text.replace("<br>", "\x02")
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = text.replace("\x02", "<br>").replace("\x01", "*")
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def plain(cell):
    return re.sub(r"[*`\[]|\]\([^)]*\)", "", cell).strip().lower()


def parse(md):
    lines = md.splitlines()
    start = next(n for n, l in enumerate(lines) if l.lstrip().startswith("|"))
    end = start
    while end < len(lines) and lines[end].lstrip().startswith("|"):
        end += 1
    rows = [split_row(l) for l in lines[start:end]]
    notes = [l for l in lines[end:] if l.strip().startswith("*")]
    return rows[0], rows[2:], notes  # rows[1] is the |---| separator


def build_html(header, body, notes):
    th = "".join(f"<th>{inline(c)}</th>" for c in header)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    foot = "".join(f"<p>{inline(n.strip())}</p>" for n in notes)
    return (f"<!doctype html><meta charset='utf-8'><style>{CSS}</style>"
            f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"
            f"<div class='notes'>{foot}</div>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--input", default=str(ROOT / "providers.md"))
    ap.add_argument("-o", "--output", default=str(ROOT / "assets" / "providers-table.png"))
    ap.add_argument("--only", help="comma-separated; keep rows whose first cell contains any of these")
    args = ap.parse_args()

    header, body, notes = parse(Path(args.input).read_text(encoding="utf-8"))
    if args.only:
        wanted = [w.strip().lower() for w in args.only.split(",") if w.strip()]
        body = [r for r in body if any(w in plain(r[0]) for w in wanted)]
        if not body:
            sys.exit("--only matched no rows")

    chrome = next((c for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
                   if shutil.which(c)), None)
    magick = shutil.which("magick") or shutil.which("convert")
    if not chrome or not magick:
        sys.exit("Need Google Chrome/Chromium and ImageMagick on PATH")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "table.html"
        raw = Path(tmp) / "raw.png"
        page.write_text(build_html(header, body, notes), encoding="utf-8")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=1500,2000",
                        f"--screenshot={raw}", page.as_uri()],
                       check=True, capture_output=True)
        # Trim the empty canvas, then add an even white margin.
        subprocess.run([magick, str(raw), "-trim", "+repage", "-bordercolor", "white",
                        "-border", "40", str(out)], check=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()

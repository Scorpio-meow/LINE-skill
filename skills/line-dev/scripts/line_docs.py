#!/usr/bin/env python3
"""line_docs.py - look things up in the LIVE official LINE Developers docs in one or two calls.

Nothing is bundled: pages are fetched from LINE's own Markdown mirror
(https://github.com/line/line-developers-docs-source, synced from developers.line.biz) and cached
for a day. Every result prints the developers.line.biz URL to cite.

Commands
  search PATTERN            regex search across ALL pages (uses a shallow git clone; falls back to the
                            Messaging API reference if git is unavailable)
  Pages come from raw.githubusercontent.com; when that host is blocked, the git clone (github.com) is used.
  section HEADING           print one API-reference section, e.g. "Send push message", "Rich menu object"
  ref --grep PATTERN        grep the API reference, showing the section heading of every hit
  headings [--grep P]       list API-reference section headings (to find the exact section name)
  page PATH [--grep P]      fetch one guide page, e.g. messaging-api/pricing, liff/using-user-profile

Options: --product (messaging-api | liff | liff-server | line-login | line-mini-app | ...; default
messaging-api), --lang (en | ja), --refresh (ignore the cache), --max N (limit hits).

Python 3.8+, standard library only (+ git for `search`, optional).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/line/line-developers-docs-source/main/docs"
REPO = "https://github.com/line/line-developers-docs-source"
SITE = "https://developers.line.biz"
TTL = 24 * 3600


def _setup_stdout():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def cache_dir():
    d = Path(os.environ.get("LINE_DOCS_CACHE") or Path(tempfile.gettempdir()) / "line-docs-cache")
    d.mkdir(parents=True, exist_ok=True)
    return d


def fresh(p, refresh):
    return p.exists() and not refresh and (time.time() - p.stat().st_mtime) < TTL


def not_in_mirror(where):
    sys.exit(f"Not in the docs mirror: {where}\n(Glossary, FAQ and news pages exist only on {SITE}; "
             f"fetch them there with a web tool. Check the path with `search` or the doc map.)")


def fetch_raw(rel, refresh=False):
    """rel like 'en/reference/messaging-api' or 'en/docs/messaging-api/pricing' -> text."""
    target = cache_dir() / "raw" / (rel.replace("/", "__") + ".md")
    if fresh(target, refresh):
        return target.read_text(encoding="utf-8")
    url = f"{RAW}/{rel}/index.html.md"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "line-dev-skill"}),
                                    timeout=60) as r:
            text = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            not_in_mirror(url)
        problem = f"HTTP {e.code} fetching {url}"
    except (urllib.error.URLError, OSError) as e:  # includes socket timeouts
        problem = f"Network error fetching {url}: {getattr(e, 'reason', e)}"
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return text
    # raw.githubusercontent.com unreachable (some sandboxes allow only github.com, e.g. claude.ai's default
    # network allowlist): the same file is in the git mirror.
    clone = ensure_clone(rel.split("/", 1)[0], refresh)
    if clone:
        f = clone / "docs" / rel / "index.html.md"
        if not f.exists():
            not_in_mirror(f"{rel} (looked in the git mirror because: {problem})")
        print(f"({problem}; using the git mirror of the same docs instead)", file=sys.stderr)
        return f.read_text(encoding="utf-8")
    if target.exists():
        age = (time.time() - target.stat().st_mtime) / 86400
        print(f"({problem}; using a cached copy from {age:.0f} day(s) ago - say it may be outdated)",
              file=sys.stderr)
        return target.read_text(encoding="utf-8")
    sys.exit(f"{problem}\nWithout network access, say the answer is unverified, or ask the user to open {SITE}.")


def site_url(rel):
    # en/docs/messaging-api/pricing -> https://developers.line.biz/en/docs/messaging-api/pricing/
    return f"{SITE}/{rel}/"


# --------------------------------------------------------------------------- reference parsing

HEADING = re.compile(r"^(#{2,5}) (.+?)\s*$")


def headings_of(text):
    out = []
    for i, line in enumerate(text.splitlines()):
        m = HEADING.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip().strip("`")))
    return out


def anchor_index(lang, product, clone):
    """Map link text -> anchor using links in the docs themselves (the Markdown has no anchors)."""
    idx = {}
    if not clone:
        return idx
    pat = re.compile(r"\[([^\]]{2,120})\]\(https://developers\.line\.biz/%s/reference/%s/#([a-z0-9-]+)\)"
                     % (lang, re.escape(product)))
    for f in (clone / "docs" / lang).rglob("*.md"):
        try:
            for text, anchor in pat.findall(f.read_text(encoding="utf-8", errors="ignore")):
                idx.setdefault(text.strip().strip("`").lower(), anchor)
        except OSError:
            pass
    return idx


GENERIC = {"response", "request headers", "request body", "path parameters", "query parameters",
           "error response", "rate limit", "example request", "example response", "note", "tip"}


def section_path(heads, i):
    """Nearest '###' title above line i (endpoint / object name) and the nearest sub-heading."""
    top = next(((j, t) for (j, lv, t) in reversed(heads) if j <= i and lv <= 3), (None, ""))
    sub = next((t for (j, lv, t) in reversed(heads) if j <= i), "")
    return top[1], (sub if sub != top[1] else "")


def cite(lang, product, title, anchors):
    a = anchors.get(title.lower()) if title.lower() not in GENERIC else None
    base = f"{SITE}/{lang}/reference/{product}/"
    return f"{base}#{a}" if a else f"{base}  (section: {title})"


# --------------------------------------------------------------------------- git clone for search

def ensure_clone(lang, refresh=False):
    if not shutil.which("git"):
        return None
    d = cache_dir() / "repo"
    stamp = d / ".line-docs-stamp"
    try:
        if not (d / ".git").exists():
            if d.exists():
                shutil.rmtree(d)
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse",
                            REPO, str(d)], check=True, timeout=180, capture_output=True)
            subprocess.run(["git", "-C", str(d), "sparse-checkout", "set", "docs/en", "docs/ja"],
                           check=True, timeout=180, capture_output=True)
            stamp.touch()
        elif refresh or not fresh(stamp, False):
            subprocess.run(["git", "-C", str(d), "pull", "--quiet", "--depth", "1", "--ff-only"],
                           check=False, timeout=180, capture_output=True)
            stamp.touch()
    except (subprocess.SubprocessError, OSError) as e:
        print(f"(git mirror unavailable: {e})", file=sys.stderr)
        return None
    return d if (d / "docs" / lang).exists() else None


def rel_of(path, clone):
    # <clone>/docs/en/docs/messaging-api/pricing/index.html.md -> en/docs/messaging-api/pricing
    return str(path.parent.relative_to(clone / "docs")).replace(os.sep, "/")


# --------------------------------------------------------------------------- commands

def cmd_search(a):
    rx = re.compile(a.pattern, re.I)
    clone = ensure_clone(a.lang, a.refresh)
    hits = 0
    if clone:
        files = sorted((clone / "docs" / a.lang).rglob("index.html.md"))
        # reference pages first, then guides; skip release notes noise unless asked
        files.sort(key=lambda p: (0 if "/reference/" in p.as_posix() else 1, p.as_posix()))
        for f in files:
            if "release-notes" in f.as_posix() and "release" not in a.pattern.lower():
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            matches = [i for i, ln in enumerate(lines) if rx.search(ln)]
            if not matches:
                continue
            rel = rel_of(f, clone)
            heads = headings_of(text)
            print(f"\n== {site_url(rel)}  ({len(matches)} hits)")
            for i in matches[: a.per_page]:
                top, sub = section_path(heads, i)
                h = top + (f" > {sub}" if sub else "")
                print(f"  L{i + 1} [{h}] {lines[i].strip()[:220]}")
                hits += 1
                if hits >= a.max:
                    print(f"\n(stopped at --max {a.max})")
                    return 0
        if not hits:
            print("No hits. Try a broader pattern or English terms used in the docs.")
        return 0
    print(f"(no git mirror: searching only the {a.product} API reference)", file=sys.stderr)
    return cmd_ref(argparse.Namespace(**{**vars(a), "grep": a.pattern, "context": 0}))


def cmd_ref(a):
    rel = f"{a.lang}/reference/{a.product}"
    text = fetch_raw(rel, a.refresh)
    lines = text.splitlines()
    heads = headings_of(text)
    rx = re.compile(a.grep, re.I)
    clone = ensure_clone(a.lang) if not a.no_anchors else None
    anchors = anchor_index(a.lang, a.product, clone)
    shown, last_head = 0, None
    for i, ln in enumerate(lines):
        if not rx.search(ln):
            continue
        top, sub = section_path(heads, i)
        h = top + (f" > {sub}" if sub else "")
        if h != last_head:
            print(f"\n== {h} -> {cite(a.lang, a.product, top, anchors)}")
            last_head = h
        lo, hi = max(0, i - a.context), min(len(lines), i + a.context + 1)
        for k in range(lo, hi):
            print(f"  L{k + 1}: {lines[k].rstrip()[:300]}")
        shown += 1
        if shown >= a.max:
            print(f"\n(stopped at --max {a.max}; narrow the pattern or use `section`)")
            break
    if not shown:
        print(f"No hits in {SITE}/{a.lang}/reference/{a.product}/")
    return 0


def cmd_section(a):
    rel = f"{a.lang}/reference/{a.product}"
    text = fetch_raw(rel, a.refresh)
    lines = text.splitlines()
    heads = headings_of(text)
    want = a.heading.lower().strip()
    cands = [h for h in heads if h[2].lower() == want] or [h for h in heads if h[2].lower().startswith(want)] \
        or [h for h in heads if want in h[2].lower()]
    if not cands:
        print(f"No section matching '{a.heading}'. Try: line_docs.py headings --grep '{a.heading.split()[0]}'")
        return 1
    start, level, title = cands[0]
    end = len(lines)
    for (j, lv, _) in heads:
        if j > start and lv <= level:
            end = j
            break
    clone = ensure_clone(a.lang) if not a.no_anchors else None
    anchors = anchor_index(a.lang, a.product, clone)
    top, _ = section_path(heads, start)
    label = title if top == title else f"{top} > {title}"
    print(f"== {label} -> {cite(a.lang, a.product, top or title, anchors)}")
    if len(cands) > 1:
        print("   (other matches: " + "; ".join(c[2] for c in cands[1:6]) + ")")
    body = [ln for ln in lines[start:end] if not ln.startswith("<!--")]
    if len(body) > a.max_lines:
        print("\n".join(body[: a.max_lines]))
        print(f"\n... ({len(body) - a.max_lines} more lines; use --max-lines or `ref --grep` inside it)")
    else:
        print("\n".join(body))
    return 0


def cmd_headings(a):
    text = fetch_raw(f"{a.lang}/reference/{a.product}", a.refresh)
    rx = re.compile(a.grep, re.I) if a.grep else None
    for (i, lv, t) in headings_of(text):
        if lv <= 3 or rx:
            if rx and not rx.search(t):
                continue
            print(f"{'  ' * (lv - 2)}{t}   (L{i + 1})")
    return 0


def cmd_page(a):
    path = a.path.strip("/")
    path = re.sub(r"^(https?://developers\.line\.biz/)?(en|ja)/(docs/)?", "", path)
    rel = f"{a.lang}/docs/{path}"
    text = fetch_raw(rel, a.refresh)
    print(f"== {site_url(rel)}")
    if a.grep:
        rx = re.compile(a.grep, re.I)
        heads = headings_of(text)
        for i, ln in enumerate(text.splitlines()):
            if rx.search(ln):
                h = next((t for (j, _, t) in reversed(heads) if j <= i), "")
                print(f"  L{i + 1} [{h}] {ln.strip()[:300]}")
    else:
        print("\n".join(ln for ln in text.splitlines() if not ln.startswith("<!--")))
    return 0


def main(argv=None):
    _setup_stdout()
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--lang", default="en", choices=["en", "ja"])
    common.add_argument("--product", default="messaging-api",
                        help="reference product: messaging-api, liff, liff-server, line-login, line-login-v2, "
                             "line-mini-app, line-notification-messages, partner-docs")
    common.add_argument("--refresh", action="store_true", help="ignore the one-day cache")
    common.add_argument("--no-anchors", action="store_true", help="skip the anchor lookup (no git needed)")
    p = argparse.ArgumentParser(prog="line_docs.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", metavar="COMMAND")
    s = sub.add_parser("search", parents=[common], help="regex search across all docs pages")
    s.add_argument("pattern")
    s.add_argument("--max", type=int, default=60)
    s.add_argument("--per-page", type=int, default=6)
    s = sub.add_parser("ref", parents=[common], help="grep the API reference with section headings")
    s.add_argument("--grep", required=True)
    s.add_argument("--context", "-C", type=int, default=1)
    s.add_argument("--max", type=int, default=40)
    s = sub.add_parser("section", parents=[common], help="print one API-reference section")
    s.add_argument("heading")
    s.add_argument("--max-lines", type=int, default=220)
    s = sub.add_parser("headings", parents=[common], help="list API-reference headings")
    s.add_argument("--grep")
    s = sub.add_parser("page", parents=[common], help="fetch a guide page, e.g. messaging-api/pricing")
    s.add_argument("path")
    s.add_argument("--grep")
    a = p.parse_args(argv)
    if not a.cmd:
        p.print_help()
        return 2
    return {"search": cmd_search, "ref": cmd_ref, "section": cmd_section, "headings": cmd_headings,
            "page": cmd_page}[a.cmd](a)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # output piped into `head` etc.
        try:
            sys.stdout = open(os.devnull, "w")
        except OSError:
            pass
        sys.exit(0)

# Security Policy

[繁體中文](/.github/SECURITY.md) | **English** | [日本語](/.github/SECURITY.ja.md) | [ไทย](/.github/SECURITY.th.md) | [Bahasa Indonesia](/.github/SECURITY.id.md) | [한국어](/.github/SECURITY.ko.md)

## Supported versions

Only the latest version, the `main` branch, gets fixes. If you're on an older version, please update first (see the [README](/README.en.md#updating-and-removing) for how).

## Reporting a vulnerability

**Please don't open a public issue.** Use GitHub's private reporting instead: go to the repo's **Security** tab and click **Report a vulnerability**, or open [this link](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new) directly. If that isn't available, email yao921024@gmail.com with `[LINE-skill security]` in the subject.

Please include:

- The affected files and version (commit)
- Steps to reproduce, and what impact it has
- A suggested fix (optional)

Use fake tokens and secrets when reproducing; don't include real values in your report.

## Scope

Vulnerabilities in this project, for example:

- A script prints the channel access token or channel secret, writes it to a file or cache, or sends it to a host other than `api.line.me` and `api-data.line.me`.
- `webhook_tools.py` sends the channel secret itself (it should send only the signature).
- A write command actually runs without `--yes`, bypassing the dry-run.
- Path traversal or command injection, for example `line_docs.py`'s page paths and cache, or `line_api.py`'s `--env-file` and `@file` arguments reading or writing unexpected locations.
- Instructions in `SKILL.md` or `references/` that make the AI assistant perform write operations without the user's consent, leak tokens, or treat fetched doc content as instructions to follow.

Not in scope:

- Vulnerabilities in **the LINE platform itself** (the LINE app, Messaging API, LIFF, LINE Login): report them through LY Corporation's [official channel](https://bugbounty.linecorp.com/).
- Vulnerabilities in **the AI tools themselves** (Claude Code, Codex, Copilot, etc.): report them to the tool's vendor.
- **Your own token leaked**: this isn't a vulnerability in this project. Reissue or revoke the token and secret right away in the [LINE Developers Console](https://developers.line.biz/console/).
- **Gotcha advice that is out of date or not secure enough** but doesn't involve an exploitable vulnerability: a regular issue is fine (the "Outdated LINE info or broken link" template).

## How reports are handled

This is a personally maintained open source project with no fixed response time. After a report comes in, as soon as possible:

1. Receipt is confirmed.
2. The problem and its impact are confirmed, and you may be asked for details if needed.
3. Once fixed, a new version is released, the CHANGELOG is updated, and the issue is disclosed in a GitHub Security Advisory; if you'd like, you'll be credited in it.

Please don't disclose vulnerability details until the fix is released.

## Protecting your own tokens

- Keep tokens and secrets in environment variables or `.env`, and point to it with `--env-file`; don't type them on the command line (they stay in your shell history and the process list).
- Make sure `.env` is listed in `.gitignore`. Some tools generate projects that don't ignore it by default (for example `supabase init`).
- For write operations, check the dry-run output first and add `--yes` only after confirming.
- You can read `SKILL.md` and `scripts/` before installing; the skill runs these scripts on your machine or in the AI tool's execution environment.

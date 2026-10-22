# Security Policy

[繁體中文](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY.md) | **English** | [日本語](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ja.md) | [ไทย](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_th.md) | [Bahasa Indonesia](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_id.md) | [한국어](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ko.md)

## Supported versions

Only the latest version, the `main` branch, gets fixes. If you're on an older version, please update first (see the [README](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/README_en.md#updating-and-removing) for how).

## Reporting a vulnerability

**Do not disclose vulnerability details in public issues, pull requests, or discussions.**

Report privately through one of these channels:

1. **GitHub private reporting (preferred)**: go to the repository's **Security** tab and click **Report a vulnerability**, or open the [private reporting form](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new) directly. Only you and the maintainer can see the report.
2. **Email**: if you can't use GitHub, write to [yao921024@gmail.com](mailto:yao921024@gmail.com) with a subject starting with `[Security] LINE-skill`. Email is not end-to-end encrypted, so start with a short summary and send the details after you get a reply.

Please include as much of the following as you can:

- The affected files and version (commit)
- Steps to reproduce, and what impact it has
- A suggested fix (optional)

Use fake tokens and secrets when reproducing; don't include real values in your report.

## Response process and timelines

This project is maintained by one person and has no bug bounty, but it commits to these timelines:

| Stage | Timeline |
|---|---|
| Acknowledge and first reply | Within 14 days of the report |
| Public disclosure | When the fix is released, and no later than 90 days after the report |

1. **Acknowledge**: confirm receipt and share an initial assessment.
2. **Assess**: confirm whether it is a vulnerability, its impact, and its severity, and ask you for details if needed; if it is not a vulnerability, explain why.
3. **Fix**: discuss the fix with you in a private GitHub security advisory, where you can also submit a fix on a private fork.
4. **Release**: merge the fix into `main`, publish the security advisory, request a CVE ID through GitHub when applicable, and record the fix under Security in the [CHANGELOG](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/CHANGELOG.md).
5. **Credit**: credit you in the advisory if you wish.

Please do not disclose details until the fix is released. If a fix cannot be ready within 90 days, the maintainer will explain why before the deadline and agree on a new disclosure date with you.

## Scope

### In scope

Vulnerabilities in this project, for example:

- A script prints the channel access token or channel secret, writes it to a file or cache, or sends it to a host other than `api.line.me` and `api-data.line.me`.
- `webhook_tools.py` sends the channel secret itself (it should send only the signature).
- A write command actually runs without `--yes`, bypassing the dry-run.
- Path traversal or command injection, for example `line_docs.py`'s page paths and cache, or `line_api.py`'s `--env-file` and `@file` arguments reading or writing unexpected locations.
- Instructions in `SKILL.md` or `references/` that make the AI assistant perform write operations without the user's consent, leak tokens, or treat fetched doc content as instructions to follow.

### Out of scope

- Vulnerabilities in **the LINE platform itself** (the LINE app, Messaging API, LIFF, LINE Login): report them through LY Corporation's [official channel](https://bugbounty.linecorp.com/).
- Vulnerabilities in **the AI tools themselves** (Claude Code, Codex, Copilot, etc.): report them to the tool's vendor.
- **Your own token leaked**: this isn't a vulnerability in this project. Reissue or revoke the token and secret right away in the [LINE Developers Console](https://developers.line.biz/console/).
- **Gotcha advice that is out of date or not secure enough** but doesn't involve an exploitable vulnerability: a regular issue is fine (the "Outdated LINE info or broken link" template).

## Protecting your own tokens

- Keep tokens and secrets in environment variables or `.env`, and point to it with `--env-file`; don't type them on the command line (they stay in your shell history and the process list).
- Make sure `.env` is listed in `.gitignore`. Some tools generate projects that don't ignore it by default (for example `supabase init`).
- For write operations, check the dry-run output first and add `--yes` only after confirming.
- You can read `SKILL.md` and `scripts/` before installing; the skill runs these scripts on your machine or in the AI tool's execution environment.

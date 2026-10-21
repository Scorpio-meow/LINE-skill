# Contributing Guide

[繁體中文](/.github/CONTRIBUTING.md) | **English** | [日本語](/.github/CONTRIBUTING.ja.md) | [ไทย](/.github/CONTRIBUTING.th.md) | [Bahasa Indonesia](/.github/CONTRIBUTING.id.md) | [한국어](/.github/CONTRIBUTING.ko.md)

Thanks for wanting to help! Please follow the [Code of Conduct](/.github/i18n/CODE_OF_CONDUCT.en.md) when taking part in this project.

You can open issues and PRs in any language the README comes in (繁體中文, English, 日本語, ไทย, Bahasa Indonesia, 한국어); replies may be in Traditional Chinese or English.

> This is not an official LY Corporation project. Please report problems with the LINE platform itself (the LINE app, Messaging API, LIFF, LINE Login) to LINE.

## Ways to help

| What you want to do | How |
|---|---|
| Questions about installing or using it, ideas to discuss | Ask in [Discussions](https://github.com/Scorpio-meow/LINE-skill/discussions) |
| LINE specs changed, a doc link is broken, a number in the skill is out of date | Open an "Outdated LINE info or broken link" issue with the official source |
| You hit a gotcha the skill doesn't cover | Open a "Feature request or new gotcha" issue, or send a PR that adds it to `references/gotchas/` |
| A script errors, or the AI follows the skill and still gets it wrong | Open a "Bug report" issue |
| Unclear docs, translation mistakes, accessibility problems | Open the matching issue, or send a PR directly |
| Security vulnerabilities | **Don't open an issue**; report it privately as described in [SECURITY.md](/.github/SECURITY.en.md) |

For larger changes (new script commands, changes to the flow in `SKILL.md`, new gotcha files), please open an issue to discuss first so no work goes to waste.

## Principles of this skill

Please read [`skills/line-dev/SKILL.md`](/skills/line-dev/SKILL.md) before making changes. PRs are reviewed against these points:

1. **No copies of the official docs.** The skill holds only a "topic → official URL" index and a lookup script; specs are always checked live on [LINE Developers](https://developers.line.biz/). Don't paste large chunks of the official docs into the repo; to cite something, give the URL or a section name that `line_docs.py` can find.
2. **Gotcha entries have a fixed format**: **symptom or rule → cause → fix**, followed by `Re-check:` with the official page to verify again (path relative to `https://developers.line.biz/en/`). Mark numbers that may change with "(at the time of writing)", and update the verification year and month at the top of the file.
3. **`SKILL.md` is written for the AI to read**: in English, short and precise, with details in `references/`, one topic per file, so the AI reads only what it needs.
4. **Scripts use only the Python 3.8+ standard library**, with no third-party packages.
5. **Token and secret handling must not be loosened**: they are read only from environment variables or `--env-file`, and never printed or written to files; `line_api.py` only connects to `api.line.me` and `api-data.line.me`, `line_docs.py` only connects to GitHub, and `webhook_tools.py` only calls the URL the user gives it and sends only the signature.
6. **Write operations are dry-run by default**: nothing is actually sent or changed without `--yes`. New write commands must follow this too and be listed under Safety tiers in `SKILL.md`.

## Development setup

```bash
git clone https://github.com/Scorpio-meow/LINE-skill.git
cd LINE-skill
```

To have your AI tool read the version you're editing directly, link the skill folder into the tool's skill folder (remove any installed `line-dev` first). Claude Code is shown here; for other tools' folders, see the [README](/README.en.md#skill-folders-by-tool):

macOS/Linux:

```bash
ln -s "$PWD/skills/line-dev" ~/.claude/skills/line-dev
```

Windows PowerShell (a junction doesn't need administrator rights):

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\line-dev" -Target "$PWD\skills\line-dev"
```

## Checking your changes

There are no automated tests yet, so please run at least the commands below (on Windows, use `python` or `py -3`):

```bash
# All three scripts start (syntax errors show up here)
python3 skills/line-dev/scripts/line_api.py -h
python3 skills/line-dev/scripts/line_docs.py -h
python3 skills/line-dev/scripts/webhook_tools.py -h

# Real operations that need no token
python3 skills/line-dev/scripts/webhook_tools.py sample text
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
```

- **Python 3.8 compatibility**: don't use syntax or functions added in 3.9 or later (e.g. `list[str]` type hints, `str.removeprefix`, `match`). If you have [uv](https://docs.astral.sh/uv/), you can run on 3.8 like this: `uv run --no-project --python 3.8 python skills/line-dev/scripts/line_api.py -h`.
- **Changed webhook-related features**: run `webhook_tools.py selftest <url>` against your local webhook.
- **Changed a write command in `line_api.py`**: confirm that without `--yes` it only prints the request and doesn't actually send it. To test against a real channel, use your own test account.
- **Changed `SKILL.md` or the gotchas in a way that may affect the AI's behavior**: run the relevant scenarios in [`evals/evals.json`](/evals/evals.json) once before and once after the change, grade each against its `expectations`, and put the pass counts in the PR. Any method works; pasting the scenarios into an AI tool and grading by hand is fine. If you add a large new topic, you're welcome to add eval scenarios too.

## Documentation

- [`README.md`](/README.md) (Traditional Chinese) is the primary version. If you change its content, please update the other language versions as well; for languages you don't know, say so in the PR and the maintainer will fill them in.
- Record notable changes under `[Unreleased]` in [`CHANGELOG.md`](/CHANGELOG.md), following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Submitting a pull request

- One PR does one thing; the smaller the change, the easier it is to review.
- Write commit messages in the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format, adding the `line-dev` scope when you change the skill itself, e.g. `fix(line-dev): 擋下 line_docs.py 的路徑穿越` or `docs: 更新評測結果`. The description can be in any language.
- **Never commit real tokens, secrets, userIds or groupIds.** Always use fake values in examples and test material (randomly generated, like `evals/files/richmenu/fake-env.txt`).
- Fill in the PR template with what you did and how you tested it.

## License

Your contributions are released under this project's [MIT License](/LICENSE).

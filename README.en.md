# LINE-skill

[繁體中文](README.md) | **English** | [日本語](README.ja.md) | [ไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [한국어](README.ko.md)

An Agent Skill for AI coding assistants: **`line-dev`**. It makes Claude, Codex, GitHub Copilot, Cursor, Gemini CLI and similar tools more reliable when building, debugging and operating on the LINE platform — Messaging API webhooks, reply/push messages and message quota, Flex Messages, rich menus, group-chat bots, LIFF and LINE Login.

It uses the open [Agent Skills](https://agentskills.io) format (a folder plus a `SKILL.md`), so any tool that supports the format can use it. See [Quick start](#quick-start) to install.

- **Specs are always checked against the live official docs**: the skill ships no copy of the docs, only a "topic → official URL" index and a lookup script. Whenever a number, limit or price matters, the AI looks it up on the spot in the official raw markdown on GitHub (the source developers.line.biz is synced from) and cites the developers.line.biz page.
- **Field-tested gotchas**: verify signatures against the raw body, respond to webhooks within about 2 seconds, reply tokens are single-use and expire quickly, a push to a group is counted per member, unverified accounts can't list group members, how to write and escape textV2 mentions, Flex size and URI limits, rich menu image limits and precedence, LIFF ID token expiry and server-side verification, userIds that differ across providers… Each one is written as "symptom → cause → fix → official page".
- **Operate the LINE API directly**: scripts that use only the Python standard library are included. Write operations are dry-run by default and only run for real when you add `--yes` after confirming; tokens/secrets are read only from environment variables or `.env` and are never printed.

> This is not an official LY Corporation project. LINE is a trademark of LY Corporation.

## Quick start

Install with a single [`skills`](https://github.com/vercel-labs/skills) command; it detects the AI tools on your machine and puts the skill in the matching folders:

```bash
bunx skills add Scorpio-meow/LINE-skill --skill line-dev -g
```

- `-g` installs to your home directory (available in every project); drop `-g` to install into the current project only.
- To install for specific tools only, add `-a`, e.g. `-a claude-code -a codex`; see the [table in the next section](#skill-folders-by-tool) for each tool's value.
- No [Bun](https://bun.sh)? Replace `bunx` with `npx`.

Once installed, it activates automatically when you ask something about LINE development, for example:

> How long until a LINE bot's reply token expires?

If the skill is loaded, the answer checks the official docs first and links to developers.line.biz. The first time a script runs, most tools ask you to allow running commands or network access.

Manual installation for each tool and other install methods are covered in the next section.

## Installation

Requires **Python 3.8 or later** (the scripts use only the standard library; no packages to install). Looking up the official docs needs access to `raw.githubusercontent.com` or `github.com`; operating the LINE API directly needs access to `api.line.me`.

### Skill folders by tool

Manual installation means copying the `line-dev` folder into the skill folder the tool reads, so that `SKILL.md` ends up at `<skill folder>/line-dev/SKILL.md`. The personal folder serves every project on this machine; the project folder sits under the project root and can be committed to share with your team.

| Tool | `-a` value | Personal folder | Project folder | Invoke manually |
|---|---|---|---|---|
| Claude Code | `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/line-dev` |
| OpenAI Codex (CLI, IDE extension, ChatGPT desktop app) | `codex` | `~/.agents/skills/` | `.agents/skills/` | `/skills` or `$line-dev` |
| GitHub Copilot (VS Code, Copilot CLI, JetBrains) | `github-copilot` | `~/.copilot/skills/` | `.github/skills/` | `/line-dev` |
| Cursor | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` | Type `/` in Agent chat and pick it |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` | `.gemini/skills/` | `/skills list` shows whether it loaded |
| Google Antigravity | `antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` | — |
| Devin Desktop (formerly Windsurf) | `devin` | `~/.config/devin/skills/` | `.devin/skills/` | `@line-dev` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | — |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | `/line-dev` |
| Kiro | `kiro-cli` | `~/.kiro/skills/` | `.kiro/skills/` | Type `/` and pick it |
| JetBrains Junie | `junie` | `~/.junie/skills/` | `.junie/skills/` | `/line-dev` or `$line-dev` |
| Roo Code | `roo` | `~/.roo/skills/` | `.roo/skills/` | — |

On Windows, `~` is your user folder (`%USERPROFILE%`). Every tool uses the skill automatically when the conversation calls for it; the "Invoke manually" column only shows how to ask for it explicitly.

- Codex, Copilot, Cursor, Gemini CLI, OpenCode, Devin Desktop, Junie and Roo Code also read `~/.agents/skills/`, so if you use several of them, one copy there is shared by all. Claude Code only reads `~/.claude/skills/`.
- `bunx skills` puts the skill in the shared `.agents/skills/` (`~/.agents/skills/` with `-g`) and creates links for the other tools. If a tool doesn't pick it up afterwards, install it manually into the folder from the table instead.
- Tools not in the table (Amp, Goose, Kilo Code, Trae, Qwen Code, etc.) can also be installed with `bunx skills`; see the [skills README](https://github.com/vercel-labs/skills) for their `-a` values.
- Devin Desktop still reads the Windsurf-era `~/.codeium/windsurf/skills/` and `.windsurf/skills/` as well.

The example below copies to `~/.agents/skills/`; for other tools, set `TARGET` to the path from the table.

macOS/Linux:

```bash
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
TARGET=~/.agents/skills
mkdir -p "$TARGET"
cp -r LINE-skill/skills/line-dev "$TARGET/"
```

Windows PowerShell:

```powershell
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
$TARGET = "$HOME\.agents\skills"
New-Item -ItemType Directory -Force $TARGET | Out-Null
Copy-Item -Recurse -Force LINE-skill\skills\line-dev "$TARGET\"
```

If the tool doesn't detect the new skill, restart it once.

### Other install methods

Some tools have their own install commands:

- **GitHub CLI** (2.90 or later; `gh skill` is currently in public preview): `--agent` takes the same values as `-a` in the table.

  ```bash
  gh skill install Scorpio-meow/LINE-skill line-dev --agent claude-code --scope user
  ```

- **OpenAI Codex**: in Codex, type

  ```text
  $skill-installer install https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev
  ```

  By default Codex runs commands in a sandbox without network access, so it asks for your approval when the scripts look up docs or call the LINE API. To always allow it, add this to `~/.codex/config.toml`:

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

- **GitHub Copilot CLI**: after cloning, run `copilot skill add LINE-skill/skills/line-dev`; if you add it mid-session, load it with `/skills reload`. If you put it in the repo's `.github/skills/` and commit it, the Copilot cloud agent uses it too.
- **Gemini CLI**: installs to user scope by default; add `--scope workspace` to install into the current project only.

  ```bash
  gemini skills install https://github.com/Scorpio-meow/LINE-skill.git --path skills/line-dev
  ```

- **Kiro**: in the Kiro panel, go to **Agent Steering & Skills** → **+** → **Import a skill** → **GitHub**; the URL must point to the subfolder that holds the skill: `https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev`.
- **Devin Desktop**: manage skills from **⋯** → **Skills** at the top right of the Cascade panel.
- **Cline**: new skills are enabled by default; toggle them in the **Skills** tab at the bottom of the Cline panel.

### Claude apps (web/desktop)

1. Turn on code execution: on Pro and Max plans, go to **Settings > Capabilities** and turn on "Code execution and file creation"; on Team and Enterprise plans, an organization owner turns on "Code execution and file creation" and "Skills" in the organization settings.
2. Package `line-dev.zip` yourself. The top level of the ZIP must be the `line-dev/` folder; GitHub's "Download ZIP" gives you the whole repo (top level `LINE-skill-main/`), which can't be uploaded as is, so extract it or clone the repo first, then zip only the `line-dev` folder.
   - macOS/Linux: in the `LINE-skill/skills` folder, run `zip -r ../../line-dev.zip line-dev -x '*.DS_Store'`.
   - Windows: in File Explorer, right-click the `skills\line-dev` folder → "Compress to ZIP file" (on Windows 10, "Send to → Compressed (zipped) folder").
3. Go to **Customize > Skills**, click **+** → **Create skill** → **Upload a skill**, and upload the ZIP. If your interface shows **Settings > Capabilities** instead, click **Upload skill** in the Skills section.

An uploaded skill is available only to your account; making it available to the whole organization requires an organization owner to provision it. The apps' code execution environment usually allows only package managers, `github.com` and a few other domains: when `line_docs.py` can't reach `raw.githubusercontent.com`, it automatically fetches the same docs from `github.com`; `api.line.me`, which `line_api.py` needs, is blocked by default, and on Team and Enterprise plans an organization owner can add allowed domains under Capabilities in the organization settings. To operate the LINE API directly, we recommend Claude Code or a similar tool on your own machine. If the interface changes, follow the [official guide](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

### ChatGPT

According to the [official help article](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), skills in ChatGPT are currently available to eligible users on Business, Enterprise, Healthcare and Edu plans, and workspace settings decide whether uploads are allowed.

1. Get `line-dev.zip` as described in the previous section.
2. In the sidebar, go to **Plugins** → the **Skills** tab, click **Create** → **Upload from your computer**, and upload the ZIP.
3. In a chat, type `@` and pick `line-dev`, or let ChatGPT decide on its own.

ChatGPT and Codex skills don't sync for now, so install it separately if you use Codex. To operate the LINE API directly, we recommend Codex or a similar tool on your own machine.

### Updating and removing

| Install method | Update | Remove |
|---|---|---|
| `bunx skills` | `bunx skills update line-dev` | `bunx skills remove line-dev` |
| `gh skill` | `gh skill update` | Delete the `line-dev` folder |
| Gemini CLI | Remove and reinstall | `gemini skills uninstall line-dev` |
| Manual copy | Run `git pull` in the `LINE-skill` folder, then copy again | Delete the `line-dev` folder |
| Claude apps, ChatGPT | Delete the old one and upload the new ZIP | Delete it on the Skills page |

### Official docs for each tool

If a path or interface changes, the official docs take precedence: [Claude Code](https://code.claude.com/docs/en/skills) · [Claude apps](https://support.claude.com/en/articles/12512180-using-skills-in-claude) · [ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) · [OpenAI Codex](https://learn.chatgpt.com/docs/build-skills) · [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) · [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills) · [Cursor](https://cursor.com/docs/skills) · [Gemini CLI](https://geminicli.com/docs/cli/skills/) · [Google Antigravity](https://antigravity.google/docs/skills) · [Devin Desktop](https://docs.devin.ai/desktop/cascade/skills) · [OpenCode](https://opencode.ai/docs/skills) · [Cline](https://docs.cline.bot/customization/skills) · [Kiro](https://kiro.dev/docs/skills/) · [JetBrains Junie](https://junie.jetbrains.com/docs/agent-skills.html) · [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) · [skills](https://github.com/vercel-labs/skills) · [gh skill](https://cli.github.com/manual/gh_skill_install)

## Using the scripts

The skill calls these scripts on its own; you can also run them directly. They need Python 3.8 or later and no extra packages (on Windows, use `python` or `py -3`).

```bash
# Look up the official docs (fetched live, cached for a day; full-text search when git is available)
python3 skills/line-dev/scripts/line_docs.py search "loading animation"
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
python3 skills/line-dev/scripts/line_docs.py page messaging-api/pricing --grep count

# Messaging API: put the token in an environment variable, or point --env-file at your project's .env
export LINE_CHANNEL_ACCESS_TOKEN=...
python3 skills/line-dev/scripts/line_api.py info                     # bot info
python3 skills/line-dev/scripts/line_api.py quota                    # this month's quota and usage
python3 skills/line-dev/scripts/line_api.py validate push card.json  # validate the message format without sending
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "test"        # dry-run: only shows what would be sent
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "test" --yes  # actually send it
python3 skills/line-dev/scripts/line_api.py richmenu-validate menu.json --image menu.png
python3 skills/line-dev/scripts/line_api.py richmenu-deploy menu.json menu.png --default        # dry-run
python3 skills/line-dev/scripts/line_api.py webhook-test

# Webhook debugging: put the secret in an environment variable
export LINE_CHANNEL_SECRET=...
python3 skills/line-dev/scripts/webhook_tools.py selftest http://localhost:3000/webhook
python3 skills/line-dev/scripts/webhook_tools.py simulate http://localhost:3000/webhook postback --source group
python3 skills/line-dev/scripts/webhook_tools.py sample memberJoined
```

`selftest` sends four requests in order — the Console's Verify (empty `events`), an event with a valid signature, one with a wrong signature, and one with no signature — and checks whether any response exceeds LINE's 2-second timeout.

## Contents

```
skills/line-dev/
├── SKILL.md                      # Main instructions (for the AI, in English)
├── references/
│   ├── doc-map.md                # Official docs index: URL rules, page list, API reference anchors, OpenAPI, status page, deprecation notices
│   └── gotchas/                  # Field-tested gotchas and design patterns, one file per topic; the AI reads only what it needs
│       ├── webhooks-and-hosting.md
│       ├── messaging.md
│       ├── groups-and-mentions.md
│       ├── rich-menus.md
│       ├── liff-and-login.md
│       └── security-and-architecture.md
└── scripts/
    ├── line_docs.py              # Live official docs lookup: full-text search, API reference sections, guide pages (with citable URLs)
    ├── line_api.py               # Messaging API CLI (dry-run first)
    └── webhook_tools.py          # Compute/verify signatures, simulate LINE calling your webhook, one-shot selftest
evals/                            # Test scenarios used to develop this skill
.github/                          # Community docs (contributing, code of conduct, security, accessibility) and issue/PR templates
```

## Safety

- Write actions — push/multicast/broadcast, setting the webhook, publishing, setting as default or deleting a rich menu, making the bot leave a group — only do a dry run without `--yes`: they validate first, then print the full request along with the recipient type, the group's member count (a push to a group is counted per member) and the quota left this month.
- Sent messages automatically carry `X-Line-Retry-Key`, so retrying after a timeout won't send duplicates.
- `line_api.py` only connects to `api.line.me` and `api-data.line.me`, `line_docs.py` only connects to GitHub to fetch docs, and `webhook_tools.py` only calls the URL you give it (it sends the signature, never the secret); tokens/secrets never appear in the output.
- The skill runs scripts on your machine (or in the AI tool's execution environment); you can read `SKILL.md` and `scripts/` before installing.

## Official documentation

Official documentation this skill draws on: [LINE Developers](https://developers.line.biz/) and its markdown source [line/line-developers-docs-source](https://github.com/line/line-developers-docs-source) (whose README explicitly allows use by AI tools). The official docs are updated continuously, so the skill ships only an index, not a copy.

## Testing

`evals/evals.json` holds the 5 test scenarios used to develop this skill — debugging a webhook 401, looking up group-bot specs, publishing a rich menu, LIFF user authentication, and a code review of a group bot — with 49 grading criteria in total. `evals/files/richmenu/` is rich menu material with deliberately planted errors; `fake-env.txt` is a randomly generated fake token: when running scenario 3, copy it into the working folder and rename it to `.env` (the prompt says the token is in `.env`).

Most recent comparison (Claude Opus 5.5, one run per scenario with and without the skill, graded blind): 47/49 with the skill, 44/49 without; 16% faster on average with the skill. The biggest gaps were LIFF (a security warning about deprecated LIFF SDK versions, and re-logging in only when the token has expired) and publishing a rich menu (keeping the token off the command line, confirming before going live). After revising the skill for the two failed criteria, scenarios 1 and 5 were re-run and passed in full, for 49/49 across all five with the skill. The trigger test (10 prompts that should trigger the skill and 10 similar ones that shouldn't, 3 runs each) was judged correctly every time.

## Contributing

Reports of outdated LINE specs, new gotchas, and improvements to the scripts and docs are welcome.

- Workflow, the skill's principles and how to check your changes: [Contributing guide](.github/CONTRIBUTING.en.md)
- [Code of Conduct](.github/i18n/CODE_OF_CONDUCT.en.md)
- Report security vulnerabilities privately as described in the [security policy](.github/SECURITY.en.md); don't open a public issue.
- Accessibility status and known limitations: [Accessibility statement](.github/ACCESSIBILITY.en.md)

## License

[MIT](LICENSE)

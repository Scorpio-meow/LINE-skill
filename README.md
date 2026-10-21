# LINE-skill

**繁體中文** | [English](README.en.md) | [日本語](README.ja.md) | [ไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [한국어](README.ko.md)

給 AI 程式助理用的 Agent Skill：**`line-dev`**。讓 Claude、Codex、GitHub Copilot、Cursor、Gemini CLI 等工具在開發、除錯、操作 LINE 平台時更可靠——Messaging API webhook、reply／push 與訊息額度、Flex Message、圖文選單（Rich Menu）、群組機器人、LIFF、LINE Login。

採用 [Agent Skills](https://agentskills.io) 開放格式（一個資料夾＋`SKILL.md`），支援這個格式的工具都能用，安裝方式見[快速開始](#快速開始)。

- **規格一律即時查官方文件**：skill 不附文件副本，只附「主題 → 官方網址」索引和一支查詢腳本。要用到數字、限制、計價時，AI 會當場去官方 GitHub 原始 markdown（developers.line.biz 的同步來源）查證並附上 developers.line.biz 出處。
- **實戰踩坑清單**：簽章驗證要用 raw body、webhook 要在約 2 秒內回應、reply token 一次性且很快失效、push 到群組按「人數」計、一般帳號列不出群組成員、textV2 mention 的寫法與跳脫、Flex 大小與 URI 限制、圖文選單圖片限制與優先順序、LIFF ID token 過期與後端驗證、provider 不同造成 userId 不一致……每條都是「症狀 → 原因 → 解法 → 官方頁面」。
- **直接操作 LINE API**：附只用 Python 標準函式庫的腳本。寫入類操作預設只做 dry-run，確認後加 `--yes` 才真的執行；token／secret 只從環境變數或 `.env` 讀取，不會印出。

> 本專案不是 LY Corporation 的官方專案。LINE 是 LY Corporation 的商標。

## 快速開始

用 [`skills`](https://github.com/vercel-labs/skills) 指令一行安裝，它會偵測你電腦上的 AI 工具並放到對應的資料夾：

```bash
bunx skills add Scorpio-meow/LINE-skill --skill line-dev -g
```

- `-g` 裝到個人目錄（所有專案都能用）；拿掉 `-g` 則只裝到目前的專案。
- 只裝給特定工具，加上 `-a`，例如 `-a claude-code -a codex`；各工具的值見[下一節的表格](#各工具的-skill-資料夾)。
- 沒有 [Bun](https://bun.sh) 的話，把 `bunx` 換成 `npx` 也可以。

裝好後問一句跟 LINE 開發有關的事就會自動啟用，例如：

> LINE bot 的 reply token 多久會失效？

有載入 skill 的話，回答會先查官方文件並附上 developers.line.biz 的連結。第一次執行腳本時，多數工具會先請你同意執行指令或連網。

各工具的手動安裝和其他安裝方式見下一節。

## 安裝

需要 **Python 3.8 以上**（腳本只用標準函式庫，不用裝套件）。查官方文件要能連 `raw.githubusercontent.com` 或 `github.com`；直接操作 LINE API 要能連 `api.line.me`。

### 各工具的 skill 資料夾

手動安裝就是把 `line-dev` 資料夾複製到工具讀取的 skill 資料夾，讓 `SKILL.md` 落在 `<skill 資料夾>/line-dev/SKILL.md`。個人資料夾給這台電腦上的所有專案用；專案資料夾放在專案根目錄下，可以 commit 給團隊一起用。

| 工具 | `-a` 參數 | 個人資料夾 | 專案資料夾 | 手動叫用 |
|---|---|---|---|---|
| Claude Code | `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/line-dev` |
| OpenAI Codex（CLI、IDE 擴充套件、ChatGPT 桌面版） | `codex` | `~/.agents/skills/` | `.agents/skills/` | `/skills` 或 `$line-dev` |
| GitHub Copilot（VS Code、Copilot CLI、JetBrains） | `github-copilot` | `~/.copilot/skills/` | `.github/skills/` | `/line-dev` |
| Cursor | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` | 在 Agent 對話輸入 `/` 選擇 |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` | `.gemini/skills/` | `/skills list` 可確認是否載入 |
| Google Antigravity | `antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` | — |
| Devin Desktop（原 Windsurf） | `devin` | `~/.config/devin/skills/` | `.devin/skills/` | `@line-dev` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | — |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | `/line-dev` |
| Kiro | `kiro-cli` | `~/.kiro/skills/` | `.kiro/skills/` | 輸入 `/` 選擇 |
| JetBrains Junie | `junie` | `~/.junie/skills/` | `.junie/skills/` | `/line-dev` 或 `$line-dev` |
| Roo Code | `roo` | `~/.roo/skills/` | `.roo/skills/` | — |

`~` 在 Windows 是使用者資料夾（`%USERPROFILE%`）。所有工具都會在對話相關時自動使用 skill，「手動叫用」欄只是指定使用的方式。

- Codex、Copilot、Cursor、Gemini CLI、OpenCode、Devin Desktop、Junie、Roo Code 也會讀 `~/.agents/skills/`，同時用好幾種工具的話，放一份在這裡就能共用。Claude Code 只讀 `~/.claude/skills/`。
- `bunx skills` 會把 skill 放在共用的 `.agents/skills/`（加 `-g` 時是 `~/.agents/skills/`），再替其他工具建立連結。裝完工具沒讀到的話，改用下面的手動安裝，放到表中的資料夾。
- 表上沒有的工具（Amp、Goose、Kilo Code、Trae、Qwen Code 等）也能用 `bunx skills` 安裝，`-a` 的值見 [skills 的說明](https://github.com/vercel-labs/skills)。
- Devin Desktop 也還讀得到 Windsurf 時期的 `~/.codeium/windsurf/skills/` 和 `.windsurf/skills/`。

以複製到 `~/.agents/skills/` 為例，換成其他工具時，把 `TARGET` 改成上表的路徑。

macOS／Linux：

```bash
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
TARGET=~/.agents/skills
mkdir -p "$TARGET"
cp -r LINE-skill/skills/line-dev "$TARGET/"
```

Windows PowerShell：

```powershell
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
$TARGET = "$HOME\.agents\skills"
New-Item -ItemType Directory -Force $TARGET | Out-Null
Copy-Item -Recurse -Force LINE-skill\skills\line-dev "$TARGET\"
```

工具若沒有偵測到新的 skill，重新啟動一次即可。

### 其他安裝方式

有些工具有自己的安裝指令：

- **GitHub CLI**（2.90 以上，`gh skill` 目前是 public preview）：`--agent` 的值和上表的 `-a` 相同。

  ```bash
  gh skill install Scorpio-meow/LINE-skill line-dev --agent claude-code --scope user
  ```

- **OpenAI Codex**：在 Codex 輸入

  ```text
  $skill-installer install https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev
  ```

  Codex 預設在沙箱裡執行指令、不開網路，腳本要查文件或呼叫 LINE API 時會先請你核准。想一律允許，在 `~/.codex/config.toml` 加上：

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

- **GitHub Copilot CLI**：clone 之後執行 `copilot skill add LINE-skill/skills/line-dev`；工作階段中途加入的，用 `/skills reload` 載入。放在 repo 的 `.github/skills/` 並 commit 的話，雲端的 Copilot cloud agent 也會用到。
- **Gemini CLI**：預設裝到個人範圍，加上 `--scope workspace` 只裝到目前專案。

  ```bash
  gemini skills install https://github.com/Scorpio-meow/LINE-skill.git --path skills/line-dev
  ```

- **Kiro**：Kiro 面板的 **Agent Steering & Skills** → **+** → **Import a skill** → **GitHub**，網址要指到 skill 所在的子資料夾：`https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev`。
- **Devin Desktop**：Cascade 面板右上角的 **⋯** → **Skills** 可以管理 skill。
- **Cline**：新的 skill 預設啟用，可以在 Cline 面板底部的 **Skills** 分頁切換。

### Claude 應用程式（網頁版／桌面版）

1. 開啟程式碼執行：Pro、Max 方案到 **Settings > Capabilities** 開啟「Code execution and file creation」；Team、Enterprise 方案由組織擁有者在組織設定裡開啟「Code execution and file creation」和「Skills」。
2. 自己打包 `line-dev.zip`。ZIP 最上層要是 `line-dev/` 資料夾；GitHub 的「Download ZIP」下載的是整個 repo（最上層是 `LINE-skill-main/`），不能直接上傳，要先解壓縮或 clone repo，再只打包 `line-dev` 資料夾。
   - macOS／Linux：在 `LINE-skill/skills` 資料夾執行 `zip -r ../../line-dev.zip line-dev -x '*.DS_Store'`。
   - Windows：在檔案總管對 `skills\line-dev` 資料夾按右鍵 →「壓縮成 ZIP 檔案」（Windows 10 是「傳送到 → 壓縮的 (zipped) 資料夾」）。
3. 到 **Customize > Skills**，按 **+** → **Create skill** → **Upload a skill**，上傳 ZIP。介面如果是 **Settings > Capabilities**，就在 Skills 區塊按 **Upload skill**。

上傳的 skill 只有你的帳號能用，要給整個組織得由組織擁有者佈建。App 的程式碼執行環境通常只開放套件管理器、`github.com` 等少數網域：`line_docs.py` 連不到 `raw.githubusercontent.com` 時會自動改從 `github.com` 取得同一份文件；`line_api.py` 需要的 `api.line.me` 預設連不上，Team、Enterprise 的組織擁有者可以在組織設定的 Capabilities 加入允許的網域。要直接操作 LINE API，建議在自己的電腦上用 Claude Code 等工具。介面如有變動，以[官方說明](https://support.claude.com/en/articles/12512180-using-skills-in-claude)為準。

### ChatGPT

依[官方說明](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)，ChatGPT 的 skill 目前開放給 Business、Enterprise、Healthcare、Edu 方案中符合資格的使用者，能不能上傳由工作區設定決定。

1. 照上一節的方式取得 `line-dev.zip`。
2. 在側邊欄的 **Plugins** → **Skills** 分頁按 **Create** → **Upload from your computer**，上傳 ZIP。
3. 對話中輸入 `@` 選擇 `line-dev`，或讓 ChatGPT 自動判斷。

ChatGPT 和 Codex 的 skill 目前不會同步，用 Codex 的話要另外安裝。直接操作 LINE API 建議在自己的電腦上用 Codex 等工具。

### 更新與移除

| 安裝方式 | 更新 | 移除 |
|---|---|---|
| `bunx skills` | `bunx skills update line-dev` | `bunx skills remove line-dev` |
| `gh skill` | `gh skill update` | 刪除 `line-dev` 資料夾 |
| Gemini CLI | 移除後重新安裝 | `gemini skills uninstall line-dev` |
| 手動複製 | 在 `LINE-skill` 資料夾執行 `git pull`，再複製一次 | 刪除 `line-dev` 資料夾 |
| Claude 應用程式、ChatGPT | 刪掉舊的，再上傳新的 ZIP | 在 Skills 頁面刪除 |

### 各工具官方說明

路徑或介面如有變動，以官方文件為準：[Claude Code](https://code.claude.com/docs/en/skills)・[Claude 應用程式](https://support.claude.com/en/articles/12512180-using-skills-in-claude)・[ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)・[OpenAI Codex](https://learn.chatgpt.com/docs/build-skills)・[GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)・[VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)・[Cursor](https://cursor.com/docs/skills)・[Gemini CLI](https://geminicli.com/docs/cli/skills/)・[Google Antigravity](https://antigravity.google/docs/skills)・[Devin Desktop](https://docs.devin.ai/desktop/cascade/skills)・[OpenCode](https://opencode.ai/docs/skills)・[Cline](https://docs.cline.bot/customization/skills)・[Kiro](https://kiro.dev/docs/skills/)・[JetBrains Junie](https://junie.jetbrains.com/docs/agent-skills.html)・[Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/)・[skills](https://github.com/vercel-labs/skills)・[gh skill](https://cli.github.com/manual/gh_skill_install)

## 腳本快速上手

skill 會自己呼叫這些腳本；你也可以直接用。需要 Python 3.8 以上，不用安裝任何套件（Windows 用 `python` 或 `py -3`）。

```bash
# 查官方文件（即時抓、快取一天；git 可用時支援全文搜尋）
python3 skills/line-dev/scripts/line_docs.py search "loading animation"
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
python3 skills/line-dev/scripts/line_docs.py page messaging-api/pricing --grep count

# Messaging API：token 放環境變數，或用 --env-file 指向專案的 .env
export LINE_CHANNEL_ACCESS_TOKEN=...
python3 skills/line-dev/scripts/line_api.py info                     # bot 資訊
python3 skills/line-dev/scripts/line_api.py quota                    # 本月額度與用量
python3 skills/line-dev/scripts/line_api.py validate push card.json  # 驗證訊息格式，不會送出
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "測試"        # dry-run：只顯示會送什麼
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "測試" --yes  # 真的送出
python3 skills/line-dev/scripts/line_api.py richmenu-validate menu.json --image menu.png
python3 skills/line-dev/scripts/line_api.py richmenu-deploy menu.json menu.png --default        # dry-run
python3 skills/line-dev/scripts/line_api.py webhook-test

# Webhook 除錯：secret 放環境變數
export LINE_CHANNEL_SECRET=...
python3 skills/line-dev/scripts/webhook_tools.py selftest http://localhost:3000/webhook
python3 skills/line-dev/scripts/webhook_tools.py simulate http://localhost:3000/webhook postback --source group
python3 skills/line-dev/scripts/webhook_tools.py sample memberJoined
```

`selftest` 會依序打四個請求：Console 的 Verify（空的 `events`）、一則正確簽章的事件、錯誤簽章、沒有簽章，並且檢查回應有沒有超過 LINE 的 2 秒逾時。

## 內容

```
skills/line-dev/
├── SKILL.md                      # 主說明（給 AI 讀，英文）
├── references/
│   ├── doc-map.md                # 官方文件索引：網址規則、頁面清單、API reference 錨點、OpenAPI、狀態頁、停用公告
│   └── gotchas/                  # 實戰踩坑與設計模式，依主題分檔，AI 只讀用得到的
│       ├── webhooks-and-hosting.md
│       ├── messaging.md
│       ├── groups-and-mentions.md
│       ├── rich-menus.md
│       ├── liff-and-login.md
│       └── security-and-architecture.md
└── scripts/
    ├── line_docs.py              # 即時查官方文件：全文搜尋、抓 API reference 段落、抓指南頁（附可引用網址）
    ├── line_api.py               # Messaging API 操作 CLI（dry-run 優先）
    └── webhook_tools.py          # 簽章計算／驗證、模擬 LINE 打 webhook、一鍵 selftest
evals/                            # 開發這個 skill 用的測試情境
.github/                          # 社群文件（貢獻指南、行為準則、資安政策、無障礙聲明）與 issue／PR 範本
```

## 安全設計

- push／multicast／broadcast、設定 webhook、圖文選單上線／設預設／刪除、讓 bot 離開群組等寫入動作，沒有 `--yes` 就只做 dry-run：先驗證，再印出完整請求，以及收件對象類型、群組人數（push 到群組會按人數計）、本月剩餘額度。
- 送訊息會自動帶 `X-Line-Retry-Key`，逾時重試不會重複送出。
- `line_api.py` 只連 `api.line.me`、`api-data.line.me`，`line_docs.py` 只連 GitHub 抓文件，`webhook_tools.py` 只打你指定的網址（送簽章，不送 secret）；token／secret 不會出現在輸出裡。
- skill 會在你的電腦（或 AI 工具的執行環境）裡執行腳本；安裝前可以先看過 `SKILL.md` 和 `scripts/`。

## 官方文件

本 skill 引用的官方文件來源：[LINE Developers](https://developers.line.biz/)，以及它的 markdown 原始檔 [line/line-developers-docs-source](https://github.com/line/line-developers-docs-source)（README 明文允許給 AI 工具使用）。官方文件持續更新，所以 skill 只放索引，不附副本。

## 測試

`evals/evals.json` 是開發這個 skill 用的 5 個測試情境：webhook 401 除錯、群組 bot 規格查詢、圖文選單上線、LIFF 身分驗證、群組 bot code review，共 49 條評分標準。`evals/files/richmenu/` 是故意埋了錯誤的圖文選單素材；`fake-env.txt` 是隨機產生的假 token，跑第 3 題時複製到工作資料夾並改名成 `.env`（題目說 token 在 `.env` 裡）。

最近一次比較（Claude Opus 5.5，每個情境有／沒有 skill 各跑一次，盲評）：有 skill 通過 47/49、沒 skill 44/49；有 skill 平均快 16%。差距最大的是 LIFF（LIFF SDK 已棄用版本的資安提醒、只在 token 過期時重新登入）與圖文選單上線（token 不放上命令列、上線前先確認）。之後針對沒過的兩條修改 skill，重跑第 1、5 題都全過，五題合計有 skill 49/49。觸發測試（10 句該用、10 句相近但不該用，每句 3 次）全部判斷正確。

## 參與貢獻

歡迎回報過時的 LINE 規格、補充踩坑，或改善腳本與文件。

- 流程、skill 的原則與怎麼檢查改動：[貢獻指南](.github/CONTRIBUTING.md)
- [行為準則](.github/CODE_OF_CONDUCT.md)
- 資安漏洞請照[資安政策](.github/SECURITY.md)私下回報，不要開公開 issue。
- 無障礙狀況與已知限制：[無障礙聲明](.github/ACCESSIBILITY.md)

## 授權

[MIT](LICENSE)

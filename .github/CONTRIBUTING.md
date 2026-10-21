# 貢獻指南

**繁體中文** | [English](/.github/CONTRIBUTING.en.md) | [日本語](/.github/CONTRIBUTING.ja.md) | [ไทย](/.github/CONTRIBUTING.th.md) | [Bahasa Indonesia](/.github/CONTRIBUTING.id.md) | [한국어](/.github/CONTRIBUTING.ko.md)

謝謝你願意幫忙！參與本專案請遵守[行為準則](/.github/CODE_OF_CONDUCT.md)。

用 README 有的任何一種語言（繁體中文、English、日本語、ไทย、Bahasa Indonesia、한국어）開 issue 或 PR 都可以，回覆可能會用繁中或英文。

> 本專案不是 LY Corporation 的官方專案。LINE 平台本身（LINE app、Messaging API、LIFF、LINE Login）的問題請向 LINE 官方回報。

## 可以幫忙的地方

| 想做的事 | 怎麼做 |
|---|---|
| 安裝或使用上的問題、想討論的點子 | 到 [Discussions](https://github.com/Scorpio-meow/LINE-skill/discussions) 發問 |
| LINE 規格改了、文件連結失效、skill 講的數字過時 | 開「LINE 規格過時或連結失效」issue，附官方出處 |
| 踩到 skill 沒寫到的坑 | 開「新功能或新踩坑」issue，或直接發 PR 加進 `references/gotchas/` |
| 腳本出錯、AI 照 skill 做卻做錯 | 開「Bug 回報」issue |
| 文件看不懂、翻譯有誤、無障礙問題 | 開對應的 issue，或直接發 PR |
| 資安漏洞 | **不要開 issue**，照 [SECURITY.md](/.github/SECURITY.md) 私下回報 |

較大的改動（新腳本指令、調整 `SKILL.md` 的流程、新增 gotcha 檔）請先開 issue 討論，避免白做工。

## 這個 skill 的原則

改動前請先讀過 [`skills/line-dev/SKILL.md`](/skills/line-dev/SKILL.md)。PR 會依下面幾點審查：

1. **不附官方文件副本。** skill 只放「主題 → 官方網址」索引和查詢腳本，規格一律即時查 [LINE Developers](https://developers.line.biz/)。不要把官方文件大段貼進 repo；要引用就寫網址，或用 `line_docs.py` 查得到的段落名稱。
2. **踩坑條目的格式固定**：**症狀或規則 → 原因 → 解法**，再用 `Re-check:` 附上要重新查證的官方頁面（路徑相對於 `https://developers.line.biz/en/`）。會變動的數字標上「(at the time of writing)」，並更新檔案開頭的查證年月。
3. **`SKILL.md` 是寫給 AI 讀的**：用英文、短而精確，細節放 `references/`，一個主題一個檔案，讓 AI 只讀用得到的。
4. **腳本只用 Python 3.8 以上的標準函式庫**，不加第三方套件。
5. **token 與 secret 的處理不能放寬**：只從環境變數或 `--env-file` 讀取，不印出、不寫進檔案；`line_api.py` 只連 `api.line.me`、`api-data.line.me`，`line_docs.py` 只連 GitHub，`webhook_tools.py` 只打使用者指定的網址而且只送簽章。
6. **寫入類操作預設 dry-run**：沒有 `--yes` 不能真的送出或改設定。新增寫入類指令也要遵守，並列進 `SKILL.md` 的 Safety tiers。

## 開發環境

```bash
git clone https://github.com/Scorpio-meow/LINE-skill.git
cd LINE-skill
```

想讓 AI 工具直接讀到你正在改的版本，把 skill 資料夾連結到工具的 skill 資料夾（先移除已安裝的 `line-dev`）。以 Claude Code 為例，其他工具的資料夾見 [README](/README.md#各工具的-skill-資料夾)：

macOS／Linux：

```bash
ln -s "$PWD/skills/line-dev" ~/.claude/skills/line-dev
```

Windows PowerShell（junction 不需要系統管理員權限）：

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\line-dev" -Target "$PWD\skills\line-dev"
```

## 檢查改動

目前沒有自動化測試，請至少跑過下面的指令（Windows 用 `python` 或 `py -3`）：

```bash
# 三支腳本都能啟動（語法錯誤會在這裡出現）
python3 skills/line-dev/scripts/line_api.py -h
python3 skills/line-dev/scripts/line_docs.py -h
python3 skills/line-dev/scripts/webhook_tools.py -h

# 不需要 token 的實際操作
python3 skills/line-dev/scripts/webhook_tools.py sample text
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
```

- **Python 3.8 相容**：不要用 3.9 之後才有的語法或函式（例如 `list[str]` 型別標註、`str.removeprefix`、`match`）。有 [uv](https://docs.astral.sh/uv/) 的話可以這樣用 3.8 跑：`uv run --no-project --python 3.8 python skills/line-dev/scripts/line_api.py -h`。
- **改了 webhook 相關功能**：對本機的 webhook 跑 `webhook_tools.py selftest <url>`。
- **改了 `line_api.py` 的寫入類指令**：確認沒加 `--yes` 時只印出請求，不會真的送出。要對真的 channel 測試，請用自己的測試帳號。
- **改了 `SKILL.md` 或 gotchas、可能影響 AI 的行為**：用 [`evals/evals.json`](/evals/evals.json) 裡相關的題目，在改動前後各跑一次，對照每題的 `expectations` 評分，把通過數寫在 PR 裡。方法不限，在 AI 工具裡貼題目、人工對照評分也可以。新增一大塊主題時，歡迎一併新增評測題目。

## 文件

- [`README.md`](/README.md)（繁中）是主要版本。改了它的內容，請一併更新其他語言版本；不會的語言就在 PR 裡註明，由維護者補上。
- 值得注意的改動請記在 [`CHANGELOG.md`](/CHANGELOG.md) 的 `[Unreleased]`，格式依 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)。

## 提交 Pull Request

- 一個 PR 只做一件事，改動越小越好審查。
- commit 訊息用 [Conventional Commits](https://www.conventionalcommits.org/zh-hant/v1.0.0/) 格式，改 skill 本身時加上 `line-dev` 範圍，例如 `fix(line-dev): 擋下 line_docs.py 的路徑穿越`、`docs: 更新評測結果`。說明用哪種語言都可以。
- **絕對不要 commit 真的 token、secret、userId 或 groupId。** 範例和測試素材一律用假值（像 `evals/files/richmenu/fake-env.txt` 那樣隨機產生）。
- 照 PR 範本填寫做了什麼、怎麼測的。

## 授權

你提交的貢獻會以本專案的 [MIT 授權](/LICENSE)釋出。

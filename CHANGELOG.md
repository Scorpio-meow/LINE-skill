# 更新日誌

這個專案所有值得注意的變更都會記錄在這裡。格式依循 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，版本號遵守[語意化版本](https://semver.org/lang/zh-TW/)。

## [Unreleased]

### Added

- `line-dev` skill（[Agent Skills](https://agentskills.io) 格式）：`SKILL.md`、官方文件索引 `references/doc-map.md`，以及六個主題的實戰踩坑清單（webhook 與部署、訊息、群組與 mention、圖文選單、LIFF 與 LINE Login、資安與架構）。
- `line_docs.py`：即時查 LINE 官方文件（全文搜尋、API reference 段落、指南頁），結果附 developers.line.biz 網址，快取一天；連不到 `raw.githubusercontent.com` 時改用 `github.com` 的 git 鏡像，兩邊都失敗時改用過期的快取並標註。
- `line_api.py`：Messaging API 操作 CLI。寫入指令沒有 `--yes` 只做 dry-run，送訊息自動帶 `X-Line-Retry-Key`，token 只送到 `api.line.me`、`api-data.line.me`。
- `webhook_tools.py`：簽章計算與驗證、範例事件、模擬 LINE 打 webhook、一鍵 `selftest`。
- 社群文件：貢獻指南、行為準則、資安政策、無障礙聲明（繁中、英、日、泰、印尼、韓文），以及 issue 與 PR 範本。
- README 六語版新增「參與貢獻」段落，「內容」目錄樹補上 `.github/`。
- `llms.txt`：給 AI 助理和爬蟲讀的專案索引，指向 SKILL.md、references、腳本、README 和評測資料。

### Removed

- README 與資安政策裡指向 GitHub Releases 的說明：目前沒有發布 Release，Claude 應用程式改為自己打包 `line-dev.zip`。

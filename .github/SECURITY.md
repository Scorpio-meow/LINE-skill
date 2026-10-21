# 資安政策

**繁體中文** | [English](/.github/SECURITY.en.md) | [日本語](/.github/SECURITY.ja.md) | [ไทย](/.github/SECURITY.th.md) | [Bahasa Indonesia](/.github/SECURITY.id.md) | [한국어](/.github/SECURITY.ko.md)

## 支援的版本

只修正最新版，也就是 `main` 分支。用舊版的話請先更新（更新方式見 [README](/README.md#更新與移除)）。

## 回報漏洞

**請不要開公開的 issue。** 請用 GitHub 的私下回報：到 repo 的 **Security** 分頁按 **Report a vulnerability**，或直接開啟[這個連結](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new)。無法使用時，寄信到 yao921024@gmail.com，主旨加上 `[LINE-skill security]`。

請附上：

- 受影響的檔案與版本（commit）
- 重現步驟，以及會造成什麼影響
- 建議的修法（可選）

重現時請用假的 token 和 secret，不要在回報裡附真的值。

## 範圍

屬於本專案的漏洞，例如：

- 腳本把 channel access token 或 channel secret 印出來、寫進檔案或快取，或送到 `api.line.me`、`api-data.line.me` 以外的主機。
- `webhook_tools.py` 把 channel secret 本身送出去（它只該送簽章）。
- 寫入類指令在沒有 `--yes` 的情況下真的執行，繞過 dry-run。
- 路徑穿越或指令注入，例如 `line_docs.py` 的頁面路徑與快取，或 `line_api.py` 的 `--env-file`、`@file` 參數讀寫到預期外的位置。
- `SKILL.md` 或 `references/` 的指示讓 AI 助理在使用者沒同意的情況下執行寫入操作、洩漏 token，或把查到的文件內容當成指令執行。

不屬於本專案的：

- **LINE 平台本身**（LINE app、Messaging API、LIFF、LINE Login）的漏洞：請依 LY Corporation 的[官方管道](https://bugbounty.linecorp.com/)回報。
- **AI 工具本身**（Claude Code、Codex、Copilot 等）的漏洞：請回報給該工具的開發商。
- **你自己的 token 外洩了**：這不是本專案的漏洞。請立刻到 [LINE Developers Console](https://developers.line.biz/console/) 重新發行或撤銷 token、secret。
- **gotchas 的建議過時或不夠安全**，但不涉及可被利用的漏洞：開一般 issue 即可（「LINE 規格過時或連結失效」範本）。

## 處理流程

這是個人維護的開源專案，沒有固定的回應時限，收到後會盡快：

1. 確認收到。
2. 確認問題與影響範圍，必要時向你詢問細節。
3. 修正後發布新版本、更新 CHANGELOG，並用 GitHub Security Advisory 公開說明；你願意的話，會在公告中致謝。

修正發布前，請不要公開漏洞細節。

## 使用時保護自己的 token

- token 和 secret 放在環境變數或 `.env`，用 `--env-file` 指定；不要打在命令列上（會留在 shell 歷史與程序列表）。
- 確認 `.env` 有列在 `.gitignore`。有些工具產生的專案預設不會忽略它（例如 `supabase init`）。
- 寫入類操作先看過 dry-run 的輸出，確認後才加 `--yes`。
- 安裝前可以先看過 `SKILL.md` 和 `scripts/`，skill 會在你的電腦或 AI 工具的執行環境裡執行這些腳本。

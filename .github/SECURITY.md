# 安全政策

**繁體中文** | [English](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_en.md) | [日本語](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ja.md) | [ไทย](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_th.md) | [Bahasa Indonesia](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_id.md) | [한국어](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ko.md)

## 支援的版本

只修正最新版，也就是 `main` 分支。用舊版的話請先更新（更新方式見 [README](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/README.md#更新與移除)）。

## 回報漏洞

**請不要在公開的 Issue、Pull Request 或討論區揭露漏洞細節。**

請擇一管道私下回報：

1. **GitHub 私下回報（建議）**：到本專案的 **Security** 分頁按 **Report a vulnerability**，或直接開啟[私下回報表單](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new)。內容只有你和維護者看得到。
2. **電子郵件**：無法使用 GitHub 時，寄到 [yao921024@gmail.com](mailto:yao921024@gmail.com)，主旨開頭加上 `[Security] LINE-skill`。電子郵件不是端對端加密，信裡先簡述問題就好，細節等收到回覆後再提供。

回報時請盡量附上：

- 受影響的檔案與版本（commit）
- 重現步驟，以及會造成什麼影響
- 建議的修法（選填）

重現時請用假的 token 和 secret，不要在回報裡附真的值。

## 處理流程與時限

本專案由個人維護，沒有漏洞獎勵，但會遵守以下時限：

| 階段 | 時限 |
|---|---|
| 確認收到並首次回覆 | 收到回報後 14 天內 |
| 公開漏洞細節 | 修正發布時，最晚在回報後 90 天 |

1. **確認收到**：回覆已收到，並說明初步評估。
2. **評估**：確認是否屬於漏洞、影響範圍與嚴重程度，必要時向你詢問細節；不屬於漏洞時會說明原因。
3. **修正**：在私下的 GitHub Security Advisory 中與你討論修正方式，你也可以在其中的私人分支提交修正。
4. **發布**：把修正合併到 `main`、公開 Security Advisory，適用時透過 GitHub 申請 CVE 編號，並在 [CHANGELOG](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/CHANGELOG.md) 的 Security 分類記錄。
5. **致謝**：你願意的話，會在 Advisory 中列名致謝。

修正發布前請不要公開漏洞細節。90 天內來不及修正時，會在期限前向你說明原因，並協商新的公開日期。

## 範圍

### 範圍內

屬於本專案的漏洞，例如：

- 腳本把 channel access token 或 channel secret 印出來、寫進檔案或快取，或送到 `api.line.me`、`api-data.line.me` 以外的主機。
- `webhook_tools.py` 把 channel secret 本身送出去（它只該送簽章）。
- 寫入類指令在沒有 `--yes` 的情況下真的執行，繞過 dry-run。
- 路徑穿越或指令注入，例如 `line_docs.py` 的頁面路徑與快取，或 `line_api.py` 的 `--env-file`、`@file` 參數讀寫到預期外的位置。
- `SKILL.md` 或 `references/` 的指示讓 AI 助理在使用者沒同意的情況下執行寫入操作、洩漏 token，或把查到的文件內容當成指令執行。

### 不在範圍內

- **LINE 平台本身**（LINE app、Messaging API、LIFF、LINE Login）的漏洞：請依 LY Corporation 的[官方管道](https://bugbounty.linecorp.com/)回報。
- **AI 工具本身**（Claude Code、Codex、Copilot 等）的漏洞：請回報給該工具的開發商。
- **你自己的 token 外洩了**：這不是本專案的漏洞。請立刻到 [LINE Developers Console](https://developers.line.biz/console/) 重新發行或撤銷 token、secret。
- **gotchas 的建議過時或不夠安全**，但不涉及可被利用的漏洞：開一般 issue 即可（「LINE 規格過時或連結失效」範本）。

## 使用時保護自己的 token

- token 和 secret 放在環境變數或 `.env`，用 `--env-file` 指定；不要打在命令列上（會留在 shell 歷史與程序列表）。
- 確認 `.env` 有列在 `.gitignore`。有些工具產生的專案預設不會忽略它（例如 `supabase init`）。
- 寫入類操作先看過 dry-run 的輸出，確認後才加 `--yes`。
- 安裝前可以先看過 `SKILL.md` 和 `scripts/`，skill 會在你的電腦或 AI 工具的執行環境裡執行這些腳本。

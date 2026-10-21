# 無障礙聲明

**繁體中文** | [English](/.github/ACCESSIBILITY.en.md) | [日本語](/.github/ACCESSIBILITY.ja.md) | [ไทย](/.github/ACCESSIBILITY.th.md) | [Bahasa Indonesia](/.github/ACCESSIBILITY.id.md) | [한국어](/.github/ACCESSIBILITY.ko.md)

## 我們的承諾

希望使用螢幕閱讀器、螢幕放大、只用鍵盤或語音輸入的開發者，以及使用不同語言的開發者，都能安裝、閱讀、使用這個 skill，也能參與貢獻。

## 專案的形式

本專案沒有網頁或圖形介面，內容是：

- Markdown 文件：六種語言的 README、`SKILL.md`、`references/`
- 三支命令列 Python 腳本
- 開發用的評測素材

你會透過自己的 AI 工具和終端機使用它，所以那些工具本身的無障礙程度也會影響使用經驗。

## 目前做到的

- 腳本只輸出純文字，不用顏色、游標控制或動畫表達資訊；所有操作都能只用鍵盤在命令列完成。
- 腳本把標準輸出設為 UTF-8，減少 Windows 主控台顯示中、日、泰、韓文時的亂碼。
- 文件用 Markdown 標題分段，可以用螢幕閱讀器的標題導覽跳到需要的段落。
- README 提供繁體中文、English、日本語、ไทย、Bahasa Indonesia、한국어 六種語言。
- 幫你開發 LINE bot 時，skill 會提醒 Flex Message 等訊息要寫 `altText`：它會出現在通知、聊天列表與引用預覽裡。

## 已知限制

- README「各工具的 skill 資料夾」是 5 欄 12 列的表格，在螢幕閱讀器或窄螢幕上不好讀。
- README「內容」一節用框線字元（`├──`、`└──`）畫目錄樹，螢幕閱讀器可能會逐一唸出這些符號。
- `SKILL.md` 和 `references/` 只有英文（主要給 AI 讀）；腳本的訊息與 `-h` 說明也只有英文。
- 繁中以外的 README 是翻譯版本，更新可能比較晚；內容不一致時以[繁中版](/README.md)為準。
- Claude、ChatGPT、Codex 等工具的安裝介面由各家廠商提供，無障礙程度不在本專案的控制範圍內。
- 我們還沒有用特定的螢幕閱讀器做過系統性的測試。

## 支援的環境

- macOS、Linux、Windows（PowerShell、Windows Terminal），Python 3.8 以上。
- 任何能顯示 UTF-8 文字的終端機。
- 文件可以在 GitHub 網頁或任何 Markdown 檢視器閱讀，也可以直接用純文字編輯器開啟。

## 回報障礙

[開一個「無障礙問題」issue](https://github.com/Scorpio-meow/LINE-skill/issues/new?template=accessibility.yml)，說明在哪裡遇到、使用的輔助科技與環境、遇到什麼困難。不方便公開的話，可以寄信到 yao921024@gmail.com。這是個人維護的專案，沒有固定的回應時限，但每一則回報都會認真看。

也歡迎建議 skill 在幫你開發 LINE bot 時，還應該提醒哪些無障礙事項。

最後更新：2026-10-21

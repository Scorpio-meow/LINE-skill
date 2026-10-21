## 說明 / Summary

<!-- 做了什麼、為什麼。相關 issue 寫 "Closes #123"。/ What and why. Link issues with "Closes #123". -->

## 類型 / Type

- [ ] 修正 bug / Bug fix
- [ ] 新功能（腳本指令、選項）/ Feature
- [ ] LINE 規格更新或新踩坑（`references/`）/ LINE spec update or new gotcha
- [ ] `SKILL.md`（AI 的行為）/ AI behaviour
- [ ] 文件或翻譯 / Docs or translation

## 怎麼測的 / How was this tested

<!-- 跑了哪些指令；改了 SKILL.md 或 gotchas 的話，評測前後各通過幾條。/ Commands you ran; eval results before/after for SKILL.md or gotcha changes. -->

## 檢查 / Checklist

- [ ] 沒有 commit 真的 token、secret、userId 或 groupId / No real tokens, secrets, user IDs or group IDs
- [ ] 腳本仍只用 Python 3.8+ 標準函式庫，寫入類操作仍預設 dry-run / Scripts stay stdlib-only on Python 3.8+, writes stay dry-run by default
- [ ] 新增或修改的 LINE 規格都附官方出處，會變動的數字標上查證時間 / New or changed LINE facts cite official docs; volatile numbers are dated
- [ ] 已更新 `CHANGELOG.md` 的 `[Unreleased]`（如果需要）/ Updated `CHANGELOG.md` if needed
- [ ] 改了 `README.md` 的話，已同步其他語言版本，或在上面註明需要翻譯 / Synced README translations, or noted that they need updating

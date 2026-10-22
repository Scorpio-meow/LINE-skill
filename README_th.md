# LINE-skill

[繁體中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | **ไทย** | [Bahasa Indonesia](README_id.md) | [한국어](README_ko.md)

Agent Skill สำหรับผู้ช่วยเขียนโค้ด AI: **`line-dev`** ช่วยให้ Claude, Codex, GitHub Copilot, Cursor, Gemini CLI และเครื่องมืออื่น ๆ ทำงานกับแพลตฟอร์ม LINE ได้แม่นยำขึ้น ทั้งการพัฒนา การดีบัก และการใช้งานจริง ครอบคลุม webhook ของ Messaging API, ข้อความ reply/push และโควตาข้อความ, Flex Message, ริชเมนู (Rich Menu), บอทในแชทกลุ่ม, LIFF และ LINE Login

ใช้รูปแบบเปิด [Agent Skills](https://agentskills.io) (โฟลเดอร์หนึ่งโฟลเดอร์พร้อมไฟล์ `SKILL.md`) เครื่องมือใดที่รองรับรูปแบบนี้ก็ใช้ได้ ดูวิธีติดตั้งได้ที่[เริ่มต้นอย่างรวดเร็ว](#เริ่มต้นอย่างรวดเร็ว)

- **ตรวจสเปกกับเอกสารทางการแบบเรียลไทม์เสมอ**: skill นี้ไม่ได้แนบสำเนาเอกสารมาด้วย มีเพียงดัชนี "หัวข้อ → URL ทางการ" และสคริปต์สำหรับค้นหา เมื่อต้องใช้ตัวเลข ข้อจำกัด หรือราคา AI จะค้นจากไฟล์ markdown ต้นฉบับทางการบน GitHub (แหล่งที่ developers.line.biz ซิงก์มา) ทันที และแนบแหล่งอ้างอิงจาก developers.line.biz
- **รายการกับดักจากการใช้งานจริง**: ต้องตรวจลายเซ็นด้วย raw body, ต้องตอบ webhook ภายในประมาณ 2 วินาที, reply token ใช้ได้ครั้งเดียวและหมดอายุเร็ว, การ push เข้ากลุ่มนับตามจำนวนสมาชิก, บัญชีที่ยังไม่ผ่านการยืนยันดึงรายชื่อสมาชิกกลุ่มไม่ได้, วิธีเขียนและ escape การ mention ใน textV2, ข้อจำกัดขนาดและ URI ของ Flex, ข้อจำกัดรูปภาพและลำดับความสำคัญของริชเมนู, การหมดอายุของ ID token ใน LIFF และการตรวจสอบฝั่งเซิร์ฟเวอร์, userId ไม่ตรงกันเมื่อต่าง provider… ทุกข้อเขียนในรูปแบบ "อาการ → สาเหตุ → วิธีแก้ → หน้าเอกสารทางการ"
- **เรียกใช้ LINE API ได้โดยตรง**: มีสคริปต์ที่ใช้เพียงไลบรารีมาตรฐานของ Python คำสั่งที่เขียนข้อมูลจะทำแค่ dry-run เป็นค่าเริ่มต้น และจะทำงานจริงเมื่อยืนยันแล้วเติม `--yes` เท่านั้น token/secret อ่านจากตัวแปรสภาพแวดล้อมหรือ `.env` เท่านั้น และจะไม่ถูกพิมพ์ออกมา

> โปรเจกต์นี้ไม่ใช่โปรเจกต์อย่างเป็นทางการของ LY Corporation และ LINE เป็นเครื่องหมายการค้าของ LY Corporation

## เริ่มต้นอย่างรวดเร็ว

ติดตั้งได้ด้วยคำสั่ง [`skills`](https://github.com/vercel-labs/skills) เพียงบรรทัดเดียว คำสั่งนี้จะตรวจหาเครื่องมือ AI ในเครื่องของคุณแล้ววาง skill ไว้ในโฟลเดอร์ที่ตรงกัน:

```bash
bunx skills add Scorpio-meow/LINE-skill --skill line-dev -g
```

- `-g` ติดตั้งไว้ในโฮมไดเรกทอรี (ใช้ได้ทุกโปรเจกต์) ถ้าไม่ใส่ `-g` จะติดตั้งเฉพาะโปรเจกต์ปัจจุบัน
- ถ้าต้องการติดตั้งให้เฉพาะบางเครื่องมือ ให้เพิ่ม `-a` เช่น `-a claude-code -a codex` ดูค่าของแต่ละเครื่องมือได้จาก[ตารางในหัวข้อถัดไป](#โฟลเดอร์-skill-ของแต่ละเครื่องมือ)
- ถ้าไม่มี [Bun](https://bun.sh) ให้เปลี่ยน `bunx` เป็น `npx` ได้

หลังติดตั้งแล้ว skill จะทำงานโดยอัตโนมัติเมื่อถามเรื่องการพัฒนาบน LINE เช่น:

> reply token ของ LINE bot หมดอายุภายในเวลาเท่าไร?

ถ้าโหลด skill แล้ว คำตอบจะตรวจสอบกับเอกสารทางการก่อนและแนบลิงก์ developers.line.biz มาด้วย ครั้งแรกที่รันสคริปต์ เครื่องมือส่วนใหญ่จะขออนุญาตรันคำสั่งหรือเชื่อมต่อเครือข่ายก่อน

วิธีติดตั้งแบบแมนนวลสำหรับแต่ละเครื่องมือและวิธีอื่น ๆ อยู่ในหัวข้อถัดไป

## การติดตั้ง

ต้องใช้ **Python 3.8 ขึ้นไป** (สคริปต์ใช้แค่ไลบรารีมาตรฐาน ไม่ต้องติดตั้งแพ็กเกจเพิ่ม) การค้นเอกสารทางการต้องเชื่อมต่อ `raw.githubusercontent.com` หรือ `github.com` ได้ ส่วนการเรียก LINE API โดยตรงต้องเชื่อมต่อ `api.line.me` ได้

### โฟลเดอร์ skill ของแต่ละเครื่องมือ

การติดตั้งแบบแมนนวลคือการคัดลอกโฟลเดอร์ `line-dev` ไปไว้ในโฟลเดอร์ skill ที่เครื่องมืออ่าน ให้ `SKILL.md` อยู่ที่ `<โฟลเดอร์ skill>/line-dev/SKILL.md` โฟลเดอร์ส่วนตัวใช้ได้กับทุกโปรเจกต์ในเครื่องนี้ ส่วนโฟลเดอร์โปรเจกต์อยู่ใต้รูทของโปรเจกต์ และ commit เพื่อแชร์ให้ทีมใช้ร่วมกันได้

| เครื่องมือ | ค่า `-a` | โฟลเดอร์ส่วนตัว | โฟลเดอร์โปรเจกต์ | เรียกใช้เอง |
|---|---|---|---|---|
| Claude Code | `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/line-dev` |
| OpenAI Codex (CLI, ส่วนขยาย IDE, แอป ChatGPT บนเดสก์ท็อป) | `codex` | `~/.agents/skills/` | `.agents/skills/` | `/skills` หรือ `$line-dev` |
| GitHub Copilot (VS Code, Copilot CLI, JetBrains) | `github-copilot` | `~/.copilot/skills/` | `.github/skills/` | `/line-dev` |
| Cursor | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` | พิมพ์ `/` ในแชท Agent แล้วเลือก |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` | `.gemini/skills/` | ใช้ `/skills list` ตรวจว่าโหลดแล้วหรือยัง |
| Google Antigravity | `antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` | — |
| Devin Desktop (เดิมคือ Windsurf) | `devin` | `~/.config/devin/skills/` | `.devin/skills/` | `@line-dev` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | — |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | `/line-dev` |
| Kiro | `kiro-cli` | `~/.kiro/skills/` | `.kiro/skills/` | พิมพ์ `/` แล้วเลือก |
| JetBrains Junie | `junie` | `~/.junie/skills/` | `.junie/skills/` | `/line-dev` หรือ `$line-dev` |
| Roo Code | `roo` | `~/.roo/skills/` | `.roo/skills/` | — |

บน Windows `~` คือโฟลเดอร์ผู้ใช้ (`%USERPROFILE%`) ทุกเครื่องมือจะใช้ skill โดยอัตโนมัติเมื่อบทสนทนาเกี่ยวข้อง คอลัมน์ "เรียกใช้เอง" เป็นเพียงวิธีระบุให้ใช้อย่างชัดเจน

- Codex, Copilot, Cursor, Gemini CLI, OpenCode, Devin Desktop, Junie และ Roo Code อ่าน `~/.agents/skills/` ด้วย ถ้าใช้หลายเครื่องมือ วางไว้ที่นี่ชุดเดียวก็ใช้ร่วมกันได้ ส่วน Claude Code อ่านแค่ `~/.claude/skills/`
- `bunx skills` จะวาง skill ไว้ที่ `.agents/skills/` ซึ่งใช้ร่วมกัน (ถ้าใส่ `-g` คือ `~/.agents/skills/`) แล้วสร้างลิงก์ให้เครื่องมืออื่น ถ้าติดตั้งแล้วเครื่องมือยังไม่เห็น ให้ติดตั้งแบบแมนนวลตามด้านล่างไปยังโฟลเดอร์ในตาราง
- เครื่องมือที่ไม่อยู่ในตาราง (Amp, Goose, Kilo Code, Trae, Qwen Code ฯลฯ) ก็ติดตั้งด้วย `bunx skills` ได้ ดูค่า `-a` ได้ที่ [README ของ skills](https://github.com/vercel-labs/skills)
- Devin Desktop ยังอ่าน `~/.codeium/windsurf/skills/` และ `.windsurf/skills/` จากยุค Windsurf ได้อยู่

ตัวอย่างด้านล่างคัดลอกไปที่ `~/.agents/skills/` ถ้าใช้เครื่องมืออื่น ให้เปลี่ยน `TARGET` เป็นพาธในตาราง

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

ถ้าเครื่องมือไม่เห็น skill ใหม่ ให้รีสตาร์ตหนึ่งครั้ง

### วิธีติดตั้งอื่น ๆ

บางเครื่องมือมีคำสั่งติดตั้งของตัวเอง:

- **GitHub CLI** (2.90 ขึ้นไป ขณะนี้ `gh skill` ยังเป็น public preview): ค่าของ `--agent` เหมือนกับ `-a` ในตาราง

  ```bash
  gh skill install Scorpio-meow/LINE-skill line-dev --agent claude-code --scope user
  ```

- **OpenAI Codex**: พิมพ์ใน Codex ว่า

  ```text
  $skill-installer install https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev
  ```

  โดยค่าเริ่มต้น Codex รันคำสั่งใน sandbox ที่ไม่มีเครือข่าย จึงจะขออนุมัติเมื่อสคริปต์ค้นเอกสารหรือเรียก LINE API ถ้าต้องการอนุญาตตลอด ให้เพิ่มใน `~/.codex/config.toml`:

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

- **GitHub Copilot CLI**: หลัง clone ให้รัน `copilot skill add LINE-skill/skills/line-dev` ถ้าเพิ่มระหว่างเซสชัน ให้โหลดด้วย `/skills reload` ถ้าวางไว้ใน `.github/skills/` ของ repo แล้ว commit ตัว Copilot cloud agent บนคลาวด์ก็จะใช้ด้วย
- **Gemini CLI**: ค่าเริ่มต้นติดตั้งในขอบเขตผู้ใช้ เพิ่ม `--scope workspace` เพื่อติดตั้งเฉพาะโปรเจกต์ปัจจุบัน

  ```bash
  gemini skills install https://github.com/Scorpio-meow/LINE-skill.git --path skills/line-dev
  ```

- **Kiro**: ในแผง Kiro ไปที่ **Agent Steering & Skills** → **+** → **Import a skill** → **GitHub** โดย URL ต้องชี้ไปยังโฟลเดอร์ย่อยที่มี skill: `https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev`
- **Devin Desktop**: จัดการ skill ได้จาก **⋯** → **Skills** ที่มุมขวาบนของแผง Cascade
- **Cline**: skill ใหม่เปิดใช้งานเป็นค่าเริ่มต้น สลับเปิด/ปิดได้ในแท็บ **Skills** ด้านล่างของแผง Cline

### แอป Claude (เว็บ/เดสก์ท็อป)

1. เปิดการรันโค้ด: แผน Pro และ Max ไปที่ **Settings > Capabilities** แล้วเปิด "Code execution and file creation" ส่วนแผน Team และ Enterprise เจ้าของ (owner) องค์กรต้องเปิด "Code execution and file creation" และ "Skills" ในการตั้งค่าองค์กร
2. บีบอัด `line-dev.zip` เอง ชั้นบนสุดของ ZIP ต้องเป็นโฟลเดอร์ `line-dev/` ส่วน "Download ZIP" ของ GitHub จะได้ทั้ง repo (ชั้นบนสุดคือ `LINE-skill-main/`) ซึ่งอัปโหลดตรง ๆ ไม่ได้ ให้แตกไฟล์หรือ clone repo ก่อน แล้วบีบอัดเฉพาะโฟลเดอร์ `line-dev`
   - macOS/Linux: ในโฟลเดอร์ `LINE-skill/skills` ให้รัน `zip -r ../../line-dev.zip line-dev -x '*.DS_Store'`
   - Windows: ใน File Explorer คลิกขวาที่โฟลเดอร์ `skills\line-dev` → "Compress to ZIP file" (บีบอัดเป็นไฟล์ ZIP; บน Windows 10 คือ "Send to → Compressed (zipped) folder")
3. ไปที่ **Customize > Skills** กด **+** → **Create skill** → **Upload a skill** แล้วอัปโหลด ZIP ถ้าหน้าจอเป็น **Settings > Capabilities** ให้กด **Upload skill** ในส่วน Skills

skill ที่อัปโหลดใช้ได้เฉพาะบัญชีของคุณ ถ้าจะให้ทั้งองค์กรใช้ เจ้าขององค์กรต้องเป็นผู้จัดสรร (provision) ให้ สภาพแวดล้อมรันโค้ดของแอปปกติอนุญาตแค่ตัวจัดการแพ็กเกจ `github.com` และโดเมนอีกไม่กี่แห่ง: เมื่อ `line_docs.py` เชื่อมต่อ `raw.githubusercontent.com` ไม่ได้ จะดึงเอกสารชุดเดียวกันจาก `github.com` แทนโดยอัตโนมัติ ส่วน `api.line.me` ที่ `line_api.py` ต้องใช้จะเชื่อมต่อไม่ได้โดยค่าเริ่มต้น สำหรับแผน Team และ Enterprise เจ้าขององค์กรเพิ่มโดเมนที่อนุญาตได้ที่ Capabilities ในการตั้งค่าองค์กร ถ้าต้องการเรียก LINE API โดยตรง แนะนำให้ใช้ Claude Code หรือเครื่องมืออื่นบนเครื่องของคุณเอง ถ้าหน้าจอเปลี่ยนไป ให้ยึดตาม[คู่มือทางการ](https://support.claude.com/en/articles/12512180-using-skills-in-claude)

### ChatGPT

ตาม[คู่มือทางการ](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) ตอนนี้ skill ใน ChatGPT เปิดให้ผู้ใช้ที่มีสิทธิ์ในแผน Business, Enterprise, Healthcare และ Edu และจะอัปโหลดได้หรือไม่ขึ้นอยู่กับการตั้งค่าเวิร์กสเปซ

1. เตรียม `line-dev.zip` ตามวิธีในหัวข้อก่อนหน้า
2. ที่แถบด้านข้าง ไปที่ **Plugins** → แท็บ **Skills** กด **Create** → **Upload from your computer** แล้วอัปโหลด ZIP
3. ในแชท พิมพ์ `@` แล้วเลือก `line-dev` หรือปล่อยให้ ChatGPT ตัดสินใจเอง

ตอนนี้ skill ของ ChatGPT และ Codex ยังไม่ซิงก์กัน ถ้าใช้ Codex ต้องติดตั้งแยก ถ้าต้องการเรียก LINE API โดยตรง แนะนำให้ใช้ Codex หรือเครื่องมืออื่นบนเครื่องของคุณเอง

### การอัปเดตและการลบ

| วิธีติดตั้ง | อัปเดต | ลบ |
|---|---|---|
| `bunx skills` | `bunx skills update line-dev` | `bunx skills remove line-dev` |
| `gh skill` | `gh skill update` | ลบโฟลเดอร์ `line-dev` |
| Gemini CLI | ลบแล้วติดตั้งใหม่ | `gemini skills uninstall line-dev` |
| คัดลอกเอง | รัน `git pull` ในโฟลเดอร์ `LINE-skill` แล้วคัดลอกอีกครั้ง | ลบโฟลเดอร์ `line-dev` |
| แอป Claude, ChatGPT | ลบอันเก่าแล้วอัปโหลด ZIP ใหม่ | ลบในหน้า Skills |

### เอกสารทางการของแต่ละเครื่องมือ

ถ้าพาธหรือหน้าจอเปลี่ยนไป ให้ยึดตามเอกสารทางการ: [Claude Code](https://code.claude.com/docs/en/skills) · [แอป Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude) · [ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) · [OpenAI Codex](https://learn.chatgpt.com/docs/build-skills) · [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) · [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills) · [Cursor](https://cursor.com/docs/skills) · [Gemini CLI](https://geminicli.com/docs/cli/skills/) · [Google Antigravity](https://antigravity.google/docs/skills) · [Devin Desktop](https://docs.devin.ai/desktop/cascade/skills) · [OpenCode](https://opencode.ai/docs/skills) · [Cline](https://docs.cline.bot/customization/skills) · [Kiro](https://kiro.dev/docs/skills/) · [JetBrains Junie](https://junie.jetbrains.com/docs/agent-skills.html) · [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) · [skills](https://github.com/vercel-labs/skills) · [gh skill](https://cli.github.com/manual/gh_skill_install)

## การใช้สคริปต์

skill จะเรียกสคริปต์เหล่านี้เอง แต่คุณก็รันเองได้ ต้องใช้ Python 3.8 ขึ้นไป ไม่ต้องติดตั้งแพ็กเกจใด ๆ (บน Windows ใช้ `python` หรือ `py -3`)

```bash
# ค้นเอกสารทางการ (ดึงแบบเรียลไทม์ แคชไว้ 1 วัน ค้นแบบเต็มข้อความได้เมื่อมี git)
python3 skills/line-dev/scripts/line_docs.py search "loading animation"
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
python3 skills/line-dev/scripts/line_docs.py page messaging-api/pricing --grep count

# Messaging API: ใส่ token ในตัวแปรสภาพแวดล้อม หรือใช้ --env-file ชี้ไปที่ .env ของโปรเจกต์
export LINE_CHANNEL_ACCESS_TOKEN=...
python3 skills/line-dev/scripts/line_api.py info                     # ข้อมูลบอท
python3 skills/line-dev/scripts/line_api.py quota                    # โควตาและการใช้งานเดือนนี้
python3 skills/line-dev/scripts/line_api.py validate push card.json  # ตรวจรูปแบบข้อความโดยไม่ส่งจริง
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "ทดสอบ"        # dry-run: แค่แสดงว่าจะส่งอะไร
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "ทดสอบ" --yes  # ส่งจริง
python3 skills/line-dev/scripts/line_api.py richmenu-validate menu.json --image menu.png
python3 skills/line-dev/scripts/line_api.py richmenu-deploy menu.json menu.png --default        # dry-run
python3 skills/line-dev/scripts/line_api.py webhook-test

# ดีบัก webhook: ใส่ secret ในตัวแปรสภาพแวดล้อม
export LINE_CHANNEL_SECRET=...
python3 skills/line-dev/scripts/webhook_tools.py selftest http://localhost:3000/webhook
python3 skills/line-dev/scripts/webhook_tools.py simulate http://localhost:3000/webhook postback --source group
python3 skills/line-dev/scripts/webhook_tools.py sample memberJoined
```

`selftest` จะส่งคำขอ 4 ครั้งตามลำดับ ได้แก่ Verify ของ Console (`events` ว่าง), อีเวนต์ที่ลายเซ็นถูกต้อง, ลายเซ็นผิด และไม่มีลายเซ็น พร้อมตรวจว่าการตอบกลับเกินเวลาหมดอายุ 2 วินาทีของ LINE หรือไม่

## เนื้อหา

```
skills/line-dev/
├── SKILL.md                      # คำอธิบายหลัก (สำหรับ AI อ่าน, ภาษาอังกฤษ)
├── references/
│   ├── doc-map.md                # ดัชนีเอกสารทางการ: กฎของ URL, รายการหน้า, anchor ของ API reference, OpenAPI, หน้าสถานะ, ประกาศยุติการให้บริการ
│   └── gotchas/                  # กับดักจากการใช้งานจริงและแพตเทิร์นการออกแบบ แยกไฟล์ตามหัวข้อ AI อ่านเฉพาะที่ต้องใช้
│       ├── webhooks-and-hosting.md
│       ├── messaging.md
│       ├── groups-and-mentions.md
│       ├── rich-menus.md
│       ├── liff-and-login.md
│       └── security-and-architecture.md
└── scripts/
    ├── line_docs.py              # ค้นเอกสารทางการแบบเรียลไทม์: ค้นแบบเต็มข้อความ, ดึงส่วนของ API reference, ดึงหน้าคู่มือ (พร้อม URL ที่อ้างอิงได้)
    ├── line_api.py               # CLI สำหรับ Messaging API (dry-run ก่อนเสมอ)
    └── webhook_tools.py          # คำนวณ/ตรวจลายเซ็น, จำลอง LINE ยิง webhook, selftest ในคำสั่งเดียว
evals/                            # สถานการณ์ทดสอบที่ใช้พัฒนา skill นี้
.github/                          # เอกสารชุมชน (แนวทางการมีส่วนร่วม, จรรยาบรรณ, นโยบายความปลอดภัย, คำแถลงด้านการเข้าถึง) และเทมเพลต issue/PR
```

## การออกแบบด้านความปลอดภัย

- คำสั่งที่เขียนข้อมูล เช่น push/multicast/broadcast, ตั้งค่า webhook, เผยแพร่/ตั้งเป็นค่าเริ่มต้น/ลบริชเมนู, ให้บอทออกจากกลุ่ม ถ้าไม่มี `--yes` จะทำแค่ dry-run: ตรวจสอบก่อน แล้วพิมพ์คำขอทั้งหมด พร้อมประเภทผู้รับ จำนวนสมาชิกในกลุ่ม (การ push เข้ากลุ่มนับตามจำนวนคน) และโควตาที่เหลือของเดือนนี้
- การส่งข้อความจะแนบ `X-Line-Retry-Key` ให้อัตโนมัติ การลองใหม่หลังหมดเวลาจึงไม่ส่งซ้ำ
- `line_api.py` เชื่อมต่อแค่ `api.line.me` และ `api-data.line.me`, `line_docs.py` เชื่อมต่อแค่ GitHub เพื่อดึงเอกสาร และ `webhook_tools.py` ยิงไปที่ URL ที่คุณระบุเท่านั้น (ส่งลายเซ็น ไม่ส่ง secret) token/secret จะไม่ปรากฏในผลลัพธ์
- skill จะรันสคริปต์บนเครื่องของคุณ (หรือในสภาพแวดล้อมรันโค้ดของเครื่องมือ AI) ก่อนติดตั้งสามารถอ่าน `SKILL.md` และ `scripts/` ดูก่อนได้

## เอกสารทางการ

แหล่งเอกสารทางการที่ skill นี้อ้างอิง: [LINE Developers](https://developers.line.biz/) และไฟล์ markdown ต้นฉบับ [line/line-developers-docs-source](https://github.com/line/line-developers-docs-source) (README ของ repo นั้นอนุญาตให้เครื่องมือ AI ใช้งานไว้อย่างชัดเจน) เอกสารทางการมีการอัปเดตอยู่เสมอ skill จึงเก็บไว้แค่ดัชนี ไม่แนบสำเนา

## การทดสอบ

`evals/evals.json` คือสถานการณ์ทดสอบ 5 ข้อที่ใช้พัฒนา skill นี้ ได้แก่ ดีบัก webhook 401, ค้นสเปกของบอทกลุ่ม, เผยแพร่ริชเมนู, การยืนยันตัวตนผู้ใช้ใน LIFF และ code review ของบอทกลุ่ม รวมเกณฑ์ให้คะแนน 49 ข้อ `evals/files/richmenu/` คือไฟล์ริชเมนูที่จงใจใส่ข้อผิดพลาดไว้ ส่วน `fake-env.txt` คือ token ปลอมที่สร้างแบบสุ่ม เมื่อรันข้อ 3 ให้คัดลอกไปไว้ในโฟลเดอร์ทำงานแล้วเปลี่ยนชื่อเป็น `.env` (โจทย์ระบุว่า token อยู่ใน `.env`)

การเปรียบเทียบครั้งล่าสุด (Claude Opus 5.5 รันแต่ละสถานการณ์แบบมีและไม่มี skill อย่างละครั้ง ให้คะแนนแบบ blind): แบบมี skill ผ่าน 47/49 แบบไม่มี skill ผ่าน 44/49 และแบบมี skill เร็วกว่าเฉลี่ย 16% จุดที่ต่างกันมากที่สุดคือ LIFF (คำเตือนด้านความปลอดภัยเรื่อง LIFF SDK เวอร์ชันที่เลิกใช้แล้ว และล็อกอินใหม่เฉพาะเมื่อ token หมดอายุ) กับการเผยแพร่ริชเมนู (ไม่ใส่ token ในบรรทัดคำสั่ง และยืนยันก่อนเผยแพร่) หลังจากแก้ skill ตาม 2 เกณฑ์ที่ไม่ผ่าน แล้วรันข้อ 1 และ 5 ใหม่ ก็ผ่านทั้งหมด รวม 5 ข้อแบบมี skill ได้ 49/49 ส่วนการทดสอบการเรียกใช้ skill (10 ประโยคที่ควรใช้ และ 10 ประโยคคล้ายกันที่ไม่ควรใช้ ประโยคละ 3 ครั้ง) ตัดสินถูกทั้งหมด

## การมีส่วนร่วม

ยินดีรับการแจ้งสเปก LINE ที่ล้าสมัย การเพิ่มกับดัก และการปรับปรุงสคริปต์หรือเอกสาร

- ขั้นตอน หลักการของ skill และวิธีตรวจการเปลี่ยนแปลง: [แนวทางการมีส่วนร่วม](.github/CONTRIBUTING_th.md)
- [จรรยาบรรณ](.github/i18n/CODE_OF_CONDUCT_th.md)
- ช่องโหว่ด้านความปลอดภัยให้แจ้งแบบส่วนตัวตาม[นโยบายความปลอดภัย](.github/SECURITY_th.md) อย่าเปิด issue สาธารณะ
- สถานะด้านการเข้าถึงและข้อจำกัดที่ทราบ: [คำแถลงด้านการเข้าถึง](.github/ACCESSIBILITY_th.md)

## สัญญาอนุญาต

[MIT](LICENSE)

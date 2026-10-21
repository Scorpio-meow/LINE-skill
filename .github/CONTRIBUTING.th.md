# แนวทางการมีส่วนร่วม

[繁體中文](/.github/CONTRIBUTING.md) | [English](/.github/CONTRIBUTING.en.md) | [日本語](/.github/CONTRIBUTING.ja.md) | **ไทย** | [Bahasa Indonesia](/.github/CONTRIBUTING.id.md) | [한국어](/.github/CONTRIBUTING.ko.md)

ขอบคุณที่อยากช่วย! การมีส่วนร่วมในโปรเจกต์นี้ต้องปฏิบัติตาม[จรรยาบรรณ](/.github/i18n/CODE_OF_CONDUCT.th.md)

เปิด issue หรือ PR ด้วยภาษาใดก็ได้ที่ README มี (繁體中文, English, 日本語, ไทย, Bahasa Indonesia, 한국어) แต่คำตอบอาจเป็นภาษาจีนตัวเต็มหรือภาษาอังกฤษ

> โปรเจกต์นี้ไม่ใช่โปรเจกต์อย่างเป็นทางการของ LY Corporation ปัญหาของแพลตฟอร์ม LINE เอง (แอป LINE, Messaging API, LIFF, LINE Login) โปรดแจ้งผ่านช่องทางทางการของ LINE

## สิ่งที่คุณช่วยได้

| สิ่งที่อยากทำ | วิธีทำ |
|---|---|
| ปัญหาในการติดตั้งหรือใช้งาน ไอเดียที่อยากพูดคุย | ถามได้ที่ [Discussions](https://github.com/Scorpio-meow/LINE-skill/discussions) |
| สเปกของ LINE เปลี่ยน ลิงก์เอกสารใช้ไม่ได้ หรือตัวเลขที่ skill บอกล้าสมัย | เปิด issue แบบ "Outdated LINE info or broken link" (ข้อมูล LINE ล้าสมัยหรือลิงก์เสีย) พร้อมแนบแหล่งอ้างอิงทางการ |
| เจอกับดักที่ skill ยังไม่ได้เขียนไว้ | เปิด issue แบบ "Feature request or new gotcha" (ขอฟีเจอร์หรือแจ้งกับดักใหม่) หรือส่ง PR เพิ่มลงใน `references/gotchas/` ได้เลย |
| สคริปต์ error หรือ AI ทำตาม skill แล้วยังทำผิด | เปิด issue แบบ "Bug report" (รายงานบั๊ก) |
| เอกสารอ่านไม่เข้าใจ คำแปลผิด ปัญหาด้านการเข้าถึง | เปิด issue แบบที่ตรงกัน หรือส่ง PR ได้เลย |
| ช่องโหว่ด้านความปลอดภัย | **อย่าเปิด issue** ให้แจ้งแบบส่วนตัวตาม [SECURITY.md](/.github/SECURITY.th.md) |

การเปลี่ยนแปลงที่ใหญ่ขึ้น (คำสั่งใหม่ของสคริปต์, ปรับขั้นตอนใน `SKILL.md`, เพิ่มไฟล์ gotcha) โปรดเปิด issue พูดคุยกันก่อน จะได้ไม่เสียแรงเปล่า

## หลักการของ skill นี้

ก่อนแก้ไข โปรดอ่าน [`skills/line-dev/SKILL.md`](/skills/line-dev/SKILL.md) ให้จบก่อน PR จะถูกรีวิวตามข้อต่อไปนี้:

1. **ไม่แนบสำเนาเอกสารทางการ** skill มีเพียงดัชนี "หัวข้อ → URL ทางการ" และสคริปต์สำหรับค้นหา สเปกทั้งหมดต้องค้นจาก [LINE Developers](https://developers.line.biz/) แบบเรียลไทม์เสมอ อย่าคัดลอกเอกสารทางการยาว ๆ มาใส่ใน repo ถ้าจะอ้างอิง ให้ใส่ URL หรือชื่อส่วนที่ค้นเจอได้ด้วย `line_docs.py`
2. **รายการกับดักมีรูปแบบตายตัว**: **อาการหรือกฎ → สาเหตุ → วิธีแก้** แล้วใส่หน้าเอกสารทางการที่ต้องตรวจซ้ำไว้หลัง `Re-check:` (พาธอิงจาก `https://developers.line.biz/en/`) ตัวเลขที่อาจเปลี่ยนให้ระบุ "(at the time of writing)" และอัปเดตปีและเดือนที่ตรวจสอบไว้ที่ต้นไฟล์
3. **`SKILL.md` เขียนไว้ให้ AI อ่าน**: ใช้ภาษาอังกฤษ สั้นและแม่นยำ รายละเอียดใส่ไว้ใน `references/` หนึ่งไฟล์ต่อหนึ่งหัวข้อ เพื่อให้ AI อ่านเฉพาะที่ต้องใช้
4. **สคริปต์ใช้แค่ไลบรารีมาตรฐานของ Python 3.8 ขึ้นไป** ไม่เพิ่มแพ็กเกจภายนอก
5. **ห้ามผ่อนปรนการจัดการ token และ secret**: อ่านจากตัวแปรสภาพแวดล้อมหรือ `--env-file` เท่านั้น ไม่พิมพ์ออกมาและไม่เขียนลงไฟล์ `line_api.py` เชื่อมต่อแค่ `api.line.me` และ `api-data.line.me`, `line_docs.py` เชื่อมต่อแค่ GitHub และ `webhook_tools.py` ยิงไปที่ URL ที่ผู้ใช้ระบุเท่านั้นและส่งแค่ลายเซ็น
6. **คำสั่งที่เขียนข้อมูลต้อง dry-run เป็นค่าเริ่มต้น**: ถ้าไม่มี `--yes` จะส่งจริงหรือเปลี่ยนการตั้งค่าไม่ได้ คำสั่งเขียนข้อมูลที่เพิ่มใหม่ก็ต้องทำตามนี้ และต้องระบุไว้ใน Safety tiers ของ `SKILL.md`

## สภาพแวดล้อมสำหรับพัฒนา

```bash
git clone https://github.com/Scorpio-meow/LINE-skill.git
cd LINE-skill
```

ถ้าต้องการให้เครื่องมือ AI อ่านเวอร์ชันที่คุณกำลังแก้อยู่โดยตรง ให้ลิงก์โฟลเดอร์ skill ไปยังโฟลเดอร์ skill ของเครื่องมือ (ลบ `line-dev` ที่ติดตั้งไว้ออกก่อน) ตัวอย่างด้านล่างใช้ Claude Code ส่วนโฟลเดอร์ของเครื่องมืออื่นดูได้ที่ [README](/README.th.md#โฟลเดอร์-skill-ของแต่ละเครื่องมือ):

macOS/Linux:

```bash
ln -s "$PWD/skills/line-dev" ~/.claude/skills/line-dev
```

Windows PowerShell (junction ไม่ต้องใช้สิทธิ์ผู้ดูแลระบบ):

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\line-dev" -Target "$PWD\skills\line-dev"
```

## ตรวจสอบการเปลี่ยนแปลง

ตอนนี้ยังไม่มีการทดสอบอัตโนมัติ โปรดรันคำสั่งด้านล่างให้ผ่านเป็นอย่างน้อย (บน Windows ใช้ `python` หรือ `py -3`):

```bash
# สคริปต์ทั้งสามตัวต้องเริ่มทำงานได้ (ถ้ามี syntax error จะเห็นตรงนี้)
python3 skills/line-dev/scripts/line_api.py -h
python3 skills/line-dev/scripts/line_docs.py -h
python3 skills/line-dev/scripts/webhook_tools.py -h

# การทำงานจริงที่ไม่ต้องใช้ token
python3 skills/line-dev/scripts/webhook_tools.py sample text
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
```

- **รองรับ Python 3.8**: อย่าใช้ไวยากรณ์หรือฟังก์ชันที่เพิ่งมีใน 3.9 ขึ้นไป (เช่น type hint แบบ `list[str]`, `str.removeprefix`, `match`) ถ้ามี [uv](https://docs.astral.sh/uv/) จะรันด้วย 3.8 ได้แบบนี้: `uv run --no-project --python 3.8 python skills/line-dev/scripts/line_api.py -h`
- **ถ้าแก้ฟีเจอร์ที่เกี่ยวกับ webhook**: รัน `webhook_tools.py selftest <url>` กับ webhook บนเครื่องของคุณ
- **ถ้าแก้คำสั่งที่เขียนข้อมูลใน `line_api.py`**: ตรวจว่าถ้าไม่ใส่ `--yes` จะแค่พิมพ์คำขอออกมา ไม่ส่งจริง ถ้าจะทดสอบกับ channel จริง โปรดใช้บัญชีทดสอบของคุณเอง
- **ถ้าแก้ `SKILL.md` หรือ gotchas ซึ่งอาจส่งผลต่อพฤติกรรมของ AI**: ใช้สถานการณ์ทดสอบที่เกี่ยวข้องใน [`evals/evals.json`](/evals/evals.json) รันทั้งก่อนและหลังแก้อย่างละครั้ง ให้คะแนนเทียบกับ `expectations` ของแต่ละข้อ แล้วเขียนจำนวนข้อที่ผ่านไว้ใน PR จะใช้วิธีใดก็ได้ แม้แต่วางโจทย์ในเครื่องมือ AI แล้วให้คะแนนเองก็ได้ ถ้าเพิ่มหัวข้อใหญ่ใหม่ ยินดีถ้าจะเพิ่มสถานการณ์ทดสอบมาด้วย

## เอกสาร

- [`README.md`](/README.md) (ภาษาจีนตัวเต็ม) คือฉบับหลัก ถ้าแก้เนื้อหาในนั้น โปรดอัปเดตฉบับภาษาอื่นด้วย ภาษาที่คุณไม่ถนัดให้ระบุไว้ใน PR แล้วผู้ดูแลจะเติมให้
- การเปลี่ยนแปลงที่ควรรู้ ให้บันทึกไว้ใน `[Unreleased]` ของ [`CHANGELOG.md`](/CHANGELOG.md) ตามรูปแบบของ [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## การส่ง Pull Request

- หนึ่ง PR ทำเพียงเรื่องเดียว ยิ่งเปลี่ยนน้อยยิ่งรีวิวง่าย
- ข้อความ commit ใช้รูปแบบ [Conventional Commits](https://www.conventionalcommits.org/th/v1.0.0/) เมื่อแก้ตัว skill ให้ใส่ scope `line-dev` เช่น `fix(line-dev): 擋下 line_docs.py 的路徑穿越`, `docs: 更新評測結果` คำอธิบายจะเขียนภาษาใดก็ได้
- **ห้าม commit token, secret, userId หรือ groupId จริงเด็ดขาด** ตัวอย่างและข้อมูลทดสอบต้องใช้ค่าปลอมเสมอ (สร้างแบบสุ่มเหมือน `evals/files/richmenu/fake-env.txt`)
- กรอกเทมเพลต PR ว่าทำอะไรไปและทดสอบอย่างไร

## สัญญาอนุญาต

ผลงานที่คุณส่งมาจะเผยแพร่ภายใต้[สัญญาอนุญาต MIT](/LICENSE)ของโปรเจกต์นี้

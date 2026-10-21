# LINE-skill

[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [ไทย](README.th.md) | **Bahasa Indonesia** | [한국어](README.ko.md)

Agent Skill untuk asisten coding AI: **`line-dev`**. Skill ini membuat Claude, Codex, GitHub Copilot, Cursor, Gemini CLI, dan alat sejenis lebih andal saat membangun, men-debug, dan mengoperasikan platform LINE — webhook Messaging API, pesan reply/push dan kuota pesan, Flex Message, rich menu, bot obrolan grup, LIFF, dan LINE Login.

Skill ini memakai format terbuka [Agent Skills](https://agentskills.io) (satu folder berisi `SKILL.md`), jadi bisa dipakai di alat apa pun yang mendukung format ini. Cara memasangnya ada di [Mulai cepat](#mulai-cepat).

- **Spesifikasi selalu dicek langsung ke dokumentasi resmi**: skill ini tidak menyertakan salinan dokumentasi, hanya indeks "topik → URL resmi" dan skrip pencarian. Setiap kali angka, batasan, atau harga diperlukan, AI langsung mencarinya di markdown mentah resmi di GitHub (sumber yang disinkronkan ke developers.line.biz) dan mencantumkan halaman developers.line.biz sebagai rujukan.
- **Daftar jebakan dari pengalaman nyata**: verifikasi tanda tangan harus memakai raw body, webhook harus dibalas dalam sekitar 2 detik, reply token hanya sekali pakai dan cepat kedaluwarsa, push ke grup dihitung per anggota, akun yang belum terverifikasi tidak bisa mengambil daftar anggota grup, cara menulis dan meng-escape mention textV2, batas ukuran dan URI Flex, batas gambar dan urutan prioritas rich menu, kedaluwarsa ID token LIFF dan verifikasi di sisi server, userId yang berbeda antar-provider… Setiap poin ditulis dalam format "gejala → penyebab → solusi → halaman resmi".
- **Operasikan LINE API secara langsung**: tersedia skrip yang hanya memakai pustaka standar Python. Operasi tulis secara default hanya dry-run dan baru benar-benar dijalankan setelah Anda mengonfirmasi dengan menambahkan `--yes`; token/secret hanya dibaca dari variabel lingkungan atau `.env` dan tidak pernah dicetak.

> Proyek ini bukan proyek resmi LY Corporation. LINE adalah merek dagang LY Corporation.

## Mulai cepat

Pasang dengan satu baris perintah [`skills`](https://github.com/vercel-labs/skills); perintah ini mendeteksi alat AI di komputer Anda dan menaruh skill di folder yang sesuai:

```bash
bunx skills add Scorpio-meow/LINE-skill --skill line-dev -g
```

- `-g` memasang ke direktori home (bisa dipakai di semua proyek); hapus `-g` untuk memasang hanya di proyek saat ini.
- Untuk memasang hanya ke alat tertentu, tambahkan `-a`, misalnya `-a claude-code -a codex`; nilai untuk setiap alat ada di [tabel pada bagian berikutnya](#folder-skill-per-alat).
- Tidak punya [Bun](https://bun.sh)? Ganti `bunx` dengan `npx`.

Setelah terpasang, skill otomatis aktif saat Anda bertanya tentang pengembangan LINE, misalnya:

> Berapa lama reply token bot LINE berlaku sebelum kedaluwarsa?

Jika skill termuat, jawabannya akan mengecek dokumentasi resmi terlebih dahulu dan menyertakan tautan developers.line.biz. Saat skrip pertama kali dijalankan, sebagian besar alat akan meminta izin Anda untuk menjalankan perintah atau mengakses jaringan.

Pemasangan manual untuk tiap alat dan cara lainnya dijelaskan di bagian berikutnya.

## Pemasangan

Membutuhkan **Python 3.8 atau lebih baru** (skrip hanya memakai pustaka standar; tidak perlu memasang paket). Mencari dokumentasi resmi memerlukan akses ke `raw.githubusercontent.com` atau `github.com`; mengoperasikan LINE API secara langsung memerlukan akses ke `api.line.me`.

### Folder skill per alat

Pemasangan manual berarti menyalin folder `line-dev` ke folder skill yang dibaca alat tersebut, sehingga `SKILL.md` berada di `<folder skill>/line-dev/SKILL.md`. Folder pribadi berlaku untuk semua proyek di komputer ini; folder proyek berada di bawah root proyek dan bisa di-commit agar dipakai bersama tim.

| Alat | Nilai `-a` | Folder pribadi | Folder proyek | Panggil manual |
|---|---|---|---|---|
| Claude Code | `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/line-dev` |
| OpenAI Codex (CLI, ekstensi IDE, aplikasi desktop ChatGPT) | `codex` | `~/.agents/skills/` | `.agents/skills/` | `/skills` atau `$line-dev` |
| GitHub Copilot (VS Code, Copilot CLI, JetBrains) | `github-copilot` | `~/.copilot/skills/` | `.github/skills/` | `/line-dev` |
| Cursor | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` | Ketik `/` di chat Agent lalu pilih |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` | `.gemini/skills/` | `/skills list` untuk mengecek apakah sudah termuat |
| Google Antigravity | `antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` | — |
| Devin Desktop (sebelumnya Windsurf) | `devin` | `~/.config/devin/skills/` | `.devin/skills/` | `@line-dev` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | — |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | `/line-dev` |
| Kiro | `kiro-cli` | `~/.kiro/skills/` | `.kiro/skills/` | Ketik `/` lalu pilih |
| JetBrains Junie | `junie` | `~/.junie/skills/` | `.junie/skills/` | `/line-dev` atau `$line-dev` |
| Roo Code | `roo` | `~/.roo/skills/` | `.roo/skills/` | — |

Di Windows, `~` adalah folder pengguna (`%USERPROFILE%`). Semua alat otomatis memakai skill saat percakapan relevan; kolom "Panggil manual" hanya menunjukkan cara memintanya secara eksplisit.

- Codex, Copilot, Cursor, Gemini CLI, OpenCode, Devin Desktop, Junie, dan Roo Code juga membaca `~/.agents/skills/`, jadi jika Anda memakai beberapa alat, cukup taruh satu salinan di sana untuk dipakai bersama. Claude Code hanya membaca `~/.claude/skills/`.
- `bunx skills` menaruh skill di `.agents/skills/` bersama (dengan `-g`: `~/.agents/skills/`) lalu membuat tautan untuk alat lain. Jika setelah itu alat tidak mendeteksinya, pasang secara manual ke folder di tabel seperti cara di bawah.
- Alat yang tidak ada di tabel (Amp, Goose, Kilo Code, Trae, Qwen Code, dll.) juga bisa dipasang dengan `bunx skills`; nilai `-a`-nya ada di [README skills](https://github.com/vercel-labs/skills).
- Devin Desktop juga masih membaca `~/.codeium/windsurf/skills/` dan `.windsurf/skills/` dari era Windsurf.

Contoh di bawah menyalin ke `~/.agents/skills/`; untuk alat lain, ubah `TARGET` ke path di tabel.

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

Jika alat tidak mendeteksi skill baru, mulai ulang alat tersebut sekali.

### Cara pemasangan lain

Beberapa alat punya perintah pemasangan sendiri:

- **GitHub CLI** (2.90 atau lebih baru; `gh skill` saat ini masih public preview): nilai `--agent` sama dengan `-a` di tabel.

  ```bash
  gh skill install Scorpio-meow/LINE-skill line-dev --agent claude-code --scope user
  ```

- **OpenAI Codex**: di Codex, ketik

  ```text
  $skill-installer install https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev
  ```

  Secara default Codex menjalankan perintah di sandbox tanpa akses jaringan, sehingga akan meminta persetujuan Anda saat skrip mencari dokumentasi atau memanggil LINE API. Untuk selalu mengizinkan, tambahkan ini ke `~/.codex/config.toml`:

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

- **GitHub Copilot CLI**: setelah clone, jalankan `copilot skill add LINE-skill/skills/line-dev`; jika ditambahkan di tengah sesi, muat dengan `/skills reload`. Jika ditaruh di `.github/skills/` dalam repo lalu di-commit, Copilot cloud agent juga akan memakainya.
- **Gemini CLI**: secara default dipasang di cakupan pengguna; tambahkan `--scope workspace` untuk memasang hanya di proyek saat ini.

  ```bash
  gemini skills install https://github.com/Scorpio-meow/LINE-skill.git --path skills/line-dev
  ```

- **Kiro**: di panel Kiro, buka **Agent Steering & Skills** → **+** → **Import a skill** → **GitHub**; URL harus menunjuk ke subfolder tempat skill berada: `https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev`.
- **Devin Desktop**: kelola skill dari **⋯** → **Skills** di kanan atas panel Cascade.
- **Cline**: skill baru aktif secara default; aktifkan atau nonaktifkan di tab **Skills** di bagian bawah panel Cline.

### Aplikasi Claude (web/desktop)

1. Aktifkan eksekusi kode: untuk paket Pro dan Max, buka **Settings > Capabilities** lalu aktifkan "Code execution and file creation"; untuk paket Team dan Enterprise, pemilik organisasi mengaktifkan "Code execution and file creation" dan "Skills" di pengaturan organisasi.
2. Buat `line-dev.zip` sendiri. Tingkat teratas ZIP harus folder `line-dev/`; "Download ZIP" dari GitHub berisi seluruh repo (tingkat teratas `LINE-skill-main/`) sehingga tidak bisa langsung diunggah, jadi ekstrak dulu atau clone repo, lalu kompres folder `line-dev` saja.
   - macOS/Linux: di folder `LINE-skill/skills`, jalankan `zip -r ../../line-dev.zip line-dev -x '*.DS_Store'`.
   - Windows: di File Explorer, klik kanan folder `skills\line-dev` → "Compress to ZIP file" (di Windows 10: "Send to → Compressed (zipped) folder").
3. Buka **Customize > Skills**, klik **+** → **Create skill** → **Upload a skill**, lalu unggah ZIP. Jika antarmuka Anda menampilkan **Settings > Capabilities**, klik **Upload skill** di bagian Skills.

Skill yang diunggah hanya bisa dipakai oleh akun Anda; agar bisa dipakai seluruh organisasi, pemilik organisasi harus menyediakannya (provisioning). Lingkungan eksekusi kode aplikasi biasanya hanya mengizinkan manajer paket, `github.com`, dan beberapa domain lain: jika `line_docs.py` tidak bisa menjangkau `raw.githubusercontent.com`, skrip ini otomatis mengambil dokumentasi yang sama dari `github.com`; `api.line.me` yang dibutuhkan `line_api.py` diblokir secara default, dan pada paket Team dan Enterprise pemilik organisasi bisa menambahkan domain yang diizinkan di Capabilities pada pengaturan organisasi. Untuk mengoperasikan LINE API secara langsung, sebaiknya gunakan Claude Code atau alat serupa di komputer Anda sendiri. Jika antarmukanya berubah, ikuti [panduan resmi](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

### ChatGPT

Menurut [artikel bantuan resmi](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), skill di ChatGPT saat ini tersedia untuk pengguna yang memenuhi syarat di paket Business, Enterprise, Healthcare, dan Edu, dan boleh tidaknya mengunggah ditentukan oleh pengaturan workspace.

1. Siapkan `line-dev.zip` seperti dijelaskan di bagian sebelumnya.
2. Di sidebar, buka **Plugins** → tab **Skills**, klik **Create** → **Upload from your computer**, lalu unggah ZIP.
3. Di chat, ketik `@` lalu pilih `line-dev`, atau biarkan ChatGPT memutuskan sendiri.

Saat ini skill ChatGPT dan Codex tidak tersinkron, jadi pasang secara terpisah jika Anda memakai Codex. Untuk mengoperasikan LINE API secara langsung, sebaiknya gunakan Codex atau alat serupa di komputer Anda sendiri.

### Memperbarui dan menghapus

| Cara pemasangan | Memperbarui | Menghapus |
|---|---|---|
| `bunx skills` | `bunx skills update line-dev` | `bunx skills remove line-dev` |
| `gh skill` | `gh skill update` | Hapus folder `line-dev` |
| Gemini CLI | Hapus lalu pasang ulang | `gemini skills uninstall line-dev` |
| Salin manual | Jalankan `git pull` di folder `LINE-skill`, lalu salin lagi | Hapus folder `line-dev` |
| Aplikasi Claude, ChatGPT | Hapus yang lama lalu unggah ZIP baru | Hapus di halaman Skills |

### Dokumentasi resmi tiap alat

Jika path atau antarmuka berubah, ikuti dokumentasi resmi: [Claude Code](https://code.claude.com/docs/en/skills) · [Aplikasi Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude) · [ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) · [OpenAI Codex](https://learn.chatgpt.com/docs/build-skills) · [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) · [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills) · [Cursor](https://cursor.com/docs/skills) · [Gemini CLI](https://geminicli.com/docs/cli/skills/) · [Google Antigravity](https://antigravity.google/docs/skills) · [Devin Desktop](https://docs.devin.ai/desktop/cascade/skills) · [OpenCode](https://opencode.ai/docs/skills) · [Cline](https://docs.cline.bot/customization/skills) · [Kiro](https://kiro.dev/docs/skills/) · [JetBrains Junie](https://junie.jetbrains.com/docs/agent-skills.html) · [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) · [skills](https://github.com/vercel-labs/skills) · [gh skill](https://cli.github.com/manual/gh_skill_install)

## Menggunakan skrip

Skill memanggil skrip-skrip ini sendiri; Anda juga bisa menjalankannya langsung. Membutuhkan Python 3.8 atau lebih baru tanpa paket tambahan (di Windows, gunakan `python` atau `py -3`).

```bash
# Cari dokumentasi resmi (diambil langsung, di-cache sehari; pencarian teks penuh jika git tersedia)
python3 skills/line-dev/scripts/line_docs.py search "loading animation"
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
python3 skills/line-dev/scripts/line_docs.py page messaging-api/pricing --grep count

# Messaging API: simpan token di variabel lingkungan, atau arahkan --env-file ke .env proyek Anda
export LINE_CHANNEL_ACCESS_TOKEN=...
python3 skills/line-dev/scripts/line_api.py info                     # info bot
python3 skills/line-dev/scripts/line_api.py quota                    # kuota dan pemakaian bulan ini
python3 skills/line-dev/scripts/line_api.py validate push card.json  # validasi format pesan tanpa mengirim
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "tes"        # dry-run: hanya menampilkan apa yang akan dikirim
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "tes" --yes  # benar-benar mengirim
python3 skills/line-dev/scripts/line_api.py richmenu-validate menu.json --image menu.png
python3 skills/line-dev/scripts/line_api.py richmenu-deploy menu.json menu.png --default        # dry-run
python3 skills/line-dev/scripts/line_api.py webhook-test

# Debug webhook: simpan secret di variabel lingkungan
export LINE_CHANNEL_SECRET=...
python3 skills/line-dev/scripts/webhook_tools.py selftest http://localhost:3000/webhook
python3 skills/line-dev/scripts/webhook_tools.py simulate http://localhost:3000/webhook postback --source group
python3 skills/line-dev/scripts/webhook_tools.py sample memberJoined
```

`selftest` mengirim empat permintaan secara berurutan — Verify di Console (`events` kosong), event dengan tanda tangan yang benar, tanda tangan yang salah, dan tanpa tanda tangan — serta mengecek apakah ada respons yang melewati batas waktu 2 detik LINE.

## Isi

```
skills/line-dev/
├── SKILL.md                      # Instruksi utama (untuk AI, berbahasa Inggris)
├── references/
│   ├── doc-map.md                # Indeks dokumentasi resmi: aturan URL, daftar halaman, anchor API reference, OpenAPI, halaman status, pengumuman penghentian
│   └── gotchas/                  # Jebakan dari pengalaman nyata dan pola desain, satu file per topik; AI hanya membaca yang diperlukan
│       ├── webhooks-and-hosting.md
│       ├── messaging.md
│       ├── groups-and-mentions.md
│       ├── rich-menus.md
│       ├── liff-and-login.md
│       └── security-and-architecture.md
└── scripts/
    ├── line_docs.py              # Cari dokumentasi resmi secara langsung: pencarian teks penuh, bagian API reference, halaman panduan (dengan URL yang bisa dikutip)
    ├── line_api.py               # CLI Messaging API (dry-run terlebih dahulu)
    └── webhook_tools.py          # Hitung/verifikasi tanda tangan, simulasikan LINE memanggil webhook, selftest sekali jalan
evals/                            # Skenario uji yang dipakai untuk mengembangkan skill ini
.github/                          # Dokumen komunitas (panduan kontribusi, kode etik, kebijakan keamanan, pernyataan aksesibilitas) dan templat issue/PR
```

## Keamanan

- Operasi tulis — push/multicast/broadcast, mengatur webhook, menerbitkan/menjadikan default/menghapus rich menu, mengeluarkan bot dari grup — hanya dry-run tanpa `--yes`: memvalidasi dulu, lalu mencetak permintaan lengkap beserta jenis penerima, jumlah anggota grup (push ke grup dihitung per anggota), dan sisa kuota bulan ini.
- Pengiriman pesan otomatis menyertakan `X-Line-Retry-Key`, jadi percobaan ulang setelah timeout tidak mengirim pesan ganda.
- `line_api.py` hanya terhubung ke `api.line.me` dan `api-data.line.me`, `line_docs.py` hanya terhubung ke GitHub untuk mengambil dokumentasi, dan `webhook_tools.py` hanya memanggil URL yang Anda tentukan (mengirim tanda tangan, bukan secret); token/secret tidak pernah muncul di output.
- Skill menjalankan skrip di komputer Anda (atau di lingkungan eksekusi alat AI); Anda bisa membaca `SKILL.md` dan `scripts/` sebelum memasang.

## Dokumentasi resmi

Sumber dokumentasi resmi yang dirujuk skill ini: [LINE Developers](https://developers.line.biz/) dan sumber markdown-nya, [line/line-developers-docs-source](https://github.com/line/line-developers-docs-source) (README-nya secara eksplisit mengizinkan penggunaan oleh alat AI). Dokumentasi resmi terus diperbarui, jadi skill hanya menyimpan indeks, bukan salinan.

## Pengujian

`evals/evals.json` berisi 5 skenario uji yang dipakai untuk mengembangkan skill ini — debug webhook 401, mencari spesifikasi bot grup, menerbitkan rich menu, autentikasi pengguna LIFF, dan code review bot grup — dengan total 49 kriteria penilaian. `evals/files/richmenu/` berisi materi rich menu yang sengaja diberi kesalahan; `fake-env.txt` adalah token palsu yang dibuat secara acak: saat menjalankan skenario 3, salin ke folder kerja dan ganti namanya menjadi `.env` (soal menyebut token ada di `.env`).

Perbandingan terbaru (Claude Opus 5.5, setiap skenario dijalankan sekali dengan dan tanpa skill, dinilai secara blind): dengan skill lulus 47/49, tanpa skill 44/49; dengan skill rata-rata 16% lebih cepat. Selisih terbesar ada pada LIFF (peringatan keamanan tentang versi LIFF SDK yang sudah deprecated, dan login ulang hanya saat token kedaluwarsa) dan penerbitan rich menu (tidak menaruh token di baris perintah, konfirmasi sebelum diterbitkan). Setelah skill direvisi untuk dua kriteria yang gagal, skenario 1 dan 5 dijalankan ulang dan lulus seluruhnya, sehingga total kelima skenario dengan skill menjadi 49/49. Uji pemicu (10 kalimat yang seharusnya memicu skill dan 10 kalimat mirip yang tidak seharusnya, masing-masing 3 kali) semuanya dinilai benar.

## Berkontribusi

Laporan spesifikasi LINE yang sudah usang, jebakan baru, dan perbaikan skrip maupun dokumentasi sangat diterima.

- Alur kerja, prinsip skill, dan cara memeriksa perubahan: [Panduan kontribusi](.github/CONTRIBUTING.id.md)
- [Kode Etik](.github/i18n/CODE_OF_CONDUCT.id.md)
- Laporkan celah keamanan secara privat sesuai [kebijakan keamanan](.github/SECURITY.id.md); jangan membuka issue publik.
- Status aksesibilitas dan keterbatasan yang diketahui: [Pernyataan aksesibilitas](.github/ACCESSIBILITY.id.md)

## Lisensi

[MIT](LICENSE)

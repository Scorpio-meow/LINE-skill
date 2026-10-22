# Panduan kontribusi

[繁體中文](/.github/CONTRIBUTING.md) | [English](/.github/CONTRIBUTING_en.md) | [日本語](/.github/CONTRIBUTING_ja.md) | [ไทย](/.github/CONTRIBUTING_th.md) | **Bahasa Indonesia** | [한국어](/.github/CONTRIBUTING_ko.md)

Terima kasih sudah mau membantu! Saat berpartisipasi dalam proyek ini, harap patuhi [Kode Etik](/.github/i18n/CODE_OF_CONDUCT_id.md).

Anda boleh membuka issue atau PR dalam bahasa apa pun yang tersedia untuk README (繁體中文, English, 日本語, ไทย, Bahasa Indonesia, 한국어); balasan mungkin ditulis dalam bahasa Tionghoa Tradisional atau bahasa Inggris.

> Proyek ini bukan proyek resmi LY Corporation. Masalah pada platform LINE itu sendiri (aplikasi LINE, Messaging API, LIFF, LINE Login) harap dilaporkan ke pihak resmi LINE.

## Yang bisa Anda bantu

| Yang ingin Anda lakukan | Caranya |
|---|---|
| Pertanyaan tentang pemasangan atau penggunaan, ide yang ingin didiskusikan | Tanyakan di [Discussions](https://github.com/Scorpio-meow/LINE-skill/discussions) |
| Spesifikasi LINE berubah, tautan dokumentasi rusak, angka yang disebut skill sudah usang | Buka issue "Outdated LINE info or broken link" (info LINE usang atau tautan rusak) dan sertakan sumber resminya |
| Menemukan jebakan yang belum dibahas skill | Buka issue "Feature request or new gotcha" (permintaan fitur atau jebakan baru), atau langsung kirim PR untuk menambahkannya ke `references/gotchas/` |
| Skrip error, atau AI sudah mengikuti skill tetapi tetap salah | Buka issue "Bug report" (laporan bug) |
| Dokumentasi sulit dipahami, terjemahan keliru, masalah aksesibilitas | Buka issue yang sesuai, atau langsung kirim PR |
| Celah keamanan | **Jangan buka issue**; laporkan secara privat sesuai [SECURITY.md](/.github/SECURITY_id.md) |

Untuk perubahan yang lebih besar (perintah skrip baru, mengubah alur di `SKILL.md`, menambah file jebakan baru), buka issue untuk berdiskusi terlebih dahulu agar usaha Anda tidak sia-sia.

## Prinsip skill ini

Sebelum mengubah apa pun, baca dulu [`skills/line-dev/SKILL.md`](/skills/line-dev/SKILL.md). PR akan ditinjau berdasarkan poin-poin berikut:

1. **Tidak menyertakan salinan dokumentasi resmi.** Skill hanya berisi indeks "topik → URL resmi" dan skrip pencarian; spesifikasi selalu dicek langsung di [LINE Developers](https://developers.line.biz/). Jangan menempelkan potongan panjang dokumentasi resmi ke repo; jika perlu mengutip, tulis URL-nya atau nama bagian yang bisa ditemukan dengan `line_docs.py`.
2. **Entri jebakan punya format tetap**: **gejala atau aturan → penyebab → solusi**, lalu cantumkan halaman resmi yang perlu dicek ulang dengan `Re-check:` (path relatif terhadap `https://developers.line.biz/en/`). Beri tanda "(at the time of writing)" pada angka yang bisa berubah, dan perbarui bulan dan tahun pengecekan di bagian awal file.
3. **`SKILL.md` ditulis untuk dibaca AI**: dalam bahasa Inggris, singkat dan tepat; detail ditaruh di `references/`, satu file per topik, agar AI hanya membaca yang diperlukan.
4. **Skrip hanya memakai pustaka standar Python 3.8 atau lebih baru**, tanpa paket pihak ketiga.
5. **Penanganan token dan secret tidak boleh dilonggarkan**: hanya dibaca dari variabel lingkungan atau `--env-file`, tidak dicetak, dan tidak ditulis ke file; `line_api.py` hanya terhubung ke `api.line.me` dan `api-data.line.me`, `line_docs.py` hanya terhubung ke GitHub, dan `webhook_tools.py` hanya memanggil URL yang ditentukan pengguna serta hanya mengirim tanda tangan.
6. **Operasi tulis secara default hanya dry-run**: tanpa `--yes`, tidak boleh benar-benar mengirim atau mengubah pengaturan. Perintah tulis baru juga harus mematuhi aturan ini dan dicantumkan di Safety tiers dalam `SKILL.md`.

## Lingkungan pengembangan

```bash
git clone https://github.com/Scorpio-meow/LINE-skill.git
cd LINE-skill
```

Agar alat AI langsung membaca versi yang sedang Anda ubah, buat tautan dari folder skill ini ke folder skill alat tersebut (hapus dulu `line-dev` yang sudah terpasang). Contoh di bawah untuk Claude Code; folder untuk alat lain ada di [README](/README_id.md#folder-skill-per-alat):

macOS/Linux:

```bash
ln -s "$PWD/skills/line-dev" ~/.claude/skills/line-dev
```

Windows PowerShell (junction tidak memerlukan hak administrator):

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\line-dev" -Target "$PWD\skills\line-dev"
```

## Memeriksa perubahan

Saat ini belum ada pengujian otomatis, jadi setidaknya jalankan perintah berikut (di Windows, gunakan `python` atau `py -3`):

```bash
# Ketiga skrip bisa dijalankan (kesalahan sintaks akan muncul di sini)
python3 skills/line-dev/scripts/line_api.py -h
python3 skills/line-dev/scripts/line_docs.py -h
python3 skills/line-dev/scripts/webhook_tools.py -h

# Operasi nyata yang tidak memerlukan token
python3 skills/line-dev/scripts/webhook_tools.py sample text
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
```

- **Kompatibel dengan Python 3.8**: jangan memakai sintaks atau fungsi yang baru tersedia mulai 3.9 (misalnya anotasi tipe `list[str]`, `str.removeprefix`, `match`). Jika punya [uv](https://docs.astral.sh/uv/), Anda bisa menjalankannya dengan 3.8 seperti ini: `uv run --no-project --python 3.8 python skills/line-dev/scripts/line_api.py -h`.
- **Jika mengubah fitur terkait webhook**: jalankan `webhook_tools.py selftest <url>` terhadap webhook lokal.
- **Jika mengubah perintah tulis di `line_api.py`**: pastikan tanpa `--yes` perintah hanya mencetak permintaan dan tidak benar-benar mengirim. Untuk menguji dengan channel sungguhan, gunakan akun uji milik Anda sendiri.
- **Jika mengubah `SKILL.md` atau file jebakan (gotchas) sehingga bisa memengaruhi perilaku AI**: jalankan skenario yang relevan dari [`evals/evals.json`](/evals/evals.json) masing-masing sekali sebelum dan sesudah perubahan, nilai berdasarkan `expectations` tiap skenario, lalu tulis jumlah yang lulus di PR. Caranya bebas; menempelkan skenario ke alat AI lalu menilainya secara manual juga boleh. Jika menambahkan topik besar baru, silakan sekalian tambahkan skenario uji.

## Dokumentasi

- [`README.md`](/README.md) (bahasa Tionghoa Tradisional) adalah versi utama. Jika Anda mengubah isinya, perbarui juga versi bahasa lainnya; untuk bahasa yang tidak Anda kuasai, cukup catat di PR dan pengelola akan melengkapinya.
- Catat perubahan yang penting di bagian `[Unreleased]` pada [`CHANGELOG.md`](/CHANGELOG.md), mengikuti format [Keep a Changelog](https://keepachangelog.com/id/1.1.0/).

## Mengirim pull request

- Satu PR untuk satu hal saja; makin kecil perubahannya, makin mudah ditinjau.
- Gunakan format [Conventional Commits](https://www.conventionalcommits.org/id/v1.0.0/) untuk pesan commit, dan tambahkan scope `line-dev` saat mengubah skill itu sendiri, misalnya `fix(line-dev): 擋下 line_docs.py 的路徑穿越` atau `docs: 更新評測結果`. Deskripsinya boleh ditulis dalam bahasa apa pun.
- **Jangan pernah meng-commit token, secret, userId, atau groupId sungguhan.** Contoh dan materi uji harus selalu memakai nilai palsu (dibuat secara acak seperti `evals/files/richmenu/fake-env.txt`).
- Isi templat PR dengan apa yang Anda ubah dan bagaimana Anda mengujinya.

## Lisensi

Kontribusi yang Anda kirim akan dirilis di bawah [lisensi MIT](/LICENSE) proyek ini.

# Kebijakan keamanan

[繁體中文](/.github/SECURITY.md) | [English](/.github/SECURITY.en.md) | [日本語](/.github/SECURITY.ja.md) | [ไทย](/.github/SECURITY.th.md) | **Bahasa Indonesia** | [한국어](/.github/SECURITY.ko.md)

## Versi yang didukung

Perbaikan hanya dilakukan untuk versi terbaru, yaitu branch `main`. Jika Anda memakai versi lama, perbarui dulu (caranya ada di [README](/README.id.md#memperbarui-dan-menghapus)).

## Melaporkan celah keamanan

**Jangan membuka issue publik.** Gunakan fitur pelaporan privat GitHub: buka tab **Security** di repo lalu klik **Report a vulnerability**, atau langsung buka [tautan ini](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new). Jika tidak bisa, kirim email ke yao921024@gmail.com dan tambahkan `[LINE-skill security]` di subjeknya.

Sertakan:

- File dan versi yang terdampak (commit)
- Langkah untuk mereproduksi, serta dampak yang ditimbulkan
- Usulan perbaikan (opsional)

Gunakan token dan secret palsu saat mereproduksi, dan jangan sertakan nilai sungguhan dalam laporan.

## Cakupan

Celah yang termasuk dalam proyek ini, misalnya:

- Skrip mencetak channel access token atau channel secret, menuliskannya ke file atau cache, atau mengirimkannya ke host selain `api.line.me` dan `api-data.line.me`.
- `webhook_tools.py` mengirim channel secret itu sendiri (seharusnya hanya mengirim tanda tangan).
- Perintah tulis benar-benar dijalankan tanpa `--yes`, sehingga melewati dry-run.
- Path traversal atau command injection, misalnya path halaman dan cache di `line_docs.py`, atau argumen `--env-file` dan `@file` di `line_api.py` yang membaca atau menulis ke lokasi yang tidak semestinya.
- Instruksi di `SKILL.md` atau `references/` yang membuat asisten AI menjalankan operasi tulis tanpa persetujuan pengguna, membocorkan token, atau menjalankan isi dokumentasi yang diambilnya seolah-olah itu instruksi.

Yang tidak termasuk dalam proyek ini:

- Celah pada **platform LINE itu sendiri** (aplikasi LINE, Messaging API, LIFF, LINE Login): laporkan melalui [saluran resmi](https://bugbounty.linecorp.com/) LY Corporation.
- Celah pada **alat AI itu sendiri** (Claude Code, Codex, Copilot, dll.): laporkan ke pengembang alat tersebut.
- **Token Anda sendiri bocor**: ini bukan celah di proyek ini. Segera terbitkan ulang atau cabut token dan secret di [LINE Developers Console](https://developers.line.biz/console/).
- **Saran di daftar jebakan (gotchas) sudah usang atau kurang aman**, tetapi tidak melibatkan celah yang bisa dieksploitasi: cukup buka issue biasa (templat "Outdated LINE info or broken link").

## Proses penanganan

Ini adalah proyek open source yang dikelola secara pribadi, jadi tidak ada batas waktu respons yang pasti. Setelah laporan diterima, langkah berikut akan dilakukan secepatnya:

1. Mengonfirmasi bahwa laporan sudah diterima.
2. Memastikan masalah dan cakupan dampaknya, dan bila perlu menanyakan detail kepada Anda.
3. Setelah diperbaiki, merilis versi baru, memperbarui CHANGELOG, dan menjelaskannya secara publik melalui GitHub Security Advisory; jika Anda bersedia, ucapan terima kasih untuk Anda akan dicantumkan di pengumuman tersebut.

Jangan memublikasikan detail celah sebelum perbaikannya dirilis.

## Melindungi token Anda saat menggunakan skill

- Simpan token dan secret di variabel lingkungan atau di `.env` yang ditunjuk dengan `--env-file`; jangan mengetikkannya di baris perintah (akan tersimpan di riwayat shell dan daftar proses).
- Pastikan `.env` tercantum di `.gitignore`. Proyek yang dibuat oleh sebagian alat tidak mengabaikannya secara default (misalnya `supabase init`).
- Untuk operasi tulis, periksa dulu output dry-run, dan tambahkan `--yes` hanya setelah Anda yakin.
- Anda bisa membaca `SKILL.md` dan `scripts/` sebelum memasang; skill akan menjalankan skrip-skrip ini di komputer Anda atau di lingkungan eksekusi alat AI.

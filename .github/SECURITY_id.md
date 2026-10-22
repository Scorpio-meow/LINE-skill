# Kebijakan keamanan

[繁體中文](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY.md) | [English](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_en.md) | [日本語](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ja.md) | [ไทย](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_th.md) | **Bahasa Indonesia** | [한국어](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ko.md)

## Versi yang didukung

Perbaikan hanya dilakukan untuk versi terbaru, yaitu branch `main`. Jika Anda memakai versi lama, perbarui dulu (caranya ada di [README](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/README_id.md#memperbarui-dan-menghapus)).

## Melaporkan celah keamanan

**Jangan mengungkapkan detail celah keamanan di issue, Pull Request, atau diskusi publik.**

Laporkan secara privat melalui salah satu saluran berikut:

1. **Pelaporan privat GitHub (disarankan)**: buka tab **Security** di repo lalu klik **Report a vulnerability**, atau langsung buka [formulir pelaporan privat](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new). Hanya Anda dan pengelola yang bisa melihat laporannya.
2. **Email**: jika tidak bisa memakai GitHub, kirim email ke [yao921024@gmail.com](mailto:yao921024@gmail.com) dengan subjek yang diawali `[Security] LINE-skill`. Email tidak dienkripsi end-to-end, jadi tulis ringkasan masalahnya dulu dan kirim detailnya setelah Anda mendapat balasan.

Sertakan sebanyak mungkin informasi berikut:

- File dan versi yang terdampak (commit)
- Langkah untuk mereproduksi, serta dampak yang ditimbulkan
- Usulan perbaikan (opsional)

Gunakan token dan secret palsu saat mereproduksi, dan jangan sertakan nilai sungguhan dalam laporan.

## Proses dan tenggat penanganan

Proyek ini dikelola secara pribadi dan tidak memiliki program bug bounty, tetapi berkomitmen pada tenggat berikut:

| Tahap | Tenggat |
|---|---|
| Konfirmasi penerimaan dan balasan pertama | Dalam 14 hari setelah laporan diterima |
| Pengungkapan detail celah | Saat perbaikan dirilis, paling lambat 90 hari setelah laporan |

1. **Konfirmasi**: mengonfirmasi bahwa laporan sudah diterima dan menyampaikan penilaian awal.
2. **Penilaian**: memastikan apakah ini celah keamanan, beserta cakupan dampak dan tingkat keparahannya, dan bila perlu menanyakan detail kepada Anda; jika bukan celah keamanan, alasannya akan dijelaskan.
3. **Perbaikan**: mendiskusikan perbaikan bersama Anda di GitHub Security Advisory privat; Anda juga bisa mengirim perbaikan melalui fork privat di dalamnya.
4. **Rilis**: menggabungkan perbaikan ke `main`, memublikasikan Security Advisory, mengajukan nomor CVE melalui GitHub bila sesuai, dan mencatatnya di kategori Security pada [CHANGELOG](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/CHANGELOG.md).
5. **Ucapan terima kasih**: jika Anda bersedia, nama Anda akan dicantumkan di Advisory.

Jangan memublikasikan detail celah sebelum perbaikannya dirilis. Jika perbaikan tidak bisa selesai dalam 90 hari, alasannya akan dijelaskan sebelum tenggat dan tanggal pengungkapan baru akan disepakati bersama Anda.

## Cakupan

### Termasuk cakupan

Celah yang termasuk dalam proyek ini, misalnya:

- Skrip mencetak channel access token atau channel secret, menuliskannya ke file atau cache, atau mengirimkannya ke host selain `api.line.me` dan `api-data.line.me`.
- `webhook_tools.py` mengirim channel secret itu sendiri (seharusnya hanya mengirim tanda tangan).
- Perintah tulis benar-benar dijalankan tanpa `--yes`, sehingga melewati dry-run.
- Path traversal atau command injection, misalnya path halaman dan cache di `line_docs.py`, atau argumen `--env-file` dan `@file` di `line_api.py` yang membaca atau menulis ke lokasi yang tidak semestinya.
- Instruksi di `SKILL.md` atau `references/` yang membuat asisten AI menjalankan operasi tulis tanpa persetujuan pengguna, membocorkan token, atau menjalankan isi dokumentasi yang diambilnya seolah-olah itu instruksi.

### Di luar cakupan

- Celah pada **platform LINE itu sendiri** (aplikasi LINE, Messaging API, LIFF, LINE Login): laporkan melalui [saluran resmi](https://bugbounty.linecorp.com/) LY Corporation.
- Celah pada **alat AI itu sendiri** (Claude Code, Codex, Copilot, dll.): laporkan ke pengembang alat tersebut.
- **Token Anda sendiri bocor**: ini bukan celah di proyek ini. Segera terbitkan ulang atau cabut token dan secret di [LINE Developers Console](https://developers.line.biz/console/).
- **Saran di daftar jebakan (gotchas) sudah usang atau kurang aman**, tetapi tidak melibatkan celah yang bisa dieksploitasi: cukup buka issue biasa (templat "Outdated LINE info or broken link").

## Melindungi token Anda saat menggunakan skill

- Simpan token dan secret di variabel lingkungan atau di `.env` yang ditunjuk dengan `--env-file`; jangan mengetikkannya di baris perintah (akan tersimpan di riwayat shell dan daftar proses).
- Pastikan `.env` tercantum di `.gitignore`. Proyek yang dibuat oleh sebagian alat tidak mengabaikannya secara default (misalnya `supabase init`).
- Untuk operasi tulis, periksa dulu output dry-run, dan tambahkan `--yes` hanya setelah Anda yakin.
- Anda bisa membaca `SKILL.md` dan `scripts/` sebelum memasang; skill akan menjalankan skrip-skrip ini di komputer Anda atau di lingkungan eksekusi alat AI.

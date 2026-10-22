# Pernyataan aksesibilitas

[繁體中文](/.github/ACCESSIBILITY.md) | [English](/.github/ACCESSIBILITY_en.md) | [日本語](/.github/ACCESSIBILITY_ja.md) | [ไทย](/.github/ACCESSIBILITY_th.md) | **Bahasa Indonesia** | [한국어](/.github/ACCESSIBILITY_ko.md)

## Komitmen kami

Kami ingin pengembang yang memakai pembaca layar, pembesar layar, hanya keyboard, atau input suara, serta pengembang yang memakai bahasa yang berbeda-beda, semuanya bisa memasang, membaca, dan menggunakan skill ini, sekaligus ikut berkontribusi.

## Bentuk proyek ini

Proyek ini tidak memiliki halaman web atau antarmuka grafis. Isinya adalah:

- Dokumen Markdown: README dalam enam bahasa, `SKILL.md`, `references/`
- Tiga skrip Python untuk baris perintah
- Materi uji yang dipakai untuk pengembangan

Anda menggunakannya melalui alat AI dan terminal Anda sendiri, sehingga tingkat aksesibilitas alat-alat tersebut juga memengaruhi pengalaman penggunaan.

## Yang sudah dilakukan

- Skrip hanya menghasilkan teks biasa, tanpa memakai warna, kontrol kursor, atau animasi untuk menyampaikan informasi; semua operasi bisa dilakukan di baris perintah hanya dengan keyboard.
- Skrip mengatur standard output ke UTF-8 untuk mengurangi karakter rusak saat konsol Windows menampilkan teks bahasa Tionghoa, Jepang, Thai, dan Korea.
- Dokumen dibagi per bagian dengan judul Markdown, sehingga Anda bisa melompat ke bagian yang diperlukan dengan navigasi judul di pembaca layar.
- README tersedia dalam enam bahasa: 繁體中文, English, 日本語, ไทย, Bahasa Indonesia, 한국어.
- Saat membantu Anda mengembangkan bot LINE, skill akan mengingatkan agar pesan seperti Flex Message diberi `altText`: teks ini muncul di notifikasi, daftar chat, dan pratinjau kutipan.

## Keterbatasan yang diketahui

- Bagian "Folder skill per alat" di README berupa tabel 5 kolom dan 12 baris yang sulit dibaca dengan pembaca layar atau di layar sempit.
- Bagian "Isi" di README menggambar pohon direktori dengan karakter garis (`├──`, `└──`), dan pembaca layar mungkin membacakan simbol-simbol ini satu per satu.
- `SKILL.md` dan `references/` hanya tersedia dalam bahasa Inggris (terutama untuk dibaca AI); pesan skrip dan bantuan `-h` juga hanya dalam bahasa Inggris.
- README selain bahasa Tionghoa Tradisional adalah terjemahan dan mungkin diperbarui lebih lambat; jika isinya berbeda, yang berlaku adalah [versi bahasa Tionghoa Tradisional](/README.md).
- Antarmuka pemasangan di Claude, ChatGPT, Codex, dan alat lainnya disediakan oleh masing-masing vendor, sehingga tingkat aksesibilitasnya di luar kendali proyek ini.
- Kami belum melakukan pengujian sistematis dengan pembaca layar tertentu.

## Lingkungan yang didukung

- macOS, Linux, Windows (PowerShell, Windows Terminal), dengan Python 3.8 atau lebih baru.
- Terminal apa pun yang bisa menampilkan teks UTF-8.
- Dokumen bisa dibaca di situs GitHub atau penampil Markdown apa pun, dan juga bisa dibuka langsung dengan editor teks biasa.

## Melaporkan hambatan

[Buka issue "Accessibility barrier" (hambatan aksesibilitas)](https://github.com/Scorpio-meow/LINE-skill/issues/new?template=accessibility.yml), lalu jelaskan di mana Anda mengalaminya, teknologi bantu dan lingkungan yang Anda pakai, serta kesulitan yang Anda hadapi. Jika tidak nyaman melaporkannya secara publik, Anda bisa mengirim email ke yao921024@gmail.com. Ini adalah proyek yang dikelola secara pribadi dan tidak memiliki batas waktu respons yang pasti, tetapi setiap laporan akan dibaca dengan serius.

Kami juga menyambut saran tentang hal-hal aksesibilitas apa lagi yang sebaiknya diingatkan skill saat membantu Anda mengembangkan bot LINE.

Terakhir diperbarui: 2026-10-21

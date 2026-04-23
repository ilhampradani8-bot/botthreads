# Integrasi Posting Otomatis Threads - MIJ Digital Malaysia

Sistem ini dirancang untuk memposting konten IT secara otomatis ke platform Threads menggunakan **Buffer API** dan **Groq AI**. Konten dibuat secara natural dalam Bahasa Malaysia, fokus pada SEO, dan tanpa watermark.

## 1. Persiapan Kredensial (.env)

Pastikan file `.env` di direktori utama memiliki data berikut:

- `GROQ_API_KEY`: API Key dari [groq.com](https://groq.com/) (Penyedia AI Llama 3).
- `BUFFER_ACCESS_TOKEN`: Access Token dari dashboard Buffer.
- `BUFFER_CHANNEL_ID`: ID unik untuk channel Threads Anda di Buffer.

## 2. Struktur Program

Sistem berada di dalam folder `mij-bot/`:

- **`bot.py`**: Mesin utama yang memanggil AI Groq untuk membuat konten IT singkat (1-2 kalimat), tanpa hashtag, lalu mengirimnya ke Buffer.
- **`mesin_jadwal.py`**: Scheduler yang mengatur waktu posting secara acak 4-5 kali sehari agar terlihat seperti postingan manusia manual.

## 3. Cara Penggunaan (Mudah)

Gunakan script `manage_bot.sh` untuk mengatur bot dengan satu perintah:

- **Mulai Bot**: `./manage_bot.sh start`
- **Berhentikan Bot**: `./manage_bot.sh stop`
- **Restart Bot**: `./manage_bot.sh restart`
- **Lihat Log/Aktivitas**: `./manage_bot.sh logs`
- **Cek Status**: `./manage_bot.sh status`

---

## 4. Jalankan Otomatis Saat Laptop Hidup (Reboot)

Agar bot otomatis berjalan sendiri setiap kali laptop dinyalakan:
1. Jalankan `crontab -e` di terminal.
2. Tambahkan baris ini di paling bawah:
   ```cron
   @reboot /home/ilham/botthreads/manage_bot.sh start
   ```
3. Simpan dan keluar.

---

## 5. Monitoring & FAQ

---

## FAQ & Penanganan Error

### 1. Postingan Tidak Muncul di Threads?
- Cek `posting.log`. Jika ada error `401`, berarti Token Buffer sudah kedaluwarsa atau salah.
- Jika ada error `403`, cek apakah akun Threads sudah terhubung dengan benar di dashboard Buffer.

### 2. Bagaimana Cara Memberhentikan Bot?
Jika ingin mematikan bot secara paksa, jalankan:
```bash
pkill -f mesin_jadwal.py
```

### 3. Kenapa Tidak Ada Hashtag?
Sesuai permintaan, bot ini menggunakan gaya bahasa **natural**. SEO Threads bekerja lebih baik dengan kata kunci di dalam kalimat daripada tumpukan hashtag yang terlihat seperti spam.

### 4. Batasan Karakter
Threads memiliki batas 500 karakter. Bot ini sudah diatur secara ketat untuk hanya menghasilkan **300-400 karakter** agar postingan tidak pernah terpotong.

# Scraper Riset — Kekerasan Seksual di Pendidikan Tinggi Indonesia

Panduan cepat untuk memulai pengambilan data dari YouTube dan portal berita.

---

## Isi Folder

```
kekerasan_seksual_scraper\
├── SETUP_WINDOWS.bat              ← Klik 2x PERTAMA KALI (install otomatis)
├── JALANKAN_SCRAPER.bat           ← Klik 2x untuk mulai scraping
├── .env.example                   ← Template API key → rename jadi .env
├── 01_youtube_scraper.py          ← Scraper YouTube (butuh API key)
├── 02_news_scraper.py             ← Scraper berita (RSS gratis + NewsAPI opsional)
├── 03_twitter_scraper.py          ← Twitter (skip dulu — berbayar)
├── 04_tiktok_scraper.py           ← TikTok (butuh approval kampus)
├── 05_ekstrak_universitas_v2.py   ← Ekstrak universitas & buat Excel riset
└── data\                          ← Semua output CSV dan Excel tersimpan di sini
```

---

## LANGKAH 1 — Install Python

1. Buka **https://www.python.org/downloads/**
2. Download dan jalankan installer
3. **PENTING:** Centang **"Add Python to PATH"** di bagian bawah installer!
4. Klik Install Now

Cek di Command Prompt:
```
python --version
```

---

## LANGKAH 2 — Setup Project

Klik 2x file **`SETUP_WINDOWS.bat`** — tunggu sampai selesai.

---

## LANGKAH 3 — Buat File .env

1. Duplikat file `.env.example`
2. Rename hasil duplikat menjadi `.env` (hapus `.example`-nya)
3. Buka `.env` dengan Notepad
4. Isi API key:

```
YOUTUBE_API_KEY=AIzaSy...    ← dari Google Cloud Console
NEWS_API_KEY=abc123...        ← dari newsapi.org (opsional)
```

### Cara dapat YouTube API Key:
1. Buka https://console.cloud.google.com
2. Buat project baru
3. Cari "YouTube Data API v3" → klik Enable
4. Pilih Credentials → Create Credentials → API Key
5. Salin key ke file .env

---

## LANGKAH 4 — Jalankan Scraper

Klik 2x **`JALANKAN_SCRAPER.bat`** → pilih platform dari menu.

Atau manual:
```cmd
venv\Scripts\activate
python 01_youtube_scraper.py   ← YouTube
python 02_news_scraper.py      ← Berita
```

---

## LANGKAH 5 — Ekstrak Universitas & Buat Excel Riset

Setelah data CSV terkumpul di folder `data\`, jalankan **opsi [5]** dari menu
atau manual:

```cmd
venv\Scripts\activate
python 05_ekstrak_universitas_v2.py
```

Script ini akan:
1. Membaca **semua file CSV** di folder `data\`
2. Mendeteksi nama universitas, kota, provinsi, status PTN/PTS
3. Mengidentifikasi jenis kekerasan dan pelaku
4. Menghasilkan **Excel riset multi-sheet** (10 sheet) termasuk:
   - Data Lengkap, Per Universitas, Per Provinsi, Per Kota
   - Jenis Kekerasan, Pelaku, Tabel Silang, Tren per Tahun
   - Dashboard Ringkasan, Panduan & Legenda

---

## Keyword yang Sudah Dikonfigurasi

Script sudah otomatis mencari dengan 7-8 keyword berikut:

- kekerasan seksual kampus
- pelecehan seksual mahasiswa
- PPKS perguruan tinggi
- kekerasan seksual dosen mahasiswa
- kasus pelecehan seksual universitas
- sexual harassment kampus indonesia
- korban kekerasan seksual kampus
- satgas PPKS kampus

---

## Output

Semua file tersimpan di folder `data\` dengan nama otomatis pakai timestamp:

| File | Isi |
|------|-----|
| `youtube_video_YYYYMMDD_HHMM.csv` | Data video (judul, views, likes, url) |
| `youtube_video_YYYYMMDD_HHMM.xlsx` | Sama, format Excel |
| `youtube_komentar_YYYYMMDD_HHMM.csv` | Komentar publik per video |
| `berita_YYYYMMDD_HHMM.csv` | Artikel dari media online |
| `berita_YYYYMMDD_HHMM.xlsx` | Sama, format Excel |
| `RISET_kekerasan_seksual_PT_YYYYMMDD_HHMM.xlsx` | **Excel riset 10-sheet** (dari langkah 5) |

---

## Batas Quota (Gratis)

| Platform | Limit |
|----------|-------|
| YouTube API | 10.000 unit/hari (reset pukul 15:00 WIB) |
| NewsAPI | 100 request/hari |
| RSS Feed | Tidak terbatas |

---

## Masalah Umum

**"python bukan perintah internal"**
→ Python belum di PATH. Uninstall, install ulang, centang "Add Python to PATH"

**"ModuleNotFoundError"**
→ Jalankan ulang `SETUP_WINDOWS.bat`

**"YOUTUBE_API_KEY tidak ditemukan"**
→ File `.env` belum dibuat atau nama file salah (pastikan bukan `.env.txt`)
→ Di Windows Explorer: aktifkan View → File name extensions

**Quota YouTube habis (Error 403)**
→ Tunggu reset besok pukul 15:00 WIB, atau buat project baru di Google Cloud

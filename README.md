# SIGAP — Sistem Informasi & Geospasial Anti-Kekerasan Seksual

SIGAP adalah platform komprehensif untuk pengumpulan data, analisis, dan visualisasi spasial terkait krisis kekerasan seksual di perguruan tinggi Indonesia.

---

## 🏗️ Arsitektur Proyek

Proyek ini terdiri dari tiga komponen utama:

1.  **Data Scraper (Python)**: Pipeline otomatis untuk mengumpulkan data dari YouTube, portal berita, dan media sosial.
2.  **Web Portal (Next.js)**: Portal interaktif premium dengan peta geospasial dan *data storytelling*.
3.  **Analysis Dashboard (Streamlit)**: Dashboard analitik mendalam untuk mengeksplorasi tren dan metrik statistik.

---

## 📂 Struktur Folder

```
kekerasan_seksual_scraper/
├── sigap_web/             ← Portal Utama (Next.js)
├── streamlit_app/         ← Dashboard Analitik (Streamlit)
├── scraper/               ← Pipeline Data Scraper (Python)
├── data/                  ← Database hasil scraping (JSON & Excel)
├── SETUP_WINDOWS.bat      ← Setup otomatis untuk Windows
└── JALANKAN_SCRAPER.bat   ← Menu utama untuk menjalankan sistem
```

---

## 🚀 Cara Menjalankan Lokal

### 1. Prasyarat
- Python 3.9+
- Node.js 18+
- Git

### 2. Setup Cepat (Windows)
Klik 2x file **`SETUP_WINDOWS.bat`**. Script ini akan:
- Membuat virtual environment Python.
- Menginstall dependensi scraper & streamlit.
- Menginstall `node_modules` untuk portal web.

### 3. Menjalankan Komponen
- **Web Portal**: `cd sigap_web && npm run dev` (Akses di http://localhost:3000)
- **Streamlit**: `streamlit run streamlit_app/app.py` (Akses di http://localhost:8501)
- **Scraper**: Klik 2x `JALANKAN_SCRAPER.bat`

---

## ☁️ Panduan Deployment (GitHub)

### 1. Persiapan Repositori
Kami telah menginisialisasi Git di folder ini. Untuk memindahkan ke GitHub Anda:
```bash
git remote add origin https://github.com/USERNAME/NAMA_REPO.git
git branch -M main
git push -u origin main
```

### 2. Deploy Portal Web (Next.js)
Gunakan **[Vercel](https://vercel.com)**:
- Hubungkan akun GitHub Anda.
- Pilih folder `sigap_web` sebagai root directory.
- Build command: `npm run build`
- Install command: `npm install`

### 3. Deploy Analysis Dashboard (Streamlit)
Gunakan **[Streamlit Cloud](https://share.streamlit.io/)**:
- Hubungkan akun GitHub Anda.
- Pilih file `streamlit_app/app.py` sebagai entry point.

---

## 🛠️ Konfigurasi API
Buat file `.env` di root untuk menjalankan scraper:
```env
YOUTUBE_API_KEY=AIzaSy...
NEWS_API_KEY=abc123...
```

---

## ⚖️ Lisensi & Kontribusi
Proyek ini dikembangkan untuk tujuan riset dan advokasi. Kontribusi sangat disambut untuk meningkatkan akurasi ekstraksi data dan jangkauan visualisasi.

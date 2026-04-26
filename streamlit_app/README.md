# SIGAP Dashboard — Selesai Dibangun ✅

Dashboard Streamlit untuk statistik kekerasan seksual di perguruan tinggi Indonesia.

## Cara Menjalankan

```bash
cd kekerasan_seksual_scraper
streamlit run streamlit_app/app.py
```

Buka browser ke: **http://localhost:8501**

---

## Struktur Folder

```
streamlit_app/
├── app.py                       # Entry point
├── requirements.txt
├── .streamlit/
│   └── config.toml              # Dark theme config
├── assets/
│   └── style.css                # IDX-style + dark cinematic CSS
├── components/
│   ├── navbar.py                # Navbar, hero, stat cards
│   ├── charts.py                # Semua chart Plotly
│   └── storytelling.py          # Auto-narasi Indonesia
└── pages/
    ├── beranda.py               # 🏠 Homepage portal
    ├── statistik.py             # 📊 5-tab dashboard
    ├── peta_sebaran.py          # 🗺️ Peta interaktif
    ├── media_sosial.py          # 📱 YouTube & Berita
    └── analisis_mandiri.py      # 📤 Upload + auto story
```

## Halaman & Fitur

| Halaman | Fitur Utama |
|---|---|
| 🏠 Beranda | Hero headline, ticker berita, 4 metric cards, tren chart, berita terbaru, YouTube highlights |
| 📊 Statistik | 5 tabs: Tren, Jenis+Pelaku, Universitas, Provinsi, Heatmap Bulanan — semua dengan narasi |
| 🗺️ Peta | Bubble map per Provinsi & Universitas, **klik lokasi → detail kasus + berita** |
| 📱 Media | YouTube: top videos, engagement, channel analysis. Berita: volume per bulan, keyword |
| 📤 Upload | Drag-drop Excel/CSV, auto-deteksi kolom, manual mapping, auto chart + narasi |

## Screenshot

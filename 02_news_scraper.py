"""
================================================================================
  BERITA SCRAPER - Riset Kekerasan Seksual di Lingkungan Pendidikan Tinggi
  Sumber : NewsAPI.org (gratis 100 req/hari) + RSS Feed (gratis total)
  Platform: Windows 10/11
================================================================================
  Cara pakai:
    1. (Opsional) Daftar NewsAPI di https://newsapi.org/register
    2. Isi NEWS_API_KEY di file .env  (kosongkan jika tidak punya — RSS tetap jalan)
    3. Klik 2x JALANKAN_SCRAPER.bat  ATAU
       Buka Command Prompt lalu ketik: python 02_news_scraper.py
================================================================================
"""

import requests
import pandas as pd
import os
import time
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ── KONFIGURASI ────────────────────────────────────────────────────────────────
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# Daftar keyword riset — semua akan dijalankan otomatis
DAFTAR_KEYWORD = [
    "peningkatan kekerasan seksual kampus",
    "statistik kekerasan seksual universitas",
    "data kasus kekerasan seksual pendidikan tinggi",
    "kasus kekerasan seksual meningkat kampus",
    "lonjakan pelecehan seksual mahasiswa",
    "catatan tahunan kekerasan seksual kampus",
]

HARI_LALU   = 30    # Cari berita berapa hari ke belakang (NewsAPI)
GUNAKAN_RSS = True  # True = ambil dari RSS Feed gratis juga

# RSS Feed media Indonesia - gratis, tanpa API key
RSS_FEEDS = {
    "Google News": "https://news.google.com/rss/search?q={keyword}&hl=id&gl=ID&ceid=ID:id",
    "Kompas":      "https://www.kompas.com/tag/kekerasan-seksual?format=rss",
    "Detik":       "https://www.detik.com/tag/kekerasan-seksual/rss",
    "Tempo":       "https://rss.tempo.co",
}


# ── 1. NEWSAPI ─────────────────────────────────────────────────────────────────
def ambil_newsapi(keyword, hari=30, bahasa="id", max_artikel=100):
    """Ambil berita dari NewsAPI berdasarkan keyword."""
    if not NEWS_API_KEY:
        print("  [SKIP] NEWS_API_KEY tidak ada — melewati NewsAPI, pakai RSS saja")
        return []

    dari_tanggal = (datetime.now() - timedelta(days=hari)).strftime("%Y-%m-%d")
    semua  = []
    halaman = 1
    print(f"\n  [NewsAPI] Mencari: '{keyword}'")

    while len(semua) < max_artikel:
        params = {
            "q":        keyword,
            "from":     dari_tanggal,
            "language": bahasa,
            "sortBy":   "publishedAt",
            "pageSize": min(100, max_artikel - len(semua)),
            "page":     halaman,
            "apiKey":   NEWS_API_KEY,
        }
        try:
            resp = requests.get("https://newsapi.org/v2/everything", params=params, timeout=15)
            if resp.status_code == 401:
                print("  [ERROR] API key NewsAPI tidak valid!")
                break
            if resp.status_code == 429:
                print("  [WAIT] Rate limit! Tunggu 60 detik...")
                time.sleep(60)
                continue
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] {e}")
            break

        articles = data.get("articles", [])
        if not articles:
            break

        for art in articles:
            semua.append({
                "judul":     art.get("title", ""),
                "sumber":    art.get("source", {}).get("name", ""),
                "penulis":   art.get("author", ""),
                "deskripsi": art.get("description", ""),
                "url":       art.get("url", ""),
                "tanggal":   art.get("publishedAt", ""),
                "konten":    (art.get("content") or "")[:500],
                "keyword":   keyword,
                "metode":    "NewsAPI",
            })

        total = data.get("totalResults", 0)
        print(f"  Hal.{halaman}: +{len(articles)} artikel | Total: {len(semua)}/{total}")
        if len(semua) >= total or len(semua) >= max_artikel:
            break
        halaman += 1
        time.sleep(0.5)

    return semua


# ── 2. RSS FEED ────────────────────────────────────────────────────────────────
def ambil_rss(nama_sumber, url_rss, keyword_filter=None):
    """
    Ambil berita dari RSS Feed — gratis, tanpa API key.
    """
    # Jika Google News, format URL dengan keyword
    if nama_sumber == "Google News" and keyword_filter:
        import urllib.parse
        encoded_kw = urllib.parse.quote(keyword_filter)
        url_rss = url_rss.format(keyword=encoded_kw)
    
    print(f"\n  [RSS] {nama_sumber}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(url_rss, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"  [WARN] Gagal ambil RSS {nama_sumber}: {e}")
        return []

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f"  [WARN] Gagal parse XML {nama_sumber}: {e}")
        return []

    ns    = {"atom": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall(".//atom:entry", ns)

    hasil = []
    for item in items:
        def teks(tag, ns_pfx=None):
            el = item.find(f"{ns_pfx}:{tag}", ns) if ns_pfx else item.find(tag)
            return (el.text or "").strip() if el is not None else ""

        judul     = teks("title")
        deskripsi = teks("description") or teks("summary", "atom")
        # Google News RSS has links in <link> tags
        link_el = item.find("link")
        url = link_el.text if link_el is not None else ""
        tanggal   = teks("pubDate") or teks("published", "atom")

        # Filter jika bukan dari Google News (karena Google News sudah di-filter di URL)
        if nama_sumber != "Google News" and keyword_filter:
            if keyword_filter.lower() not in (judul + deskripsi).lower():
                continue

        hasil.append({
            "judul":     judul,
            "sumber":    nama_sumber,
            "penulis":   "",
            "deskripsi": (deskripsi or "")[:400],
            "url":       url,
            "tanggal":   tanggal,
            "konten":    "",
            "keyword":   keyword_filter or "",
            "metode":    "RSS",
        })

    print(f"  Ditemukan: {len(hasil)} artikel relevan")
    return hasil


# ── 3. SIMPAN DATA ─────────────────────────────────────────────────────────────
def simpan_data(data_list, ts):
    if not data_list:
        print("  [WARN] Tidak ada data.")
        return
    df = pd.DataFrame(data_list)
    df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce", utc=True)
    df["tanggal"] = df["tanggal"].dt.tz_localize(None)
    df = df.drop_duplicates(subset="url")
    df = df.dropna(subset=["judul"])
    df = df.sort_values("tanggal", ascending=False).reset_index(drop=True)

    os.makedirs("data", exist_ok=True)

    path_csv = os.path.join("data", f"berita_{ts}.csv")
    df.to_csv(path_csv, index=False, encoding="utf-8-sig")
    print(f"  [OK] {path_csv} ({len(df)} artikel)")

    path_xlsx = os.path.join("data", f"berita_{ts}.xlsx")
    with pd.ExcelWriter(path_xlsx, engine="openpyxl") as w:
        df.to_excel(w, sheet_name="Berita", index=False)
        ws = w.sheets["Berita"]
        for col in ws.columns:
            mx = max((len(str(c.value)) for c in col if c.value), default=10)
            ws.column_dimensions[col[0].column_letter].width = min(mx + 4, 80)
    print(f"  [OK] {path_xlsx}")


# ── 4. MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    print("=" * 65)
    print("  BERITA SCRAPER (NewsAPI + RSS)")
    print("  Topik : Kekerasan Seksual di Pendidikan Tinggi Indonesia")
    print(f"  Mulai : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 65)

    semua_artikel = []

    for idx, keyword in enumerate(DAFTAR_KEYWORD, 1):
        print(f"\n[{idx}/{len(DAFTAR_KEYWORD)}] -- '{keyword}'")

        # NewsAPI
        art_api = ambil_newsapi(keyword, hari=HARI_LALU)
        semua_artikel.extend(art_api)

        # RSS Feed (filter per keyword)
        if GUNAKAN_RSS:
            for nama, url in RSS_FEEDS.items():
                art_rss = ambil_rss(nama, url, keyword_filter=keyword)
                semua_artikel.extend(art_rss)
                time.sleep(0.5)

        if idx < len(DAFTAR_KEYWORD):
            time.sleep(2)

    print(f"\n{'=' * 65}")
    print(f"  Total artikel terkumpul: {len(semua_artikel)}")
    print("  MENYIMPAN DATA...")
    simpan_data(semua_artikel, ts)

    print(f"\n{'=' * 65}")
    print(f"  SELESAI: {datetime.now().strftime('%H:%M:%S')}")
    print(f"  Output folder: data\\")
    print(f"{'=' * 65}")
    input("\n  Tekan ENTER untuk keluar...")

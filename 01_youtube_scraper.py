"""
================================================================================
  YOUTUBE SCRAPER - Riset Kekerasan Seksual di Lingkungan Pendidikan Tinggi
  Platform : Windows 10/11
  Kebutuhan: Python 3.8+, pip install requests pandas openpyxl python-dotenv
================================================================================
  Cara pakai:
    1. Isi YOUTUBE_API_KEY di file .env
    2. Klik 2x JALANKAN_SCRAPER.bat  ATAU
       Buka Command Prompt lalu ketik: python 01_youtube_scraper.py
    3. Hasil tersimpan di folder  data\
================================================================================
"""

import requests
import pandas as pd
import os
import time
import sys
from datetime import datetime
from dotenv import load_dotenv

# ── 1. LOAD API KEY ────────────────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    print("=" * 60)
    print("  ERROR: YOUTUBE_API_KEY tidak ditemukan di file .env!")
    print("  Buka file .env dan isi API key Anda.")
    print("  Cara daftar: https://console.cloud.google.com")
    print("=" * 60)
    sys.exit(1)

BASE_URL = "https://www.googleapis.com/youtube/v3"

# ── 2. DAFTAR KEYWORD RISET ────────────────────────────────────────────────────
# Semua keyword terkait kekerasan seksual di lingkungan pendidikan tinggi.
# Scraper akan berjalan satu per satu secara otomatis.
DAFTAR_KEYWORD = [
    "kekerasan seksual kampus",
    "pelecehan seksual mahasiswa",
    "PPKS perguruan tinggi",
    "kekerasan seksual dosen mahasiswa",
    "kasus pelecehan seksual universitas",
    "sexual harassment kampus indonesia",
    "korban kekerasan seksual kampus",
    "satgas PPKS kampus",
]

# ── 3. KONFIGURASI ─────────────────────────────────────────────────────────────
MAX_RESULTS      = 50   # Jumlah video per keyword
AMBIL_KOMENT     = True # True = ambil komentar juga
MAX_KOMENT       = 100  # Jumlah komentar per video
MAX_VIDEO_KOMENT = 10   # Ambil komentar dari N video teratas per keyword


# ── 4. FUNGSI AMBIL DATA ───────────────────────────────────────────────────────
def get_video_stats(video_ids):
    """Ambil statistik (views, likes, komentar) dari list video ID."""
    if not video_ids:
        return {}
    params = {
        "part": "statistics,contentDetails",
        "id":   ",".join(video_ids),
        "key":  API_KEY,
    }
    try:
        resp = requests.get(f"{BASE_URL}/videos", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"  [WARN] Gagal ambil statistik: {e}")
        return {}
    result = {}
    for item in data.get("items", []):
        vid_id = item["id"]
        stats  = item.get("statistics", {})
        detail = item.get("contentDetails", {})
        result[vid_id] = {
            "view_count":    int(stats.get("viewCount",    0)),
            "like_count":    int(stats.get("likeCount",    0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "duration":      detail.get("duration", ""),
        }
    return result


def search_videos(keyword, max_results=50, language="id"):
    """Cari video YouTube berdasarkan keyword."""
    all_videos = []
    next_page  = None
    halaman    = 1
    print(f"\n  Mencari: '{keyword}' (target {max_results} video)...")
    while len(all_videos) < max_results:
        sisa = max_results - len(all_videos)
        params = {
            "part":              "snippet",
            "q":                 keyword,
            "type":              "video",
            "maxResults":        min(50, sisa),
            "relevanceLanguage": language,
            "key":               API_KEY,
        }
        if next_page:
            params["pageToken"] = next_page
        try:
            resp = requests.get(f"{BASE_URL}/search", params=params, timeout=15)
            if resp.status_code == 429:
                print("  [WAIT] Rate limit! Tunggu 60 detik...")
                time.sleep(60)
                continue
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.ConnectionError:
            print("  [ERROR] Tidak ada koneksi internet.")
            break
        except requests.exceptions.Timeout:
            print("  [WARN] Timeout. Coba lagi...")
            time.sleep(5)
            continue
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 403:
                print("  [ERROR] API key tidak valid atau quota habis!")
                print(f"          {resp.json().get('error', {}).get('message', '')}")
            else:
                print(f"  [ERROR] HTTP {resp.status_code}: {e}")
            break
        items = data.get("items", [])
        if not items:
            print("  Tidak ada hasil lagi.")
            break
        video_ids = [i["id"]["videoId"] for i in items if i.get("id", {}).get("videoId")]
        stats_map = get_video_stats(video_ids)
        for item in items:
            vid_id = item.get("id", {}).get("videoId")
            if not vid_id:
                continue
            snip  = item.get("snippet", {})
            stats = stats_map.get(vid_id, {})
            all_videos.append({
                "video_id":       vid_id,
                "judul":          snip.get("title", ""),
                "channel":        snip.get("channelTitle", ""),
                "tanggal_tayang": snip.get("publishedAt", ""),
                "deskripsi":      snip.get("description", "")[:300],
                "views":          stats.get("view_count",    0),
                "likes":          stats.get("like_count",    0),
                "komentar":       stats.get("comment_count", 0),
                "url":            f"https://www.youtube.com/watch?v={vid_id}",
                "keyword":        keyword,
            })
        print(f"  Halaman {halaman}: +{len(items)} video | Total: {len(all_videos)}")
        halaman  += 1
        next_page = data.get("nextPageToken")
        if not next_page:
            break
        time.sleep(0.5)
    return all_videos


def ambil_komentar(video_id, max_komentar=100):
    """Ambil komentar dari sebuah video."""
    komentar_list = []
    next_page     = None
    while len(komentar_list) < max_komentar:
        params = {
            "part":       "snippet",
            "videoId":    video_id,
            "maxResults": min(100, max_komentar - len(komentar_list)),
            "order":      "relevance",
            "key":        API_KEY,
        }
        if next_page:
            params["pageToken"] = next_page
        try:
            resp = requests.get(f"{BASE_URL}/commentThreads", params=params, timeout=10)
            if resp.status_code == 403:
                break  # Komentar dinonaktifkan
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException:
            break
        for item in data.get("items", []):
            top = item["snippet"]["topLevelComment"]["snippet"]
            komentar_list.append({
                "video_id":  video_id,
                "penulis":   top.get("authorDisplayName", ""),
                "komentar":  top.get("textDisplay", ""),
                "likes":     top.get("likeCount", 0),
                "tanggal":   top.get("publishedAt", ""),
                "url_video": f"https://www.youtube.com/watch?v={video_id}",
            })
        next_page = data.get("nextPageToken")
        if not next_page:
            break
        time.sleep(0.3)
    return komentar_list


# ── 5. SIMPAN DATA ─────────────────────────────────────────────────────────────
def simpan_data(data_list, nama_csv, nama_xlsx, key_dedup, sort_by=None):
    """Simpan ke CSV dan Excel."""
    if not data_list:
        print("  [WARN] Tidak ada data.")
        return
    df = pd.DataFrame(data_list)
    if "tanggal_tayang" in df.columns:
        df["tanggal_tayang"] = pd.to_datetime(
            df["tanggal_tayang"], errors="coerce", utc=True
        ).dt.tz_localize(None)
    if key_dedup in df.columns:
        df = df.drop_duplicates(subset=key_dedup)
    if sort_by and sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=False).reset_index(drop=True)
    os.makedirs("data", exist_ok=True)
    df.to_csv(os.path.join("data", nama_csv), index=False, encoding="utf-8-sig")
    print(f"  [OK] {nama_csv}  ({len(df)} baris)")
    with pd.ExcelWriter(os.path.join("data", nama_xlsx), engine="openpyxl") as w:
        df.to_excel(w, sheet_name="Data", index=False)
        ws = w.sheets["Data"]
        for col in ws.columns:
            mx = max((len(str(c.value)) for c in col if c.value), default=10)
            ws.column_dimensions[col[0].column_letter].width = min(mx + 4, 60)
    print(f"  [OK] {nama_xlsx}")


# ── 6. MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    print("=" * 65)
    print("  YOUTUBE SCRAPER")
    print("  Topik : Kekerasan Seksual di Pendidikan Tinggi Indonesia")
    print(f"  Mulai : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"  Keyword: {len(DAFTAR_KEYWORD)} kata kunci")
    print("=" * 65)

    semua_video    = []
    semua_komentar = []

    for idx, keyword in enumerate(DAFTAR_KEYWORD, 1):
        print(f"\n[{idx}/{len(DAFTAR_KEYWORD)}] -- '{keyword}'")
        videos = search_videos(keyword, max_results=MAX_RESULTS)
        semua_video.extend(videos)

        if AMBIL_KOMENT and videos:
            print(f"\n  Ambil komentar dari {MAX_VIDEO_KOMENT} video teratas...")
            for i, vid in enumerate(videos[:MAX_VIDEO_KOMENT], 1):
                print(f"  [{i}/{MAX_VIDEO_KOMENT}] {vid['judul'][:55]}...")
                koms = ambil_komentar(vid["video_id"], max_komentar=MAX_KOMENT)
                semua_komentar.extend(koms)
                time.sleep(0.5)

        if idx < len(DAFTAR_KEYWORD):
            print("\n  Jeda 3 detik...")
            time.sleep(3)

    print(f"\n{'=' * 65}")
    print("  MENYIMPAN DATA...")
    simpan_data(semua_video,    f"youtube_video_{ts}.csv",    f"youtube_video_{ts}.xlsx",    "video_id", "views")
    if semua_komentar:
        simpan_data(semua_komentar, f"youtube_komentar_{ts}.csv", f"youtube_komentar_{ts}.xlsx", "komentar", "likes")

    print(f"\n{'=' * 65}")
    print(f"  SELESAI: {datetime.now().strftime('%H:%M:%S')}")
    print(f"  Total video    : {len(semua_video)}")
    print(f"  Total komentar : {len(semua_komentar)}")
    print(f"  Output folder  : data\\")
    print(f"{'=' * 65}")
    input("\n  Tekan ENTER untuk keluar...")

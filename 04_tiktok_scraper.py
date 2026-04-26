"""
================================================================================
  TIKTOK SCRAPER - Ambil data video TikTok ke CSV / Excel
  API     : TikTok Research API (untuk peneliti/akademisi)
  Platform: Windows 10/11
================================================================================
  Cara daftar Research API:
    1. Buka https://developers.tiktok.com/products/research-api/
    2. Klik "Apply for Access"
    3. Isi form — butuh afiliasi institusi (kampus/perusahaan)
    4. Tunggu approval 2-4 minggu
    5. Setelah approved, buat app → dapatkan Client Key & Client Secret
    6. Isi di file .env:
         TIKTOK_CLIENT_KEY=...
         TIKTOK_CLIENT_SECRET=...
================================================================================
  ALTERNATIF tanpa API (untuk belajar):
    - Gunakan snscrape (tidak resmi, bisa kena blokir)
    - Gunakan Apify TikTok Scraper (berbayar, mudah)
================================================================================
"""

import requests
import pandas as pd
import os
import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CLIENT_KEY    = os.getenv("TIKTOK_CLIENT_KEY", "")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")

if not CLIENT_KEY or not CLIENT_SECRET:
    print("=" * 60)
    print("  TIKTOK_CLIENT_KEY atau TIKTOK_CLIENT_SECRET")
    print("  tidak ditemukan di .env!")
    print()
    print("  Daftar Research API di:")
    print("  https://developers.tiktok.com/products/research-api/")
    print()
    print("  Sambil menunggu approval, coba jalankan:")
    print("  python 01_youtube_scraper.py  (tidak perlu approval)")
    print("=" * 60)
    sys.exit(1)


# ── 1. AUTENTIKASI (Client Credentials) ──────────────────────────────────────
def get_access_token():
    """
    Dapatkan access token menggunakan Client Credentials flow.
    Token berlaku 2 jam, perlu diperbarui setelahnya.
    """
    resp = requests.post(
        "https://open.tiktokapis.com/v2/oauth/token/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_key":    CLIENT_KEY,
            "client_secret": CLIENT_SECRET,
            "grant_type":    "client_credentials",
        },
        timeout=15,
    )

    if resp.status_code != 200:
        print(f"  [ERROR] Autentikasi gagal: {resp.text}")
        return None

    data = resp.json()
    token = data.get("access_token")
    if token:
        print("  [OK] Access token berhasil didapat")
    return token


# ── 2. CARI VIDEO ─────────────────────────────────────────────────────────────
def cari_video_tiktok(keyword, token, max_video=100):
    """
    Cari video TikTok berdasarkan keyword menggunakan Research API.
    Research API hanya tersedia untuk peneliti yang sudah approved.
    """
    semua    = []
    cursor   = 0
    has_more = True

    # Hitung tanggal (Research API butuh rentang tanggal)
    sampai    = datetime.now()
    dari      = sampai - timedelta(days=30)   # 30 hari ke belakang

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }

    print(f"\n  Mencari video TikTok: '{keyword}'")

    while has_more and len(semua) < max_video:
        payload = {
            "query": {
                "and": [
                    {
                        "operation": "IN",
                        "field_name": "keyword",
                        "field_values": [keyword],
                    }
                ]
            },
            "start_date":  dari.strftime("%Y%m%d"),
            "end_date":    sampai.strftime("%Y%m%d"),
            "max_count":   min(100, max_video - len(semua)),
            "cursor":      cursor,
            "search_id":   "",
            "fields":      "id,video_description,create_time,region_code,"
                           "share_count,view_count,like_count,comment_count,"
                           "music_id,hashtag_names,username,effect_ids,duet_from",
        }

        try:
            resp = requests.post(
                "https://open.tiktokapis.com/v2/research/video/query/",
                headers=headers,
                json=payload,
                timeout=20,
            )
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] {e}")
            break

        if resp.status_code == 401:
            print("  [ERROR] Token kedaluwarsa. Coba jalankan ulang.")
            break
        if resp.status_code == 429:
            print("  [WAIT] Rate limit! Tunggu 60 detik...")
            time.sleep(60)
            continue

        try:
            resp.raise_for_status()
            data = resp.json().get("data", {})
        except Exception as e:
            print(f"  [ERROR] Parsing response: {e}")
            break

        videos   = data.get("videos", [])
        has_more = data.get("has_more", False)
        cursor   = data.get("cursor", cursor + len(videos))

        for v in videos:
            hashtags = v.get("hashtag_names", [])
            semua.append({
                "video_id":    v.get("id"),
                "deskripsi":   v.get("video_description", "")[:300],
                "tanggal":     datetime.fromtimestamp(
                                   v.get("create_time", 0)
                               ).strftime("%Y-%m-%d %H:%M:%S"),
                "username":    v.get("username", ""),
                "views":       v.get("view_count",    0),
                "likes":       v.get("like_count",    0),
                "komentar":    v.get("comment_count", 0),
                "share":       v.get("share_count",   0),
                "region":      v.get("region_code",   ""),
                "hashtag":     ", ".join(hashtags) if hashtags else "",
                "jumlah_tag":  len(hashtags),
                "url":         f"https://www.tiktok.com/@{v.get('username')}/video/{v.get('id')}",
                "keyword":     keyword,
            })

        print(f"  +{len(videos)} video | Total: {len(semua)}")

        if not has_more:
            break
        time.sleep(0.5)

    return semua


# ── 3. SIMPAN DATA ─────────────────────────────────────────────────────────────
def simpan_data(data_list, prefix="tiktok"):
    if not data_list:
        print("  [WARN] Tidak ada data.")
        return

    df = pd.DataFrame(data_list)
    df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")
    df = df.drop_duplicates(subset="video_id")
    df = df.sort_values("views", ascending=False).reset_index(drop=True)

    os.makedirs("data", exist_ok=True)

    path_csv = os.path.join("data", f"{prefix}.csv")
    df.to_csv(path_csv, index=False, encoding="utf-8-sig")
    print(f"  [OK] CSV: {path_csv} ({len(df)} video)")

    path_xlsx = os.path.join("data", f"{prefix}.xlsx")
    with pd.ExcelWriter(path_xlsx, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="TikTok", index=False)
        ws = writer.sheets["TikTok"]
        for col in ws.columns:
            max_len = max(
                (len(str(c.value)) for c in col if c.value), default=10
            )
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 80)
    print(f"  [OK] Excel: {path_xlsx}")


# ── 4. MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  TIKTOK RESEARCH API SCRAPER")
    print(f"  Waktu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    KEYWORD   = "kecerdasan buatan"
    MAX_VIDEO = 100

    token = get_access_token()
    if not token:
        sys.exit(1)

    videos = cari_video_tiktok(KEYWORD, token, max_video=MAX_VIDEO)
    print(f"\n  Total: {len(videos)} video")
    simpan_data(videos)

    print(f"\n  Selesai: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    input("\n  Tekan ENTER untuk keluar...")

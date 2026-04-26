"""
================================================================================
  TWITTER / X SCRAPER - Ambil tweet ke CSV / Excel
  Platform : Windows 10/11
  Syarat   : Twitter Developer Account + Bearer Token
  Harga    : Free tier = 500 tweet/bulan  |  Basic = $100/bulan (10.000 tweet)
================================================================================
  Cara daftar:
    1. Buka https://developer.twitter.com/en/portal/dashboard
    2. Buat project + app baru
    3. Salin "Bearer Token" ke file .env (TWITTER_BEARER_TOKEN=...)
    4. Ketik: python 03_twitter_scraper.py
================================================================================
"""

import requests
import pandas as pd
import os
import time
import sys
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

BEARER = os.getenv("TWITTER_BEARER_TOKEN")

if not BEARER:
    print("=" * 60)
    print("  ERROR: TWITTER_BEARER_TOKEN tidak ditemukan di .env!")
    print("  Daftar di: https://developer.twitter.com")
    print("=" * 60)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {BEARER}",
    "User-Agent":    "v2RecentSearchPython",
}
BASE_URL = "https://api.twitter.com/2"


# ── 1. CARI TWEET ─────────────────────────────────────────────────────────────
def cari_tweet(keyword, max_tweet=100, exclude_retweet=True, bahasa="id"):
    """
    Cari tweet dari 7 hari terakhir (batas free tier).
    max_tweet: Free tier = 500/bulan, Basic = 10.000/bulan.
    """
    semua    = []
    next_tok = None

    # Bangun query — Twitter punya sintaks khusus
    query = keyword
    if exclude_retweet:
        query += " -is:retweet"
    if bahasa:
        query += f" lang:{bahasa}"

    print(f"\n  Query: '{query}'")

    while len(semua) < max_tweet:
        sisa = max_tweet - len(semua)

        params = {
            "query":       query,
            "max_results": min(100, max(10, sisa)),  # API minta min 10, maks 100
            "tweet.fields": "created_at,public_metrics,author_id,conversation_id,lang",
            "expansions":   "author_id",
            "user.fields":  "name,username,public_metrics,verified",
        }
        if next_tok:
            params["next_token"] = next_tok

        try:
            resp = requests.get(
                f"{BASE_URL}/tweets/search/recent",
                headers=HEADERS,
                params=params,
                timeout=15,
            )
        except requests.exceptions.ConnectionError:
            print("  [ERROR] Tidak ada koneksi internet.")
            break
        except requests.exceptions.Timeout:
            print("  [WARN] Timeout. Coba lagi...")
            time.sleep(5)
            continue

        # Handle rate limit (15 menit window untuk Twitter)
        if resp.status_code == 429:
            reset_ts = int(resp.headers.get("x-rate-limit-reset", time.time() + 900))
            tunggu   = max(reset_ts - int(time.time()), 5)
            print(f"  [WAIT] Rate limit! Tunggu {tunggu} detik (~{tunggu//60} menit)...")
            time.sleep(tunggu + 2)
            continue

        if resp.status_code == 401:
            print("  [ERROR] Bearer Token tidak valid atau kedaluwarsa!")
            break

        if resp.status_code == 403:
            print("  [ERROR] Akses ditolak. Mungkin quota sudah habis bulan ini.")
            print(f"          {resp.json().get('detail', '')}")
            break

        try:
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  [ERROR] {e}")
            break

        tweets = data.get("data", [])
        if not tweets:
            print("  Tidak ada tweet lagi.")
            break

        # Buat map user (dari expansions)
        users_map = {}
        for u in data.get("includes", {}).get("users", []):
            users_map[u["id"]] = u

        # Gabungkan data tweet + user
        for t in tweets:
            met   = t.get("public_metrics", {})
            uid   = t.get("author_id", "")
            user  = users_map.get(uid, {})
            u_met = user.get("public_metrics", {})

            semua.append({
                "tweet_id":       t.get("id"),
                "teks":           t.get("text", "").replace("\n", " "),
                "tanggal":        t.get("created_at", ""),
                "bahasa":         t.get("lang", ""),
                "likes":          met.get("like_count",    0),
                "retweet":        met.get("retweet_count", 0),
                "reply":          met.get("reply_count",   0),
                "quote":          met.get("quote_count",   0),
                "username":       user.get("username", ""),
                "nama_akun":      user.get("name", ""),
                "verified":       user.get("verified", False),
                "followers":      u_met.get("followers_count", 0),
                "following":      u_met.get("following_count", 0),
                "total_tweet_akun": u_met.get("tweet_count",  0),
                "url":            f"https://twitter.com/i/web/status/{t.get('id')}",
                "keyword":        keyword,
            })

        print(f"  +{len(tweets)} tweet | Total: {len(semua)}")

        meta = data.get("meta", {})
        next_tok = meta.get("next_token")
        if not next_tok:
            break

        time.sleep(1)   # Jangan spam

    return semua


# ── 2. SIMPAN DATA ─────────────────────────────────────────────────────────────
def simpan_data(data_list, prefix="twitter"):
    if not data_list:
        print("  [WARN] Tidak ada data untuk disimpan.")
        return

    df = pd.DataFrame(data_list)
    df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce", utc=True)
    df["tanggal"] = df["tanggal"].dt.tz_localize(None)
    df = df.drop_duplicates(subset="tweet_id")
    df = df.sort_values("likes", ascending=False).reset_index(drop=True)

    os.makedirs("data", exist_ok=True)

    path_csv = os.path.join("data", f"{prefix}.csv")
    df.to_csv(path_csv, index=False, encoding="utf-8-sig")
    print(f"  [OK] CSV: {path_csv} ({len(df)} tweet)")

    path_xlsx = os.path.join("data", f"{prefix}.xlsx")
    with pd.ExcelWriter(path_xlsx, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Twitter", index=False)
        ws = writer.sheets["Twitter"]
        for col in ws.columns:
            max_len = max(
                (len(str(c.value)) for c in col if c.value), default=10
            )
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 80)

    print(f"  [OK] Excel: {path_xlsx}")


# ── 3. MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  TWITTER / X SCRAPER")
    print(f"  Waktu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    # ─── KONFIGURASI ───
    KEYWORD   = "AI Indonesia"
    MAX_TWEET = 100      # Free tier: hemat (maks 500/bulan total!)
    # ───────────────────

    print(f"  Mencari tweet: '{KEYWORD}'")
    print(f"  PERHATIAN: Free tier hanya 500 tweet/bulan!")

    tweets = cari_tweet(KEYWORD, max_tweet=MAX_TWEET)
    print(f"\n  Total terkumpul: {len(tweets)} tweet")
    simpan_data(tweets, prefix="twitter")

    print(f"\n  Selesai: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    input("\n  Tekan ENTER untuk keluar...")

"""
Menu utama - pilih platform scraper yang ingin dijalankan.
"""
import os
import sys
import subprocess

def main():
    print("=" * 80)
    print("  SCRAPPING DATA KASUS KEKERASAN SEKSUAL PADA PERGURUAN TINGGI DI INDONESIA")
    print("=" * 80)
    print()
    print("  Pilih platform yang ingin di-scrape:")
    print()
    print("  [1] YouTube")
    print("  [2] Berita / Artikel")
    print("  [3] Twitter / X")
    print("  [4] TikTok")
    print("  [5] Ekstrak Universitas v2  (olah CSV -> Excel riset. Intinya olah data mentah)")
    print("  [0] Keluar")
    print()

    pilihan = input("  Masukkan nomor pilihan: ").strip()

    scripts = {
        "1": "01_youtube_scraper.py",
        "2": "02_news_scraper.py",
        "3": "03_twitter_scraper.py",
        "4": "04_tiktok_scraper.py",
        "5": "05_ekstrak_universitas_v2.py",
    }

    if pilihan == "0":
        print("\n  Keluar. Sampai jumpa!")
        sys.exit(0)
    elif pilihan in scripts:
        script = scripts[pilihan]
        if not os.path.exists(script):
            print(f"\n  [ERROR] File {script} tidak ditemukan!")
            sys.exit(1)
        print(f"\n  Menjalankan {script}...\n")
        subprocess.run([sys.executable, script])
    else:
        print("\n  Pilihan tidak valid. Jalankan ulang dan pilih 1-5.")

if __name__ == "__main__":
    main()

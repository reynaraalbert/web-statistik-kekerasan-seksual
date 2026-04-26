"""
scripts/process_data.py
Converts Excel data to JSON for Next.js website
"""
import pandas as pd
import json
import os
from datetime import datetime
import re

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE, "data")
OUT_DIR = os.path.join(BASE, "sigap_web", "public", "data")
os.makedirs(OUT_DIR, exist_ok=True)

def clean_html(text):
    if not isinstance(text, str): return ""
    return re.sub(r'<[^>]+>', '', text).strip()

def safe_int(v, default=0):
    try: return int(v) if pd.notna(v) else default
    except: return default

def safe_str(v, default=""):
    if pd.isna(v) if not isinstance(v, str) else False: return default
    return str(v).strip() if v else default

# ---- Load Data ----
riset_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("RISET_") and f.endswith(".xlsx")], reverse=True)
berita_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("berita_") and f.endswith(".xlsx")], reverse=True)
yt_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("youtube_video_") and f.endswith(".xlsx")], reverse=True)

print("Loading RISET data...")
df = pd.read_excel(os.path.join(DATA_DIR, riset_files[0]))
df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")

print("Loading Berita data...")
df_b = pd.read_excel(os.path.join(DATA_DIR, berita_files[0]))

print("Loading YouTube data...")
df_yt = pd.read_excel(os.path.join(DATA_DIR, yt_files[0]))

# ====================================================
# 1. MAIN STATS
# ====================================================
total = len(df)
identifikasi = df[df["universitas"] != "Tidak Teridentifikasi"]
n_kampus = df["universitas"].nunique() - 1
n_provinsi = df[df["provinsi"] != "Tidak Diketahui"]["provinsi"].nunique()
tahun_min = int(df["tahun"].dropna().min())
tahun_max = int(df["tahun"].dropna().max())

# ====================================================
# 2. TREND TAHUNAN
# ====================================================
trend = df.groupby("tahun").size().reset_index(name="jumlah")
trend = trend[trend["tahun"].notna()].sort_values("tahun")
trend_data = [{"tahun": int(r["tahun"]), "jumlah": int(r["jumlah"])} for _, r in trend.iterrows()]

# ====================================================
# 3. JENIS KEKERASAN
# ====================================================
jenis_data_raw = df["jenis_kekerasan"].dropna()
jenis_data_raw = jenis_data_raw[jenis_data_raw != "Tidak Teridentifikasi"].value_counts()
jenis_data = [{"label": k, "value": int(v)} for k, v in jenis_data_raw.items()]

# ====================================================
# 4. PELAKU
# ====================================================
pelaku_raw = df["pelaku"].dropna()
pelaku_raw = pelaku_raw[pelaku_raw != "Tidak Diketahui"].value_counts()
pelaku_data = [{"label": k, "value": int(v)} for k, v in pelaku_raw.items()]

# ====================================================
# 5. TOP UNIVERSITAS
# ====================================================
univ_raw = identifikasi["universitas"].value_counts().head(20)
univ_data = [{"label": k, "value": int(v)} for k, v in univ_raw.items()]

# ====================================================
# 6. PROVINSI
# ====================================================
prov_raw = df[df["provinsi"] != "Tidak Diketahui"]["provinsi"].value_counts()
prov_data = [{"label": k, "value": int(v)} for k, v in prov_raw.items()]

# Provinsi with coordinates
PROV_COORDS = {
    "Aceh": [-4.695, 96.749],
    "Sumatera Utara": [2.115, 99.030],
    "Sumatera Barat": [-0.740, 100.800],
    "Riau": [0.293, 101.707],
    "Kepulauan Riau": [3.943, 108.143],
    "Jambi": [-1.610, 103.615],
    "Sumatera Selatan": [-3.320, 103.914],
    "Bangka Belitung": [-2.741, 106.441],
    "Bengkulu": [-3.793, 102.265],
    "Lampung": [-4.558, 105.405],
    "DKI Jakarta": [-6.200, 106.817],
    "Jawa Barat": [-6.889, 107.640],
    "Banten": [-6.406, 106.064],
    "Jawa Tengah": [-7.151, 110.140],
    "DI Yogyakarta": [-7.797, 110.371],
    "Jawa Timur": [-7.536, 112.239],
    "Bali": [-8.410, 115.189],
    "Nusa Tenggara Barat": [-8.652, 117.362],
    "Nusa Tenggara Timur": [-8.657, 121.079],
    "Kalimantan Barat": [-0.026, 109.343],
    "Kalimantan Tengah": [-1.681, 113.383],
    "Kalimantan Selatan": [-3.093, 115.284],
    "Kalimantan Timur": [1.638, 116.419],
    "Kalimantan Utara": [3.074, 116.042],
    "Sulawesi Utara": [0.628, 123.975],
    "Gorontalo": [0.531, 123.057],
    "Sulawesi Tengah": [-1.430, 121.446],
    "Sulawesi Barat": [-2.841, 119.232],
    "Sulawesi Selatan": [-3.668, 119.974],
    "Sulawesi Tenggara": [-4.145, 122.175],
    "Maluku": [-3.238, 130.145],
    "Maluku Utara": [1.571, 127.809],
    "Papua Barat": [-1.336, 133.175],
    "Papua": [-4.270, 138.080],
}

prov_geo = []
for item in prov_data:
    coords = PROV_COORDS.get(item["label"])
    if coords:
        # Count universities in this province
        univ_list = identifikasi[identifikasi["provinsi"] == item["label"]]["universitas"].value_counts()
        top_univ = [{"name": k, "count": int(v)} for k, v in univ_list.items()]
        
        jenis_prov = df[df["provinsi"] == item["label"]]["jenis_kekerasan"].dropna()
        jenis_prov = jenis_prov[jenis_prov != "Tidak Teridentifikasi"].value_counts()
        
        jenis_prov_items = list(jenis_prov.items())[:5]
        prov_geo.append({
            "name": item["label"],
            "count": item["value"],
            "lat": coords[0],
            "lng": coords[1],
            "kampus_count": int(univ_list.shape[0]),
            "top_universitas": top_univ[:5],
            "jenis_kekerasan": [{"label": k, "value": int(v)} for k, v in jenis_prov_items],
        })

# ====================================================
# 7. UNIVERSITAS GEO
# ====================================================
UNIV_COORDS = {
    "Universitas Indonesia": [-6.3605, 106.8270],
    "Universitas Brawijaya": [-7.9521, 112.6122],
    "Universitas Negeri Yogyakarta": [-7.7778, 110.3928],
    "Universitas Gadjah Mada": [-7.7714, 110.3775],
    "Universitas Sumatera Utara": [3.5669, 98.6482],
    "Universitas Padjadjaran": [-6.9218, 107.7693],
    "Universitas Airlangga": [-7.2687, 112.7582],
    "Universitas Negeri Jakarta": [-6.2000, 106.8700],
    "Universitas Pelita Harapan": [-6.2240, 106.6398],
    "Universitas Sebelas Maret": [-7.5567, 110.8586],
    "Universitas Diponegoro": [-7.0500, 110.4381],
    "Institut Teknologi Bandung": [-6.8913, 107.6102],
    "Universitas Hasanuddin": [-5.1354, 119.4887],
    "Universitas Udayana": [-8.7979, 115.1664],
    "Universitas Lampung": [-5.3667, 105.2417],
    "Universitas Riau": [0.4694, 101.3731],
    "Universitas Andalas": [-0.9003, 100.4569],
    "Universitas Sam Ratulangi": [1.4707, 124.8454],
}

univ_geo = []
for _, grp in identifikasi.groupby("universitas"):
    name = grp["universitas"].iloc[0]
    coords = UNIV_COORDS.get(name)
    if not coords:
        continue
    count = len(grp)
    prov = grp["provinsi"].mode()[0] if len(grp) > 0 else "-"
    status = grp["status_pt"].mode()[0] if len(grp) > 0 else "-"
    jenis = grp["jenis_kekerasan"].dropna()
    jenis = jenis[jenis != "Tidak Teridentifikasi"].value_counts()
    pelaku_g = grp["pelaku"].dropna()
    pelaku_g = pelaku_g[pelaku_g != "Tidak Diketahui"].value_counts()
    trend_u = grp.groupby("tahun").size().reset_index(name="n")
    
    jenis_items = list(jenis.items())[:5]
    pelaku_items = list(pelaku_g.items())[:5]
    univ_geo.append({
        "name": name,
        "count": count,
        "lat": coords[0],
        "lng": coords[1],
        "provinsi": prov,
        "status": status,
        "jenis_kekerasan": [{"label": k, "value": int(v)} for k, v in jenis_items],
        "pelaku": [{"label": k, "value": int(v)} for k, v in pelaku_items],
        "trend": [{"tahun": int(r["tahun"]), "n": int(r["n"])} for _, r in trend_u.iterrows() if pd.notna(r["tahun"])],
    })

# ====================================================
# 8. CROSS-TAB PELAKU VS JENIS
# ====================================================
ct = pd.crosstab(df["pelaku"], df["jenis_kekerasan"])
ct = ct.drop(index="Tidak Diketahui", errors="ignore").drop(columns="Tidak Teridentifikasi", errors="ignore")
# Get top 5 pelaku and top 5 jenis for cleaner chart
top_p = pelaku_raw.head(5).index
top_j = jenis_data_raw.head(5).index
ct_sub = ct.loc[ct.index.isin(top_p), ct.columns.isin(top_j)]

crosstab_data = []
for p in ct_sub.index:
    for j in ct_sub.columns:
        crosstab_data.append({
            "pelaku": p,
            "jenis": j,
            "jumlah": int(ct_sub.loc[p, j])
        })

# ====================================================
# 9. KOTA STATS
# ====================================================
kota_raw = df[df["kota"] != "Tidak Diketahui"]["kota"].value_counts().head(15)
kota_data = [{"label": k, "value": int(v)} for k, v in kota_raw.items()]

# ====================================================
# 10. MONTHLY HEATMAP
# ====================================================
BULAN_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
BULAN_ID = ["Januari","Februari","Maret","April","Mei","Juni",
            "Juli","Agustus","September","Oktober","November","Desember"]

heatmap_data = []
for tahun_val in sorted(df["tahun"].dropna().unique()):
    for i, bulan_val in enumerate(BULAN_ORDER):
        count = len(df[(df["tahun"] == tahun_val) & (df["bulan"] == bulan_val)])
        if count > 0:
            heatmap_data.append({
                "tahun": int(tahun_val),
                "bulan": bulan_val,
                "bulan_id": BULAN_ID[i],
                "bulan_index": i,
                "jumlah": count
            })

# ====================================================
# 11. STATUS PT
# ====================================================
status_raw = df[df["status_pt"] != "Tidak Diketahui"]["status_pt"].value_counts()
status_data = [{"label": k, "value": int(v)} for k, v in status_raw.items()]

# ====================================================
# 10. YOUTUBE
# ====================================================
yt_top = df_yt.dropna(subset=["views"]).nlargest(20, "views")
yt_data = []
for _, r in yt_top.iterrows():
    yt_data.append({
        "video_id": safe_str(r.get("video_id")),
        "judul": safe_str(r.get("judul")),
        "channel": safe_str(r.get("channel")),
        "views": safe_int(r.get("views")),
        "likes": safe_int(r.get("likes")),
        "komentar": safe_int(r.get("komentar")),
        "tanggal": safe_str(r.get("tanggal_tayang"))[:10],
        "url": safe_str(r.get("url")),
        "keyword": safe_str(r.get("keyword")),
    })

# YT trend by year
df_yt["tahun_upload"] = pd.to_datetime(df_yt["tanggal_tayang"], errors="coerce").dt.year
yt_trend = df_yt.dropna(subset=["tahun_upload"]).groupby("tahun_upload").agg(
    video=("tahun_upload","count"), total_views=("views","sum")).reset_index()
yt_trend_data = [{"tahun": int(r["tahun_upload"]), "video": int(r["video"]),
                  "total_views": safe_int(r["total_views"])} for _, r in yt_trend.iterrows()]

# ====================================================
# 11. BERITA TERBARU
# ====================================================
berita_list = []
for _, r in df_b.dropna(subset=["judul"]).head(30).iterrows():
    judul = clean_html(safe_str(r.get("judul")))
    judul = judul.split(" - ")[0][:120]
    if len(judul) < 10: continue
    berita_list.append({
        "judul": judul,
        "sumber": safe_str(r.get("sumber")),
        "tanggal": safe_str(r.get("tanggal"))[:10],
        "url": safe_str(r.get("url")),
        "keyword": safe_str(r.get("keyword")),
    })

# ====================================================
# 12. GROWTH STATS
# ====================================================
trend_clean = trend[trend["tahun"] >= 2019].set_index("tahun")["jumlah"]
years_list = sorted(trend_clean.index.tolist())
growth_2021 = int(trend_clean.get(2021, 0))
growth_latest = int(trend_clean.iloc[-1]) if len(trend_clean) > 0 else 0
growth_prev = int(trend_clean.iloc[-2]) if len(trend_clean) > 1 else 0
growth_pct = round((growth_latest - growth_prev) / growth_prev * 100, 1) if growth_prev > 0 else 0

# ====================================================
# ASSEMBLE OUTPUT
# ====================================================
output = {
    "meta": {
        "generated_at": datetime.now().isoformat(),
        "source_file": riset_files[0],
    },
    "overview": {
        "total_laporan": total,
        "total_teridentifikasi": len(identifikasi),
        "total_kampus": n_kampus,
        "total_provinsi": n_provinsi,
        "tahun_min": tahun_min,
        "tahun_max": tahun_max,
        "total_berita": len(df_b),
        "total_youtube": len(df_yt),
        "total_views_yt": safe_int(df_yt["views"].sum()),
    },
    "growth": {
        "latest_year": tahun_max,
        "latest_count": growth_latest,
        "prev_count": growth_prev,
        "growth_pct": growth_pct,
        "peak_2021": growth_2021,
    },
    "trend_tahunan": trend_data,
    "jenis_kekerasan": jenis_data,
    "pelaku": pelaku_data,
    "status_pt": status_data,
    "top_universitas": univ_data,
    "provinsi": prov_data,
    "provinsi_geo": prov_geo,
    "universitas_geo": univ_geo,
    "heatmap_bulanan": heatmap_data,
    "youtube_top": yt_data,
    "youtube_trend": yt_trend_data,
    "berita_terbaru": berita_list,
    "crosstab": crosstab_data,
    "kota_stats": kota_data,
}

OUT_FILE = os.path.join(OUT_DIR, "sigap.json")
with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n[OK] Data berhasil diproses!")
print(f"   Output: {OUT_FILE}")
print(f"   Total laporan: {total:,}")
print(f"   Provinsi geo: {len(prov_geo)}")
print(f"   Universitas geo: {len(univ_geo)}")
print(f"   Berita: {len(berita_list)}")
print(f"   YouTube: {len(yt_data)}")

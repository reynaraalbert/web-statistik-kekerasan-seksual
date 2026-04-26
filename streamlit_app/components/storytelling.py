"""
components/storytelling.py
Auto-generates narrative storytelling from data
"""
import pandas as pd


def format_num(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f} juta"
    if n >= 1_000:
        return f"{n:,.0f}"
    return str(int(n))


def story_overview(df: pd.DataFrame) -> str:
    """Main overview narrative"""
    total = len(df)
    identifikasi = df[df["universitas"] != "Tidak Teridentifikasi"] if "universitas" in df.columns else df
    n_id = len(identifikasi)
    kampus = df["universitas"].nunique() - (1 if "Tidak Teridentifikasi" in df["universitas"].values else 0) if "universitas" in df.columns else 0
    provinsi = df["provinsi"].nunique() - (1 if "Tidak Diketahui" in df["provinsi"].values else 0) if "provinsi" in df.columns else 0
    tahun_min = int(df["tahun"].min()) if "tahun" in df.columns else "?"
    tahun_max = int(df["tahun"].max()) if "tahun" in df.columns else "?"

    return (
        f"Dari total <strong>{format_num(total)}</strong> laporan yang berhasil dikumpulkan antara tahun "
        f"<strong>{tahun_min}–{tahun_max}</strong>, sebanyak <strong>{n_id:,}</strong> kasus "
        f"({(n_id/total*100):.0f}%) berhasil diidentifikasi dan dikaitkan dengan institusi pendidikan tinggi tertentu. "
        f"Data ini mencakup <strong>{kampus} perguruan tinggi</strong> yang tersebar di "
        f"<strong>{provinsi} provinsi</strong> di seluruh Indonesia — menjadikannya salah satu "
        f"basis data terlengkap tentang kekerasan seksual di lingkungan kampus yang pernah dikompilasi."
    )


def story_trend(df: pd.DataFrame) -> str:
    """Trend narrative"""
    if "tahun" not in df.columns:
        return "Data tren tahunan tidak tersedia."
    tahunan = df.groupby("tahun").size().sort_index()
    tahunan = tahunan[tahunan.index > 2015]
    if len(tahunan) < 2:
        return "Data tren tidak cukup untuk dianalisis."

    tahun_puncak = int(tahunan.idxmax())
    n_puncak = int(tahunan.max())
    tahun_awal = int(tahunan.index[0])
    n_awal = int(tahunan.iloc[0])
    tahun_akhir = int(tahunan.index[-1])
    n_akhir = int(tahunan.iloc[-1])

    perubahan = ((n_akhir - n_awal) / n_awal * 100) if n_awal > 0 else 0
    arah = "meningkat" if perubahan > 0 else "menurun"
    magnitude = abs(perubahan)

    lonjakan_2021 = tahunan.get(2021, 0)
    konteks_2021 = ""
    if lonjakan_2021 > 0:
        konteks_2021 = (
            f" Lonjakan signifikan terjadi pada 2021, bertepatan dengan maraknya gerakan "
            f"<em>#MeToo</em> Indonesia dan disahkannya Permendikbudristek No. 30/2021 tentang "
            f"PPKS di kampus, yang mendorong lebih banyak korban berani melapor."
        )

    return (
        f"Tren pemberitaan menunjukkan kasus kekerasan seksual di kampus "
        f"<strong>{arah} sebesar {magnitude:.0f}%</strong> dari {tahun_awal} ke {tahun_akhir}. "
        f"Puncak pemberitaan tertinggi terjadi pada <strong>tahun {tahun_puncak}</strong> dengan "
        f"<strong>{n_puncak:,} laporan</strong>.{konteks_2021} "
        f"Peningkatan liputan media ini tidak selalu berarti peningkatan kejadian, melainkan juga "
        f"mencerminkan meningkatnya kesadaran publik dan keberanian korban untuk melapor."
    )


def story_jenis_kekerasan(df: pd.DataFrame) -> str:
    """Narrative for violence types"""
    if "jenis_kekerasan" not in df.columns:
        return "Data jenis kekerasan tidak tersedia."
    data = df["jenis_kekerasan"].dropna()
    data = data[data != "Tidak Teridentifikasi"]
    if len(data) == 0:
        return "Data jenis kekerasan tidak cukup."
    vc = data.value_counts()
    top = vc.index[0]
    top_n = int(vc.iloc[0])
    top_pct = top_n / len(data) * 100
    total_id = len(data)

    kbgo_n = int(vc.get("KBGO", 0))
    kbgo_txt = ""
    if kbgo_n > 0:
        kbgo_txt = (
            f" Yang perlu dicatat adalah munculnya kategori <strong>KBGO (Kekerasan Berbasis Gender Online)</strong> "
            f"dengan <strong>{kbgo_n} laporan</strong>, mencerminkan pergeseran modus kekerasan ke ranah digital "
            f"seiring meningkatnya penggunaan media sosial di lingkungan kampus."
        )

    return (
        f"Dari <strong>{total_id:,} kasus</strong> yang berhasil dikategorikan, jenis kekerasan paling dominan "
        f"adalah <strong>{top}</strong> yang menyumbang <strong>{top_pct:.0f}%</strong> ({top_n:,} kasus) dari total "
        f"laporan. Dominasi kategori ini mencerminkan tantangan dalam pendefinisian dan pelaporan "
        f"kekerasan seksual di kampus, di mana banyak korban kesulitan mengidentifikasi pengalaman "
        f"mereka ke dalam kategori yang lebih spesifik.{kbgo_txt}"
    )


def story_pelaku(df: pd.DataFrame) -> str:
    """Narrative for perpetrators"""
    if "pelaku" not in df.columns:
        return "Data pelaku tidak tersedia."
    data = df["pelaku"].dropna()
    data = data[data != "Tidak Diketahui"]
    if len(data) == 0:
        return "Data pelaku tidak cukup."
    vc = data.value_counts()
    top = vc.index[0]
    top_n = int(vc.iloc[0])
    top_pct = top_n / len(data) * 100

    dosen_n = int(vc.get("Dosen", 0)) + int(vc.get("Dosen Pembimbing", 0))
    dosen_txt = ""
    if dosen_n > 0:
        dosen_pct = dosen_n / len(data) * 100
        dosen_txt = (
            f" Gabungan pelaku dari kalangan <strong>dosen</strong> (termasuk dosen pembimbing) "
            f"mencapai <strong>{dosen_n} kasus ({dosen_pct:.0f}%)</strong>, menunjukkan betapa "
            f"relasi kuasa yang tidak setara antara dosen dan mahasiswa masih menjadi faktor risiko utama."
        )

    return (
        f"Berdasarkan identifikasi pelaku, <strong>{top}</strong> merupakan kelompok pelaku terbanyak "
        f"dengan <strong>{top_n} kasus ({top_pct:.0f}%)</strong> dari total kasus teridentifikasi.{dosen_txt} "
        f"Temuan ini menegaskan perlunya kebijakan yang tidak hanya menyasar mahasiswa, tetapi juga "
        f"membangun sistem pelaporan yang aman bagi korban yang berhadapan dengan pelaku "
        f"yang memiliki otoritas lebih tinggi."
    )


def story_universitas(df: pd.DataFrame) -> str:
    """Narrative for universities"""
    if "universitas" not in df.columns:
        return "Data universitas tidak tersedia."
    data = df["universitas"].dropna()
    data = data[data != "Tidak Teridentifikasi"]
    if len(data) == 0:
        return "Data tidak cukup."
    vc = data.value_counts()
    top1 = vc.index[0]
    top1_n = int(vc.iloc[0])
    top3 = ", ".join(vc.index[:3].tolist())

    status_data = df["status_pt"].dropna() if "status_pt" in df.columns else pd.Series()
    negeri_n = int((status_data == "Negeri").sum())
    swasta_n = int((status_data == "Swasta").sum())
    status_txt = ""
    if negeri_n > 0 and swasta_n > 0:
        ratio = negeri_n / (negeri_n + swasta_n) * 100
        status_txt = (
            f" Menariknya, <strong>{ratio:.0f}%</strong> kasus yang teridentifikasi terjadi di "
            f"perguruan tinggi negeri, yang mungkin mencerminkan tingginya liputan media terhadap "
            f"kampus-kampus besar daripada rendahnya insiden di kampus swasta."
        )

    return (
        f"<strong>{top1}</strong> menjadi perguruan tinggi dengan jumlah laporan tertinggi, "
        f"yakni <strong>{top1_n} laporan</strong>. Tiga besar universitas dengan kasus terbanyak "
        f"adalah <strong>{top3}</strong>.{status_txt} "
        f"Tingginya angka pada kampus-kampus besar kemungkinan juga dipengaruhi oleh "
        f"visibilitas media yang lebih besar dan adanya saluran pelaporan yang lebih terstruktur."
    )


def story_provinsi(df: pd.DataFrame) -> str:
    """Narrative for provinces"""
    if "provinsi" not in df.columns:
        return "Data provinsi tidak tersedia."
    data = df["provinsi"].dropna()
    data = data[data != "Tidak Diketahui"]
    if len(data) == 0:
        return "Data tidak cukup."
    vc = data.value_counts()
    top1 = vc.index[0]
    top1_n = int(vc.iloc[0])
    n_provinsi = len(vc)

    jabar = int(vc.get("Jawa Barat", 0))
    jatim = int(vc.get("Jawa Timur", 0))
    yogya = int(vc.get("DI Yogyakarta", 0))
    jawa_total = jabar + jatim + yogya + int(vc.get("Jawa Tengah", 0)) + int(vc.get("DKI Jakarta", 0))
    jawa_pct = jawa_total / len(data) * 100

    return (
        f"Sebaran kasus mencakup <strong>{n_provinsi} provinsi</strong> di seluruh Indonesia. "
        f"<strong>{top1}</strong> menjadi provinsi dengan laporan terbanyak (<strong>{top1_n} kasus</strong>), "
        f"yang sejalan dengan konsentrasi perguruan tinggi di wilayah tersebut. "
        f"Pulau Jawa secara keseluruhan mendominasi dengan lebih dari <strong>{jawa_pct:.0f}%</strong> "
        f"dari total laporan yang teridentifikasi — mencerminkan baik konsentrasi kampus maupun "
        f"kekuatan jaringan media di wilayah ini. Diperlukan perhatian khusus untuk "
        f"meningkatkan visibilitas kasus di luar Jawa."
    )


def generate_auto_story(df: pd.DataFrame, kolom_map: dict) -> dict:
    """
    Generate full storytelling for user-uploaded data.
    kolom_map: mapping from user column names to standard names
    Returns dict of section -> narrative text
    """
    # Rename columns to standard
    df_std = df.rename(columns={v: k for k, v in kolom_map.items() if v in df.columns})

    stories = {}
    total = len(df_std)

    # Overview
    stories["ringkasan"] = (
        f"Data yang Anda upload berisi <strong>{total:,} baris</strong> dengan "
        f"<strong>{len(df_std.columns)} kolom</strong>. "
        f"Berikut adalah analisis otomatis berdasarkan kolom-kolom yang terdeteksi."
    )

    if "tahun" in df_std.columns:
        stories["tren"] = story_trend(df_std)
    if "jenis_kekerasan" in df_std.columns:
        stories["jenis"] = story_jenis_kekerasan(df_std)
    if "pelaku" in df_std.columns:
        stories["pelaku"] = story_pelaku(df_std)
    if "universitas" in df_std.columns:
        stories["universitas"] = story_universitas(df_std)
    if "provinsi" in df_std.columns:
        stories["provinsi"] = story_provinsi(df_std)

    return stories, df_std

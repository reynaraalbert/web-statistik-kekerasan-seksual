"""
pages/beranda.py
Halaman Beranda — Portal Berita Style
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.navbar import (render_navbar, render_hero, render_footer,
                                render_ticker, render_section_header, render_story_box, render_stat_card)
from components.charts import chart_trend_tahunan
from components.storytelling import story_overview, story_trend


def render_beranda(df: pd.DataFrame, df_berita: pd.DataFrame, df_yt: pd.DataFrame):
    render_navbar("Beranda")

    # ---- Stats ----
    total = len(df)
    identifikasi = df[df["universitas"] != "Tidak Teridentifikasi"] if "universitas" in df.columns else df
    n_kampus = df["universitas"].nunique() - 1 if "universitas" in df.columns else 0
    n_provinsi = df[df["provinsi"] != "Tidak Diketahui"]["provinsi"].nunique() if "provinsi" in df.columns else 0
    tahun_min = int(df["tahun"].min()) if "tahun" in df.columns else "?"
    tahun_max = int(df["tahun"].max()) if "tahun" in df.columns else "?"

    # ---- Hero ----
    render_hero(total, n_kampus, n_provinsi, f"{tahun_min}–{tahun_max}")

    # ---- Ticker ----
    if not df_berita.empty and "judul" in df_berita.columns:
        headlines = df_berita["judul"].dropna().head(10).tolist()
        # Clean HTML from headlines
        import re
        headlines = [re.sub(r'<[^>]+>', '', h).split(" - ")[0] for h in headlines]
        render_ticker(headlines)

    # ---- 4 Metric Cards ----
    render_section_header("Ringkasan Data", f"Diperbarui per {pd.Timestamp.now().strftime('%d %b %Y')}")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_stat_card(f"{total:,}", "Total Laporan", f"Dari semua sumber 2012–{tahun_max}")
    with c2:
        render_stat_card(f"{len(identifikasi):,}", "Kasus Teridentifikasi",
                         f"{len(identifikasi)/total*100:.0f}% dari total laporan")
    with c3:
        render_stat_card(str(n_kampus), "Perguruan Tinggi",
                         "Yang disebut dalam pemberitaan")
    with c4:
        render_stat_card(str(n_provinsi), "Provinsi",
                         "Tersebar di seluruh Indonesia")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Main Content: Chart + Story ----
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        render_section_header("Tren Kasus per Tahun", "Jumlah laporan yang berhasil dikumpulkan")
        fig_trend = chart_trend_tahunan(df)
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        render_story_box("Analisis Tren", story_trend(df))

    with col_right:
        render_section_header("Berita Terbaru")
        if not df_berita.empty:
            import re
            recent = df_berita.dropna(subset=["judul"]).head(8)
            for _, row in recent.iterrows():
                judul_raw = str(row.get("judul", ""))
                judul = re.sub(r'<[^>]+>', '', judul_raw).split(" - ")[0][:90]
                tanggal = str(row.get("tanggal", ""))[:10]
                sumber = str(row.get("sumber", ""))
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-card-title">{judul}</div>
                    <div class="news-card-meta">
                        <span>📰 {sumber}</span>
                        <span>🗓️ {tanggal}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Data berita tidak tersedia.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Secondary Stats Row ----
    render_section_header("Snapshot Cepat", "Distribusi utama dari data")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if "jenis_kekerasan" in df.columns:
            data = df["jenis_kekerasan"].dropna()
            data = data[data != "Tidak Teridentifikasi"]
            top_jenis = data.value_counts().index[0] if len(data) > 0 else "-"
            top_jenis_n = int(data.value_counts().iloc[0]) if len(data) > 0 else 0
            render_stat_card(top_jenis, "Jenis Terbanyak",
                             f"{top_jenis_n:,} laporan", "#C0392B")

    with col_b:
        if "pelaku" in df.columns:
            data = df["pelaku"].dropna()
            data = data[data != "Tidak Diketahui"]
            top_p = data.value_counts().index[0] if len(data) > 0 else "-"
            top_p_n = int(data.value_counts().iloc[0]) if len(data) > 0 else 0
            render_stat_card(top_p, "Pelaku Terbanyak",
                             f"{top_p_n:,} kasus", "#1A1A2E")

    with col_c:
        if "universitas" in df.columns:
            data = df["universitas"].dropna()
            data = data[data != "Tidak Teridentifikasi"]
            top_univ = data.value_counts().index[0] if len(data) > 0 else "-"
            top_univ_n = int(data.value_counts().iloc[0]) if len(data) > 0 else 0
            render_stat_card(top_univ.replace("Universitas ", "Univ. "),
                             "Kampus Terbanyak",
                             f"{top_univ_n:,} laporan", "#D4A017")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Overview Story ----
    render_section_header("Gambaran Umum")
    render_story_box("Ringkasan Riset", story_overview(df))

    # ---- YouTube Highlights ----
    if not df_yt.empty:
        render_section_header("Sorotan YouTube", f"{len(df_yt):,} video terkait ditemukan")
        top_yt = df_yt.dropna(subset=["views"]).nlargest(3, "views")

        yt_cols = st.columns(3)
        for i, (_, row) in enumerate(top_yt.iterrows()):
            judul = str(row.get("judul", ""))[:60] + "..."
            views = int(row.get("views", 0))
            channel = str(row.get("channel", ""))
            url = str(row.get("url", "#"))
            views_fmt = f"{views/1e6:.1f}M" if views >= 1e6 else f"{views/1e3:.0f}K"
            likes = int(row.get("likes", 0)) if pd.notna(row.get("likes")) else 0

            with yt_cols[i]:
                st.markdown(f"""
                <div class="news-card" style="border-left: 4px solid #C0392B; height:100%;">
                    <span class="news-card-tag">▶ YouTube</span>
                    <div class="news-card-title" style="margin-top:0.5rem;">{judul}</div>
                    <div class="news-card-meta" style="margin-top:0.5rem;">
                        <span>📺 {channel}</span>
                        <span>👁️ {views_fmt} views</span>
                        <span>👍 {likes:,}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    render_footer()

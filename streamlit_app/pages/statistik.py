"""
pages/statistik.py
Halaman Statistik Lengkap — Dashboard dengan narasi storytelling
"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.navbar import render_navbar, render_footer, render_section_header, render_story_box
from components.charts import (chart_trend_tahunan, chart_jenis_kekerasan, chart_pelaku,
                                chart_status_pt, chart_top_universitas, chart_bulanan_heatmap, chart_provinsi_bar)
from components.storytelling import story_trend, story_jenis_kekerasan, story_pelaku, story_universitas, story_provinsi


def render_statistik(df: pd.DataFrame):
    render_navbar("Statistik")

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.8rem; font-weight:800;
                   color:#1A1A2E; margin-bottom:0.4rem;">📊 Dashboard Statistik Lengkap</h2>
        <p style="color:#6C757D; font-size:0.92rem; font-family:'Inter',sans-serif;">
            Analisis komprehensif data kekerasan seksual di perguruan tinggi Indonesia,
            disajikan dengan narasi berbasis data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---- FILTER SIDEBAR ----
    with st.sidebar:
        st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown("""<div style="color:#F0C040; font-size:0.8rem; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.5rem;">
                        🎛️ Filter Data</div>""", unsafe_allow_html=True)

        tahun_vals = sorted(df["tahun"].dropna().astype(int).unique().tolist())
        tahun_sel = st.multiselect("Tahun", options=tahun_vals, default=tahun_vals,
                                    help="Pilih satu atau beberapa tahun")

        if "status_pt" in df.columns:
            status_opts = [s for s in df["status_pt"].dropna().unique() if s != "Tidak Diketahui"]
            status_sel = st.multiselect("Status PT", options=status_opts, default=status_opts)
        else:
            status_sel = []

        if "jenis_kekerasan" in df.columns:
            jenis_opts = [j for j in df["jenis_kekerasan"].dropna().unique() if j != "Tidak Teridentifikasi"]
            jenis_sel = st.multiselect("Jenis Kekerasan", options=jenis_opts, default=jenis_opts)
        else:
            jenis_sel = []

    # ---- Apply Filters ----
    df_f = df.copy()
    if tahun_sel:
        df_f = df_f[df_f["tahun"].astype("Int64", errors="ignore").isin(tahun_sel)]
    if status_sel and "status_pt" in df_f.columns:
        df_f = df_f[df_f["status_pt"].isin(status_sel + ["Tidak Diketahui"])]
    if jenis_sel and "jenis_kekerasan" in df_f.columns:
        df_f = df_f[df_f["jenis_kekerasan"].isin(jenis_sel + ["Tidak Teridentifikasi"])]

    total_f = len(df_f)

    # ---- Filter Info Banner ----
    if total_f < len(df):
        st.markdown(f"""
        <div class="alert-box info">
            🎛️ Filter aktif — Menampilkan <strong>{total_f:,}</strong> dari <strong>{len(df):,}</strong> total baris data.
        </div>
        """, unsafe_allow_html=True)

    # ========== TAB NAVIGATION ==========
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Tren Tahunan", "⚡ Jenis & Pelaku", "🏛️ Universitas", "🗾 Provinsi", "📅 Pola Bulanan"
    ])

    # ====== TAB 1: TREN TAHUNAN ======
    with tab1:
        render_section_header("Tren Kasus per Tahun", f"Total {total_f:,} laporan")

        fig = chart_trend_tahunan(df_f)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        render_story_box("Interpretasi Tren Tahunan", story_trend(df_f))

        # Growth analysis
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("Analisis Pertumbuhan", "Perbandingan antar periode")

        tahunan = df_f.groupby("tahun").size().sort_index()
        tahunan_clean = tahunan[tahunan.index > 2018]

        col1, col2, col3 = st.columns(3)
        if len(tahunan_clean) >= 2:
            years = sorted(tahunan_clean.index.tolist())
            with col1:
                n = int(tahunan_clean[years[-1]])
                st.metric("Laporan Tahun Terbaru", f"{n:,}",
                          delta=f"{n - int(tahunan_clean[years[-2]]):+,} vs tahun sebelumnya")
            with col2:
                total_5yr = int(tahunan_clean[tahunan_clean.index >= years[-1]-4].sum())
                st.metric("Total 5 Tahun Terakhir", f"{total_5yr:,}")
            with col3:
                avg = int(tahunan_clean.mean())
                st.metric("Rata-rata per Tahun", f"{avg:,}")

    # ====== TAB 2: JENIS & PELAKU ======
    with tab2:
        col_left, col_right = st.columns(2, gap="medium")

        with col_left:
            render_section_header("Jenis Kekerasan")
            fig_jenis = chart_jenis_kekerasan(df_f)
            st.plotly_chart(fig_jenis, use_container_width=True, config={"displayModeBar": False})
            render_story_box("Analisis Jenis Kekerasan", story_jenis_kekerasan(df_f))

        with col_right:
            render_section_header("Status Perguruan Tinggi")
            fig_status = chart_status_pt(df_f)
            st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})

            # Metrics PT
            if "status_pt" in df_f.columns:
                n_negeri = int((df_f["status_pt"] == "Negeri").sum())
                n_swasta = int((df_f["status_pt"] == "Swasta").sum())
                c1, c2 = st.columns(2)
                c1.metric("PT Negeri", f"{n_negeri:,}")
                c2.metric("PT Swasta", f"{n_swasta:,}")

        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("Distribusi Pelaku")
        fig_pelaku = chart_pelaku(df_f)
        st.plotly_chart(fig_pelaku, use_container_width=True, config={"displayModeBar": False})
        render_story_box("Analisis Pelaku", story_pelaku(df_f))

    # ====== TAB 3: UNIVERSITAS ======
    with tab3:
        render_section_header("Top Perguruan Tinggi", "Berdasarkan jumlah laporan yang teridentifikasi")

        top_n = st.slider("Tampilkan top N universitas", min_value=5, max_value=30, value=15, step=5)

        fig_univ = chart_top_universitas(df_f, top_n=top_n)
        st.plotly_chart(fig_univ, use_container_width=True, config={"displayModeBar": False})

        render_story_box("Analisis Sebaran Kampus", story_universitas(df_f))

        # Table
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("Tabel Lengkap Universitas")

        if "universitas" in df_f.columns:
            tabel_univ = df_f[df_f["universitas"] != "Tidak Teridentifikasi"].groupby("universitas").agg(
                jumlah_laporan=("universitas", "count"),
                provinsi=("provinsi", lambda x: x.mode()[0] if len(x) > 0 else "-"),
                status_pt=("status_pt", lambda x: x.mode()[0] if len(x) > 0 else "-"),
            ).reset_index().sort_values("jumlah_laporan", ascending=False)
            tabel_univ.columns = ["Universitas", "Jumlah Laporan", "Provinsi", "Status"]
            st.dataframe(tabel_univ.reset_index(drop=True), use_container_width=True, height=400)

    # ====== TAB 4: PROVINSI ======
    with tab4:
        render_section_header("Sebaran per Provinsi")
        fig_prov = chart_provinsi_bar(df_f, top_n=20)
        st.plotly_chart(fig_prov, use_container_width=True, config={"displayModeBar": False})
        render_story_box("Analisis Geografis", story_provinsi(df_f))

        # Table
        st.markdown("<br>", unsafe_allow_html=True)
        if "provinsi" in df_f.columns:
            tabel_prov = df_f[df_f["provinsi"] != "Tidak Diketahui"].groupby("provinsi").agg(
                jumlah=("provinsi", "count"),
                kampus=("universitas", lambda x: x[x != "Tidak Teridentifikasi"].nunique())
            ).reset_index().sort_values("jumlah", ascending=False)
            tabel_prov.columns = ["Provinsi", "Jumlah Laporan", "Kampus Terdampak"]
            tabel_prov["Rank"] = range(1, len(tabel_prov) + 1)
            tabel_prov = tabel_prov[["Rank", "Provinsi", "Jumlah Laporan", "Kampus Terdampak"]]
            st.dataframe(tabel_prov.reset_index(drop=True), use_container_width=True, height=400)

    # ====== TAB 5: POLA BULANAN ======
    with tab5:
        render_section_header("Heatmap Distribusi Bulanan", "Pola musiman kasus per bulan dan tahun")
        fig_heat = chart_bulanan_heatmap(df_f)
        st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

        render_story_box("Interpretasi Pola Musiman",
            "Distribusi kasus berdasarkan bulan dan tahun dapat mengungkap pola musiman pemberitaan "
            "kekerasan seksual di kampus. Lonjakan pada bulan-bulan tertentu seringkali berkaitan dengan "
            "momen-momen penting seperti <strong>Peringatan Hari Perempuan (Maret)</strong>, "
            "<strong>Hari Anti Kekerasan Terhadap Perempuan (November)</strong>, atau viralnya "
            "kasus tertentu di media sosial. Memahami pola ini penting untuk merancang kampanye "
            "kesadaran dan kebijakan pencegahan yang lebih tepat waktu."
        )

        if "bulan" in df_f.columns:
            render_section_header("Distribusi per Bulan (Agregat)")
            bulan_count = df_f["bulan"].value_counts().reset_index()
            bulan_count.columns = ["Bulan", "Jumlah"]
            c1, c2 = st.columns([1, 2])
            with c1:
                st.dataframe(bulan_count, use_container_width=True, height=300)
            with c2:
                import plotly.express as px
                urutan = ["January","February","March","April","May","June",
                          "July","August","September","October","November","December"]
                label_map = {"January":"Januari","February":"Februari","March":"Maret",
                             "April":"April","May":"Mei","June":"Juni","July":"Juli",
                             "August":"Agustus","September":"September","October":"Oktober",
                             "November":"November","December":"Desember"}
                bc2 = bulan_count.copy()
                bc2["order"] = bc2["Bulan"].apply(lambda x: urutan.index(x) if x in urutan else 99)
                bc2 = bc2.sort_values("order")
                bc2["Bulan_ID"] = bc2["Bulan"].map(label_map).fillna(bc2["Bulan"])
                fig_bar = px.bar(bc2, x="Bulan_ID", y="Jumlah", color="Jumlah",
                                 color_continuous_scale=["#FADBD8","#C0392B"],
                                 labels={"Bulan_ID":"Bulan","Jumlah":"Jumlah Kasus"})
                fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                      height=280, margin=dict(l=10,r=10,t=10,b=10),
                                      coloraxis_showscale=False,
                                      font=dict(family="Inter,sans-serif"),
                                      xaxis=dict(showgrid=False),
                                      yaxis=dict(showgrid=True, gridcolor="#E9ECEF"))
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    render_footer()

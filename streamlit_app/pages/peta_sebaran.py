"""
pages/peta_sebaran.py
Halaman Peta Sebaran — Interactive map with clickable locations
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.navbar import render_navbar, render_footer, render_section_header, render_story_box
from components.storytelling import story_provinsi

# Koordinat pusat per provinsi
PROVINSI_COORDS = {
    "Aceh": (-4.695135, 96.749397),
    "Sumatera Utara": (2.115202, 99.030418),
    "Sumatera Barat": (-0.739994, 100.800000),
    "Riau": (0.293394, 101.706952),
    "Kepulauan Riau": (3.942820, 108.142860),
    "Jambi": (-1.610070, 103.614929),
    "Sumatera Selatan": (-3.319713, 103.914399),
    "Bangka Belitung": (-2.741051, 106.440826),
    "Bengkulu": (-3.793129, 102.264755),
    "Lampung": (-4.558480, 105.405296),
    "DKI Jakarta": (-6.200000, 106.816666),
    "Jawa Barat": (-6.889465, 107.640179),
    "Banten": (-6.405803, 106.064293),
    "Jawa Tengah": (-7.150975, 110.140259),
    "DI Yogyakarta": (-7.797068, 110.370529),
    "Jawa Timur": (-7.536064, 112.238588),
    "Bali": (-8.409518, 115.188919),
    "Nusa Tenggara Barat": (-8.652406, 117.361762),
    "Nusa Tenggara Timur": (-8.657384, 121.079180),
    "Kalimantan Barat": (-0.026338, 109.342503),
    "Kalimantan Tengah": (-1.681488, 113.382530),
    "Kalimantan Selatan": (-3.093191, 115.283897),
    "Kalimantan Timur": (1.637573, 116.419389),
    "Kalimantan Utara": (3.073750, 116.041581),
    "Sulawesi Utara": (0.627546, 123.975478),
    "Gorontalo": (0.531380, 123.056787),
    "Sulawesi Tengah": (-1.430196, 121.445617),
    "Sulawesi Barat": (-2.840958, 119.232184),
    "Sulawesi Selatan": (-3.668165, 119.974236),
    "Sulawesi Tenggara": (-4.144722, 122.174576),
    "Maluku": (-3.238024, 130.145332),
    "Maluku Utara": (1.570863, 127.808741),
    "Papua Barat": (-1.336286, 133.174698),
    "Papua": (-4.269928, 138.080353),
}

# Koordinat universitas utama
UNIVERSITAS_COORDS = {
    "Universitas Indonesia": (-6.3605, 106.8270),
    "Universitas Brawijaya": (-7.9521, 112.6122),
    "Universitas Negeri Yogyakarta": (-7.7778, 110.3928),
    "Universitas Gadjah Mada": (-7.7714, 110.3775),
    "Universitas Sumatera Utara": (3.5669, 98.6482),
    "Universitas Padjadjaran": (-6.9218, 107.7693),
    "Universitas Airlangga": (-7.2687, 112.7582),
    "Universitas Negeri Jakarta": (-6.2000, 106.8700),
    "Universitas Pelita Harapan": (-6.2240, 106.6398),
    "Universitas Sebelas Maret": (-7.5567, 110.8586),
    "Universitas Diponegoro": (-7.0500, 110.4381),
    "Institut Teknologi Bandung": (-6.8913, 107.6102),
    "Universitas Hasanuddin": (-5.1354, 119.4887),
    "Universitas Udayana": (-8.7979, 115.1664),
    "Universitas Lampung": (-5.3667, 105.2417),
}


def render_peta(df: pd.DataFrame):
    render_navbar("Peta Sebaran")

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.8rem; font-weight:800;
                   color:#1A1A2E; margin-bottom:0.4rem;">🗺️ Peta Sebaran Kasus</h2>
        <p style="color:#6C757D; font-size:0.92rem; font-family:'Inter',sans-serif;">
            Visualisasi geografis sebaran laporan kekerasan seksual di perguruan tinggi Indonesia.
            Klik pada titik lokasi untuk melihat detail kasus.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---- FILTER ----
    with st.sidebar:
        st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown("""<div style="color:#F0C040; font-size:0.8rem; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.5rem;">
                        🎛️ Filter Peta</div>""", unsafe_allow_html=True)

        tampilan = st.radio("Mode Tampilan", ["Peta Provinsi", "Peta Universitas"])

        tahun_vals = sorted(df["tahun"].dropna().astype(int).unique().tolist())
        tahun_sel = st.multiselect("Filter Tahun", options=tahun_vals, default=tahun_vals)

        if "status_pt" in df.columns:
            status_opts = [s for s in df["status_pt"].dropna().unique() if s != "Tidak Diketahui"]
            status_sel = st.multiselect("Status PT", options=status_opts, default=status_opts)
        else:
            status_sel = []

    # ---- Filter Data ----
    df_f = df.copy()
    if tahun_sel:
        df_f = df_f[df_f["tahun"].isin(tahun_sel)]
    if status_sel and "status_pt" in df_f.columns:
        df_f = df_f[df_f["status_pt"].isin(status_sel + ["Tidak Diketahui"])]

    # ======================================================
    # MODE 1: PETA PROVINSI
    # ======================================================
    if tampilan == "Peta Provinsi":
        render_section_header("Sebaran per Provinsi", "Klik provinsi untuk melihat detail")

        # Aggregate by province
        prov_data = df_f[df_f["provinsi"] != "Tidak Diketahui"].groupby("provinsi").agg(
            jumlah=("provinsi", "count"),
            kampus=("universitas", lambda x: x[x != "Tidak Teridentifikasi"].nunique())
        ).reset_index()

        # Add coordinates
        prov_data["lat"] = prov_data["provinsi"].map(lambda p: PROVINSI_COORDS.get(p, (None, None))[0])
        prov_data["lon"] = prov_data["provinsi"].map(lambda p: PROVINSI_COORDS.get(p, (None, None))[1])
        prov_data = prov_data.dropna(subset=["lat", "lon"])

        # Normalize bubble size
        max_j = prov_data["jumlah"].max()
        prov_data["size"] = (prov_data["jumlah"] / max_j * 60).clip(lower=10)

        fig = go.Figure()

        # Indonesia basemap using scatter_geo
        fig.add_trace(go.Scattergeo(
            lat=prov_data["lat"],
            lon=prov_data["lon"],
            mode="markers+text",
            marker=dict(
                size=prov_data["size"],
                color=prov_data["jumlah"],
                colorscale=[[0, "#FADBD8"], [0.4, "#C0392B"], [1, "#5c0000"]],
                line=dict(color="white", width=1.5),
                opacity=0.85,
                colorbar=dict(
                    title=dict(text="Jumlah<br>Laporan", font=dict(size=11)),
                    thickness=12, len=0.6, x=1.01
                ),
                sizemode="diameter"
            ),
            text=prov_data["provinsi"].str.replace("DI ", "").str.replace("DKI ", ""),
            textposition="top center",
            textfont=dict(size=9, family="Inter", color="#1A1A2E"),
            customdata=list(zip(prov_data["provinsi"], prov_data["jumlah"], prov_data["kampus"])),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "📊 Laporan: <b>%{customdata[1]}</b><br>"
                "🏛️ Kampus: <b>%{customdata[2]}</b><br>"
                "<extra></extra>"
            ),
            name=""
        ))

        fig.update_layout(
            geo=dict(
                scope="asia",
                center=dict(lat=-2.5, lon=118),
                projection_scale=4.5,
                showland=True, landcolor="#F5F5F5",
                showocean=True, oceancolor="#EBF5FB",
                showcountries=True, countrycolor="#CCCCCC",
                showcoastlines=True, coastlinecolor="#AAAAAA",
                showframe=False,
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=520,
            margin=dict(l=0, r=0, t=20, b=0),
            font=dict(family="Inter, sans-serif"),
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---- Province Detail: Click Simulation via Selectbox ----
        st.markdown("<hr>", unsafe_allow_html=True)
        render_section_header("Detail Lokasi", "Pilih provinsi untuk melihat data lengkap")

        prov_list = sorted(prov_data["provinsi"].tolist())
        sel_prov = st.selectbox("Pilih Provinsi", options=prov_list,
                                 format_func=lambda x: f"📍 {x}")

        if sel_prov:
            df_prov = df_f[df_f["provinsi"] == sel_prov]
            df_prov_id = df_prov[df_prov["universitas"] != "Tidak Teridentifikasi"]

            total_p = len(df_prov)
            n_kampus = df_prov_id["universitas"].nunique() if len(df_prov_id) > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Laporan", f"{total_p:,}")
            col2.metric("Kampus Terdampak", str(n_kampus))

            if "jenis_kekerasan" in df_prov.columns:
                top_jenis = df_prov["jenis_kekerasan"].dropna()
                top_jenis = top_jenis[top_jenis != "Tidak Teridentifikasi"]
                if len(top_jenis) > 0:
                    col3.metric("Jenis Dominan", top_jenis.value_counts().index[0])

            if "pelaku" in df_prov.columns:
                top_p_col = df_prov["pelaku"].dropna()
                top_p_col = top_p_col[top_p_col != "Tidak Diketahui"]
                if len(top_p_col) > 0:
                    col4.metric("Pelaku Dominan", top_p_col.value_counts().index[0])

            # Universitas list in this province
            if len(df_prov_id) > 0:
                st.markdown("<br>", unsafe_allow_html=True)
                render_section_header(f"Kampus di {sel_prov}")
                univ_list = df_prov_id.groupby("universitas").agg(
                    laporan=("universitas", "count"),
                    status=("status_pt", lambda x: x.mode()[0] if len(x) > 0 else "-")
                ).reset_index().sort_values("laporan", ascending=False)
                univ_list.columns = ["Universitas", "Jumlah Laporan", "Status"]

                for _, row in univ_list.iterrows():
                    status_color = "#8B0000" if row["Status"] == "Negeri" else "#1A1A2E"
                    st.markdown(f"""
                    <div class="news-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div class="news-card-title">🏛️ {row['Universitas']}</div>
                            <div>
                                <span style="color:{status_color}; font-weight:700; font-size:0.88rem;">
                                    {row['Jumlah Laporan']} laporan
                                </span>
                                <span class="news-card-tag" style="margin-left:0.5rem;">{row['Status']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Recent news from this province
            if "judul" in df_prov.columns:
                recent = df_prov.dropna(subset=["judul"]).head(5)
                if len(recent) > 0:
                    import re
                    st.markdown("<br>", unsafe_allow_html=True)
                    render_section_header(f"Berita Terkait — {sel_prov}")
                    for _, row in recent.iterrows():
                        judul = re.sub(r'<[^>]+>', '', str(row.get("judul", "")))
                        judul = judul.split(" - ")[0][:100]
                        tanggal = str(row.get("tanggal", ""))[:10]
                        url = str(row.get("url", "#"))
                        st.markdown(f"""
                        <div class="news-card">
                            <div class="news-card-title">{judul}</div>
                            <div class="news-card-meta"><span>🗓️ {tanggal}</span>
                            <a href="{url}" target="_blank" style="color:#8B0000;">Baca →</a></div>
                        </div>
                        """, unsafe_allow_html=True)

    # ======================================================
    # MODE 2: PETA UNIVERSITAS
    # ======================================================
    else:
        render_section_header("Sebaran per Universitas", "Lokasi kampus yang muncul dalam pemberitaan")

        univ_data = df_f[df_f["universitas"] != "Tidak Teridentifikasi"].groupby("universitas").agg(
            jumlah=("universitas", "count"),
            provinsi=("provinsi", lambda x: x.mode()[0] if len(x) > 0 else "-"),
            status=("status_pt", lambda x: x.mode()[0] if len(x) > 0 else "-")
        ).reset_index()

        univ_data["lat"] = univ_data["universitas"].map(lambda u: UNIVERSITAS_COORDS.get(u, (None, None))[0])
        univ_data["lon"] = univ_data["universitas"].map(lambda u: UNIVERSITAS_COORDS.get(u, (None, None))[1])
        univ_data_geo = univ_data.dropna(subset=["lat", "lon"])
        univ_no_geo = univ_data[univ_data["lat"].isna()]

        max_j = univ_data_geo["jumlah"].max() if len(univ_data_geo) > 0 else 1
        univ_data_geo = univ_data_geo.copy()
        univ_data_geo["size"] = (univ_data_geo["jumlah"] / max_j * 55).clip(lower=12)

        fig2 = go.Figure()
        fig2.add_trace(go.Scattergeo(
            lat=univ_data_geo["lat"],
            lon=univ_data_geo["lon"],
            mode="markers+text",
            marker=dict(
                size=univ_data_geo["size"],
                color=univ_data_geo["jumlah"],
                colorscale=[[0, "#FADBD8"], [0.5, "#C0392B"], [1, "#5c0000"]],
                line=dict(color="white", width=1.5),
                opacity=0.88,
                colorbar=dict(title=dict(text="Laporan"), thickness=12, len=0.5, x=1.01),
                sizemode="diameter"
            ),
            text=univ_data_geo["universitas"].str.replace("Universitas ", "").str[:15],
            textposition="top center",
            textfont=dict(size=8, family="Inter"),
            customdata=list(zip(
                univ_data_geo["universitas"], univ_data_geo["jumlah"],
                univ_data_geo["provinsi"], univ_data_geo["status"]
            )),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "📊 Laporan: <b>%{customdata[1]}</b><br>"
                "📍 %{customdata[2]}<br>"
                "🏛️ PT %{customdata[3]}<br>"
                "<extra></extra>"
            ),
            name=""
        ))

        fig2.update_layout(
            geo=dict(
                scope="asia", center=dict(lat=-2.5, lon=118), projection_scale=4.5,
                showland=True, landcolor="#F5F5F5",
                showocean=True, oceancolor="#EBF5FB",
                showcountries=True, countrycolor="#CCCCCC",
                showcoastlines=True, coastlinecolor="#AAAAAA",
                showframe=False, bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            height=520, margin=dict(l=0, r=0, t=20, b=0),
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig2, use_container_width=True)

        # ---- Detail Universitas ----
        st.markdown("<hr>", unsafe_allow_html=True)
        render_section_header("Detail Universitas", "Pilih kampus untuk melihat profil lengkap")

        univ_list_all = sorted(univ_data["universitas"].tolist())
        sel_univ = st.selectbox("Pilih Universitas", options=univ_list_all,
                                 format_func=lambda x: f"🏛️ {x}")

        if sel_univ:
            df_u = df_f[df_f["universitas"] == sel_univ]
            total_u = len(df_u)

            st.markdown("<br>", unsafe_allow_html=True)
            row_info = univ_data[univ_data["universitas"] == sel_univ].iloc[0]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Laporan", f"{total_u:,}")
            col2.metric("Status PT", str(row_info.get("status", "-")))
            col3.metric("Provinsi", str(row_info.get("provinsi", "-")))

            if "tahun" in df_u.columns:
                tahun_aktif = df_u["tahun"].dropna().astype(int)
                if len(tahun_aktif) > 0:
                    col4.metric("Tahun Aktif", f"{int(tahun_aktif.min())}–{int(tahun_aktif.max())}")

            # Charts for this university
            if total_u > 0:
                col_l, col_r = st.columns(2)
                with col_l:
                    render_section_header("Tren Tahunan")
                    if "tahun" in df_u.columns:
                        tahunan = df_u.groupby("tahun").size().reset_index(name="n")
                        tahunan["tahun"] = tahunan["tahun"].astype(int).astype(str)
                        import plotly.express as px
                        fig_u = px.bar(tahunan, x="tahun", y="n",
                                       color="n", color_continuous_scale=["#FADBD8","#8B0000"],
                                       labels={"tahun":"Tahun","n":"Laporan"},
                                       text="n")
                        fig_u.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                             plot_bgcolor="rgba(0,0,0,0)", height=260,
                                             coloraxis_showscale=False,
                                             margin=dict(l=5,r=5,t=10,b=5),
                                             font=dict(family="Inter"))
                        fig_u.update_traces(textposition="outside")
                        st.plotly_chart(fig_u, use_container_width=True, config={"displayModeBar": False})

                with col_r:
                    render_section_header("Jenis Kekerasan")
                    if "jenis_kekerasan" in df_u.columns:
                        jenis = df_u["jenis_kekerasan"].dropna()
                        jenis = jenis[jenis != "Tidak Teridentifikasi"]
                        if len(jenis) > 0:
                            vc = jenis.value_counts().reset_index()
                            vc.columns = ["Jenis", "n"]
                            import plotly.express as px
                            fig_j = px.pie(vc, names="Jenis", values="n",
                                           color_discrete_sequence=["#8B0000","#1A1A2E","#D4A017",
                                                                     "#C0392B","#2E8B57","#4169E1"],
                                           hole=0.45)
                            fig_j.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                                height=260, margin=dict(l=5,r=5,t=10,b=5),
                                                font=dict(family="Inter"),
                                                legend=dict(font=dict(size=10)))
                            st.plotly_chart(fig_j, use_container_width=True, config={"displayModeBar": False})

                # Recent articles
                import re
                recent_u = df_u.dropna(subset=["judul"]).head(6)
                if len(recent_u) > 0:
                    render_section_header(f"Berita — {sel_univ}")
                    for _, row in recent_u.iterrows():
                        judul = re.sub(r'<[^>]+>', '', str(row.get("judul", ""))).split(" - ")[0][:100]
                        tanggal = str(row.get("tanggal", ""))[:10]
                        url = str(row.get("url", "#"))
                        jenis = str(row.get("jenis_kekerasan", ""))
                        st.markdown(f"""
                        <div class="news-card">
                            <div class="news-card-title">{judul}</div>
                            <div class="news-card-meta">
                                <span>🗓️ {tanggal}</span>
                                <span class="news-card-tag">{jenis}</span>
                                <a href="{url}" target="_blank" style="color:#8B0000;">Baca →</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        # Universities without coordinates
        if len(univ_no_geo) > 0:
            with st.expander(f"📍 {len(univ_no_geo)} kampus lainnya (koordinat belum tersedia)"):
                st.dataframe(univ_no_geo[["universitas", "jumlah", "provinsi", "status"]].rename(
                    columns={"universitas": "Universitas", "jumlah": "Laporan",
                             "provinsi": "Provinsi", "status": "Status"}
                ), use_container_width=True)

    # ---- Story ----
    st.markdown("<br>", unsafe_allow_html=True)
    render_story_box("Analisis Geografis", story_provinsi(df_f))

    render_footer()

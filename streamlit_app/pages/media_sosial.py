"""
pages/media_sosial.py
Halaman Media & YouTube — Analisis coverage media dan video
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.navbar import render_navbar, render_footer, render_section_header, render_story_box
from components.charts import chart_yt_top_video, chart_yt_trend


def render_media(df: pd.DataFrame, df_berita: pd.DataFrame, df_yt: pd.DataFrame):
    render_navbar("Media & YouTube")

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.8rem; font-weight:800;
                   color:#1A1A2E; margin-bottom:0.4rem;">📱 Analisis Media & YouTube</h2>
        <p style="color:#6C757D; font-size:0.92rem; font-family:'Inter',sans-serif;">
            Bagaimana media daring dan YouTube meliput isu kekerasan seksual di kampus?
            Analisis volume pemberitaan, engagement, dan tren konten dari waktu ke waktu.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["▶️ YouTube", "📰 Pemberitaan Media"])

    # ============================
    # TAB 1: YOUTUBE
    # ============================
    with tab1:
        if df_yt.empty:
            st.warning("Data YouTube tidak tersedia.")
        else:
            # ---- KPI Row ----
            col1, col2, col3, col4 = st.columns(4)
            total_yt = len(df_yt)
            total_views = int(df_yt["views"].sum()) if "views" in df_yt.columns else 0
            total_likes = int(df_yt["likes"].dropna().sum()) if "likes" in df_yt.columns else 0
            total_kom = int(df_yt["komentar"].dropna().sum()) if "komentar" in df_yt.columns else 0

            views_fmt = f"{total_views/1e6:.1f}M" if total_views >= 1e6 else f"{total_views/1e3:.0f}K"
            likes_fmt = f"{total_likes/1e3:.1f}K" if total_likes >= 1e3 else str(total_likes)

            col1.metric("Total Video", f"{total_yt:,}")
            col2.metric("Total Views", views_fmt)
            col3.metric("Total Likes", likes_fmt)
            col4.metric("Total Komentar", f"{total_kom:,}")

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Top Videos by Views ----
            render_section_header("Top Video Berdasarkan Views")
            fig_top = chart_yt_top_video(df_yt, top_n=10)
            st.plotly_chart(fig_top, use_container_width=True, config={"displayModeBar": False})

            render_story_box("Analisis Konten YouTube",
                f"Dari <strong>{total_yt:,} video YouTube</strong> yang dikumpulkan, total tayangan mencapai "
                f"<strong>{views_fmt}</strong> — menunjukkan betapa besarnya perhatian publik terhadap isu ini "
                f"di platform video. Video-video viral seringkali memiliki efek <em>agenda-setting</em> yang "
                f"kuat, mendorong lebih banyak korban berani melapor dan meningkatkan tekanan publik "
                f"terhadap institusi kampus untuk bertindak."
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Trend Upload ----
            render_section_header("Tren Unggahan Video per Tahun")
            fig_trend = chart_yt_trend(df_yt)
            st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Engagement Analysis ----
            render_section_header("Analisis Engagement")
            df_yt2 = df_yt.dropna(subset=["views", "likes"]).copy()
            df_yt2["engagement_rate"] = (df_yt2["likes"] / df_yt2["views"] * 100).clip(upper=10)
            df_yt2["label"] = df_yt2["judul"].str[:45] + "..."

            top_eng = df_yt2.nlargest(10, "engagement_rate")

            fig_eng = go.Figure(go.Bar(
                x=top_eng["engagement_rate"], y=top_eng["label"],
                orientation="h",
                marker=dict(
                    color=top_eng["engagement_rate"],
                    colorscale=[[0,"#FADBD8"],[1,"#1A1A2E"]],
                    line=dict(width=0)
                ),
                text=[f"{v:.2f}%" for v in top_eng["engagement_rate"]],
                textposition="outside",
                textfont=dict(size=10),
                hovertemplate="<b>%{y}</b><br>Engagement: %{x:.2f}%<extra></extra>"
            ))
            fig_eng.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=380, margin=dict(l=10,r=80,t=30,b=10),
                title=dict(text="Top 10 Video: Engagement Rate (Likes/Views)", font=dict(size=13), x=0.01),
                font=dict(family="Inter, sans-serif"),
                xaxis=dict(title="Engagement Rate (%)", showgrid=True, gridcolor="#E9ECEF"),
                yaxis=dict(tickfont=dict(size=9), showgrid=False)
            )
            st.plotly_chart(fig_eng, use_container_width=True, config={"displayModeBar": False})

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Channel Analysis ----
            render_section_header("Analisis per Channel")
            if "channel" in df_yt.columns:
                channel_data = df_yt.dropna(subset=["channel"]).groupby("channel").agg(
                    video=("channel", "count"),
                    total_views=("views", "sum"),
                    avg_views=("views", "mean")
                ).reset_index().sort_values("total_views", ascending=False).head(15)

                channel_data["total_views_fmt"] = channel_data["total_views"].apply(
                    lambda v: f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}K")
                channel_data["avg_views_fmt"] = channel_data["avg_views"].apply(
                    lambda v: f"{v/1e3:.0f}K")

                col_c1, col_c2 = st.columns([2, 1])
                with col_c1:
                    fig_ch = px.bar(channel_data, x="channel", y="total_views",
                                    color="video",
                                    color_continuous_scale=["#FADBD8","#8B0000"],
                                    labels={"channel":"Channel","total_views":"Total Views","video":"# Video"},
                                    text=channel_data["total_views_fmt"])
                    fig_ch.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                          plot_bgcolor="rgba(0,0,0,0)", height=360,
                                          font=dict(family="Inter"),
                                          xaxis=dict(tickangle=-35, showgrid=False),
                                          yaxis=dict(showgrid=True, gridcolor="#E9ECEF"),
                                          coloraxis_showscale=False,
                                          margin=dict(l=10,r=10,t=10,b=60))
                    fig_ch.update_traces(textposition="outside")
                    st.plotly_chart(fig_ch, use_container_width=True, config={"displayModeBar": False})

                with col_c2:
                    st.dataframe(
                        channel_data[["channel","video","total_views_fmt","avg_views_fmt"]].rename(
                            columns={"channel":"Channel","video":"Video",
                                     "total_views_fmt":"Total Views","avg_views_fmt":"Avg Views"}
                        ).reset_index(drop=True),
                        use_container_width=True, height=340
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Video List ----
            render_section_header("Daftar Semua Video")
            with st.expander("📋 Lihat Daftar Video Lengkap"):
                df_yt_show = df_yt[["judul","channel","tanggal_tayang","views","likes","komentar","url"]].copy()
                df_yt_show["views"] = df_yt_show["views"].fillna(0).astype(int)
                df_yt_show = df_yt_show.sort_values("views", ascending=False).reset_index(drop=True)
                df_yt_show.columns = ["Judul","Channel","Tanggal","Views","Likes","Komentar","URL"]
                st.dataframe(df_yt_show, use_container_width=True, height=400)

    # ============================
    # TAB 2: PEMBERITAAN MEDIA
    # ============================
    with tab2:
        if df_berita.empty:
            st.warning("Data berita tidak tersedia.")
        else:
            # ---- KPI ----
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Artikel", f"{len(df_berita):,}")
            if "tanggal" in df_berita.columns:
                df_b2 = df_berita.copy()
                df_b2["tanggal_dt"] = pd.to_datetime(df_b2["tanggal"], errors="coerce")
                df_b2 = df_b2.dropna(subset=["tanggal_dt"])
                if len(df_b2) > 0:
                    rentang = (df_b2["tanggal_dt"].max() - df_b2["tanggal_dt"].min()).days
                    col2.metric("Rentang Waktu", f"{rentang} hari")
                    col3.metric("Rata-rata per Minggu", f"{len(df_berita)/(rentang/7+1):.0f}")

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Volume per month ----
            render_section_header("Volume Pemberitaan per Bulan")
            if "tanggal" in df_berita.columns:
                df_b3 = df_berita.copy()
                df_b3["tanggal_dt"] = pd.to_datetime(df_b3["tanggal"], errors="coerce")
                df_b3 = df_b3.dropna(subset=["tanggal_dt"])
                df_b3["year_month"] = df_b3["tanggal_dt"].dt.to_period("M").astype(str)
                ym = df_b3.groupby("year_month").size().reset_index(name="n")
                ym = ym.sort_values("year_month")

                fig_ym = go.Figure()
                fig_ym.add_trace(go.Scatter(
                    x=ym["year_month"], y=ym["n"],
                    mode="lines+markers",
                    line=dict(color="#8B0000", width=2.5),
                    marker=dict(size=7, color="#8B0000"),
                    fill="tozeroy",
                    fillcolor="rgba(139,0,0,0.08)",
                    hovertemplate="<b>%{x}</b><br>Artikel: %{y}<extra></extra>"
                ))
                fig_ym.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    height=320, margin=dict(l=10,r=10,t=20,b=10),
                    font=dict(family="Inter,sans-serif"),
                    xaxis=dict(showgrid=False, tickangle=-35),
                    yaxis=dict(showgrid=True, gridcolor="#E9ECEF", title="Jumlah Artikel")
                )
                st.plotly_chart(fig_ym, use_container_width=True, config={"displayModeBar": False})

            # ---- Keyword Analysis ----
            if "keyword" in df_berita.columns:
                render_section_header("Distribusi Keyword Pencarian")
                kw_data = df_berita["keyword"].dropna().value_counts().head(15).reset_index()
                kw_data.columns = ["keyword", "n"]

                fig_kw = px.bar(kw_data, x="n", y="keyword", orientation="h",
                                color="n", color_continuous_scale=["#FADBD8","#8B0000"],
                                labels={"n":"Jumlah Artikel","keyword":"Keyword"},
                                text="n")
                fig_kw.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                      plot_bgcolor="rgba(0,0,0,0)", height=400,
                                      font=dict(family="Inter"), coloraxis_showscale=False,
                                      xaxis=dict(showgrid=True, gridcolor="#E9ECEF"),
                                      yaxis=dict(tickfont=dict(size=10)),
                                      margin=dict(l=10,r=50,t=20,b=10))
                fig_kw.update_traces(textposition="outside", textfont_size=10)
                st.plotly_chart(fig_kw, use_container_width=True, config={"displayModeBar": False})

            # ---- Recent Articles ----
            st.markdown("<br>", unsafe_allow_html=True)
            render_section_header("Artikel Terbaru")

            kw_filter = "Semua"
            if "keyword" in df_berita.columns:
                kw_opts = ["Semua"] + df_berita["keyword"].dropna().unique().tolist()
                kw_filter = st.selectbox("Filter berdasarkan Keyword", kw_opts)

            df_b_show = df_berita.copy()
            if kw_filter != "Semua" and "keyword" in df_b_show.columns:
                df_b_show = df_b_show[df_b_show["keyword"] == kw_filter]

            for _, row in df_b_show.dropna(subset=["judul"]).head(20).iterrows():
                judul = re.sub(r'<[^>]+>', '', str(row.get("judul",""))).split(" - ")[0][:110]
                tanggal = str(row.get("tanggal",""))[:10]
                sumber = str(row.get("sumber",""))
                url = str(row.get("url","#"))
                kw = str(row.get("keyword",""))
                st.markdown(f"""
                <div class="news-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;">
                        <div>
                            <div class="news-card-title">{judul}</div>
                            <div class="news-card-meta" style="margin-top:0.3rem;">
                                <span>📰 {sumber}</span>
                                <span>🗓️ {tanggal}</span>
                                <span class="news-card-tag">{kw}</span>
                            </div>
                        </div>
                        <a href="{url}" target="_blank" style="color:#8B0000; font-weight:600;
                           font-size:0.82rem; white-space:nowrap; font-family:'Inter',sans-serif;">Baca →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    render_footer()

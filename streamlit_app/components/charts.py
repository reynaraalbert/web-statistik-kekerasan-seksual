"""
components/charts.py
Reusable chart functions with consistent IDX-style color palette
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ---- Color Palette ----
COLORS_RED = ["#8B0000", "#A52A2A", "#C0392B", "#E74C3C", "#F1948A", "#FADBD8"]
COLORS_NAVY = ["#1A1A2E", "#16213E", "#0F3460", "#533483", "#7B2D8B", "#A64AC9"]
COLORS_MULTI = ["#8B0000", "#1A1A2E", "#D4A017", "#2E8B57", "#4169E1", "#8B008B",
                "#FF6B35", "#2D6A4F", "#0077B6", "#F72585"]
CHART_BG = "rgba(0,0,0,0)"
GRID_COLOR = "#E9ECEF"
FONT_FAMILY = "Inter, Plus Jakarta Sans, sans-serif"

def base_layout(title="", height=400, showlegend=True):
    return dict(
        title=dict(text=title, font=dict(size=14, family=FONT_FAMILY, color="#1A1A2E"), x=0.01),
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family=FONT_FAMILY, size=12, color="#343A40"),
        height=height,
        margin=dict(l=10, r=10, t=50 if title else 20, b=20),
        showlegend=showlegend,
        legend=dict(
            orientation="h", x=0, y=-0.15,
            font=dict(size=11, family=FONT_FAMILY)
        ),
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR, gridwidth=1,
            zeroline=False, tickfont=dict(size=11)
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR, gridwidth=1,
            zeroline=False, tickfont=dict(size=11)
        ),
    )


def chart_trend_tahunan(df: pd.DataFrame, col_tahun="tahun", title="Tren Kasus per Tahun"):
    """Line + bar combo for yearly trend"""
    data = df.groupby(col_tahun).size().reset_index(name="jumlah")
    data = data[data[col_tahun].notna()].sort_values(col_tahun)
    data[col_tahun] = data[col_tahun].astype(int).astype(str)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data[col_tahun], y=data["jumlah"],
        name="Jumlah Kasus",
        marker=dict(
            color=data["jumlah"],
            colorscale=[[0, "#FADBD8"], [0.5, "#C0392B"], [1, "#5c0000"]],
            line=dict(width=0)
        ),
        text=data["jumlah"], textposition="outside",
        textfont=dict(size=12, family=FONT_FAMILY, color="#1A1A2E"),
        hovertemplate="<b>%{x}</b><br>Kasus: %{y}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=data[col_tahun], y=data["jumlah"],
        name="Tren",
        mode="lines+markers",
        line=dict(color="#D4A017", width=2.5, dash="solid"),
        marker=dict(color="#D4A017", size=8, symbol="circle"),
        hoverinfo="skip"
    ))

    layout = base_layout(title, height=380)
    layout["xaxis"]["title"] = "Tahun"
    layout["yaxis"]["title"] = "Jumlah Laporan"
    fig.update_layout(**layout)
    return fig


def chart_jenis_kekerasan(df: pd.DataFrame, col="jenis_kekerasan", title="Distribusi Jenis Kekerasan"):
    """Donut chart for violence types"""
    data = df[col].dropna()
    data = data[data != "Tidak Teridentifikasi"]
    vc = data.value_counts().reset_index()
    vc.columns = ["jenis", "jumlah"]

    fig = go.Figure(go.Pie(
        labels=vc["jenis"], values=vc["jumlah"],
        hole=0.55,
        marker=dict(colors=COLORS_MULTI, line=dict(color="white", width=2)),
        textfont=dict(size=11, family=FONT_FAMILY),
        hovertemplate="<b>%{label}</b><br>%{value} kasus (%{percent})<extra></extra>",
        showlegend=True
    ))
    fig.add_annotation(
        text=f"<b>{len(data):,}</b><br><span style='font-size:10px'>Total</span>",
        showarrow=False, font=dict(size=14, family=FONT_FAMILY, color="#1A1A2E"),
        x=0.5, y=0.5
    )
    layout = base_layout(title, height=370, showlegend=True)
    layout["legend"]["orientation"] = "v"
    layout["legend"]["x"] = 1.02
    layout["legend"]["y"] = 0.5
    layout.pop("xaxis"); layout.pop("yaxis")
    fig.update_layout(**layout)
    return fig


def chart_pelaku(df: pd.DataFrame, col="pelaku", title="Distribusi Pelaku"):
    """Horizontal bar chart for perpetrators"""
    data = df[col].dropna()
    data = data[data != "Tidak Diketahui"]
    vc = data.value_counts().reset_index()
    vc.columns = ["pelaku", "jumlah"]
    vc = vc.sort_values("jumlah")

    fig = go.Figure(go.Bar(
        x=vc["jumlah"], y=vc["pelaku"],
        orientation="h",
        marker=dict(
            color=vc["jumlah"],
            colorscale=[[0, "#FADBD8"], [1, "#8B0000"]],
            line=dict(width=0)
        ),
        text=vc["jumlah"], textposition="outside",
        textfont=dict(size=11, family=FONT_FAMILY),
        hovertemplate="<b>%{y}</b><br>%{x} kasus<extra></extra>"
    ))
    layout = base_layout(title, height=max(300, len(vc) * 45))
    layout["yaxis"]["title"] = ""
    layout["xaxis"]["title"] = "Jumlah Kasus"
    layout["yaxis"]["tickfont"] = dict(size=12)
    fig.update_layout(**layout)
    return fig


def chart_status_pt(df: pd.DataFrame, col="status_pt", title="Status Perguruan Tinggi"):
    """Pie chart for PT status"""
    data = df[col].dropna()
    data = data[data != "Tidak Diketahui"]
    vc = data.value_counts().reset_index()
    vc.columns = ["status", "jumlah"]

    fig = go.Figure(go.Pie(
        labels=vc["status"], values=vc["jumlah"],
        marker=dict(colors=["#8B0000", "#1A1A2E"], line=dict(color="white", width=3)),
        textfont=dict(size=13, family=FONT_FAMILY),
        textinfo="label+percent+value",
        hovertemplate="<b>%{label}</b><br>%{value} kasus (%{percent})<extra></extra>"
    ))
    layout = base_layout(title, height=320, showlegend=False)
    layout.pop("xaxis"); layout.pop("yaxis")
    fig.update_layout(**layout)
    return fig


def chart_top_universitas(df: pd.DataFrame, top_n=15, col="universitas", title="Top Universitas"):
    """Ranked bar chart for universities"""
    data = df[col].dropna()
    data = data[data != "Tidak Teridentifikasi"]
    vc = data.value_counts().head(top_n).reset_index()
    vc.columns = ["universitas", "jumlah"]
    vc = vc.sort_values("jumlah")

    # Shorten long names
    vc["label"] = vc["universitas"].str.replace("Universitas ", "Univ. ", regex=False)
    vc["label"] = vc["label"].str[:35]

    fig = go.Figure(go.Bar(
        x=vc["jumlah"], y=vc["label"],
        orientation="h",
        marker=dict(
            color=list(range(len(vc))),
            colorscale=[[0, "#FADBD8"], [0.5, "#C0392B"], [1, "#5c0000"]],
            line=dict(width=0)
        ),
        text=vc["jumlah"], textposition="outside",
        textfont=dict(size=11, family=FONT_FAMILY),
        customdata=vc["universitas"],
        hovertemplate="<b>%{customdata}</b><br>%{x} kasus<extra></extra>"
    ))
    layout = base_layout(title, height=max(350, top_n * 40))
    layout["yaxis"]["tickfont"] = dict(size=11)
    layout["xaxis"]["title"] = "Jumlah Laporan"
    fig.update_layout(**layout)
    return fig


def chart_bulanan_heatmap(df: pd.DataFrame, col_bulan="bulan", col_tahun="tahun", title="Distribusi Kasus per Bulan & Tahun"):
    """Heatmap of cases by month and year"""
    urutan_bulan = ["January","February","March","April","May","June",
                    "July","August","September","October","November","December"]
    label_bulan = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Ags","Sep","Okt","Nov","Des"]

    df2 = df[df[col_tahun].notna() & df[col_bulan].notna()].copy()
    df2[col_tahun] = df2[col_tahun].astype(int).astype(str)
    pivot = df2.groupby([col_tahun, col_bulan]).size().reset_index(name="n")
    pivot = pivot[pivot[col_bulan].isin(urutan_bulan)]
    pivot_table = pivot.pivot(index=col_bulan, columns=col_tahun, values="n").fillna(0)
    pivot_table = pivot_table.reindex(urutan_bulan)
    pivot_table.index = [label_bulan[urutan_bulan.index(b)] if b in urutan_bulan else b
                         for b in pivot_table.index]

    fig = go.Figure(go.Heatmap(
        z=pivot_table.values, x=pivot_table.columns, y=pivot_table.index,
        colorscale=[[0, "#FFF5F5"], [0.5, "#C0392B"], [1, "#5c0000"]],
        hovertemplate="<b>%{y} %{x}</b><br>%{z} kasus<extra></extra>",
        text=pivot_table.values.astype(int),
        texttemplate="%{text}",
        textfont=dict(size=10, family=FONT_FAMILY),
        showscale=True
    ))
    layout = base_layout(title, height=350, showlegend=False)
    layout.pop("xaxis"); layout.pop("yaxis")
    fig.update_layout(**layout)
    return fig


def chart_provinsi_bar(df: pd.DataFrame, top_n=15, col="provinsi", title="Sebaran per Provinsi"):
    """Bar chart for provinces"""
    data = df[col].dropna()
    data = data[data != "Tidak Diketahui"]
    vc = data.value_counts().head(top_n).reset_index()
    vc.columns = ["provinsi", "jumlah"]

    fig = go.Figure(go.Bar(
        x=vc["provinsi"], y=vc["jumlah"],
        marker=dict(
            color=vc["jumlah"],
            colorscale=[[0, "#FADBD8"], [1, "#8B0000"]],
            line=dict(width=0)
        ),
        text=vc["jumlah"], textposition="outside",
        textfont=dict(size=11, family=FONT_FAMILY),
        hovertemplate="<b>%{x}</b><br>%{y} kasus<extra></extra>"
    ))
    layout = base_layout(title, height=380)
    layout["xaxis"]["tickangle"] = -35
    layout["yaxis"]["title"] = "Jumlah Laporan"
    fig.update_layout(**layout)
    return fig


def chart_yt_top_video(df: pd.DataFrame, top_n=10, title="Top Video YouTube Berdasarkan Views"):
    """Horizontal bar for top YouTube videos"""
    df2 = df.dropna(subset=["views"]).nlargest(top_n, "views").copy()
    df2["label"] = df2["judul"].str[:50] + "..."

    fig = go.Figure(go.Bar(
        x=df2["views"].values[::-1], y=df2["label"].values[::-1],
        orientation="h",
        marker=dict(
            color=list(range(top_n)),
            colorscale=[[0, "#FADBD8"], [1, "#8B0000"]],
            line=dict(width=0)
        ),
        text=[f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}K" for v in df2["views"].values[::-1]],
        textposition="outside",
        textfont=dict(size=10, family=FONT_FAMILY),
        hovertemplate="<b>%{y}</b><br>Views: %{x:,.0f}<extra></extra>"
    ))
    layout = base_layout(title, height=max(350, top_n * 42))
    layout["yaxis"]["tickfont"] = dict(size=10)
    layout["xaxis"]["title"] = "Jumlah Views"
    fig.update_layout(**layout)
    return fig


def chart_yt_trend(df: pd.DataFrame, col_tahun="tanggal_tayang", title="Tren Upload Video per Tahun"):
    """Trend of YT video uploads by year"""
    df2 = df.dropna(subset=[col_tahun]).copy()
    df2["tahun"] = pd.to_datetime(df2[col_tahun], errors="coerce").dt.year
    df2 = df2.dropna(subset=["tahun"])
    vc = df2.groupby("tahun").agg(
        video=("tahun", "count"),
        total_views=("views", "sum")
    ).reset_index()
    vc["tahun"] = vc["tahun"].astype(int).astype(str)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=vc["tahun"], y=vc["video"], name="Jumlah Video",
        marker_color="#8B0000",
        hovertemplate="<b>%{x}</b><br>Video: %{y}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=vc["tahun"], y=vc["total_views"] / 1e6,
        name="Total Views (juta)", yaxis="y2",
        mode="lines+markers",
        line=dict(color="#D4A017", width=2.5),
        marker=dict(size=8, color="#D4A017"),
        hovertemplate="<b>%{x}</b><br>Views: %{y:.1f}M<extra></extra>"
    ))
    layout = base_layout(title, height=380)
    layout["yaxis"]["title"] = "Jumlah Video"
    layout["yaxis2"] = dict(
        title="Views (Juta)", overlaying="y", side="right",
        showgrid=False, tickfont=dict(size=11, color="#D4A017")
    )
    fig.update_layout(**layout)
    return fig

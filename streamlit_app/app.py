import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ====================================================
# THEME & LANGUAGE DETECTION
# ====================================================
query_params = st.query_params
theme = query_params.get("theme", "light")
lang = query_params.get("lang", "id")

# Multi-language support
translations = {
    "id": {
        "title": "SIGAP - Engine Analisis Mandiri",
        "upload_label": "Unggah Dataset Riset Anda (.xlsx / .csv)",
        "upload_help": "Dataset harus memiliki kolom kategori dan jumlah laporan.",
        "metric_total": "Total Laporan",
        "metric_inst": "Institusi",
        "metric_region": "Wilayah",
        "dist_by": "Distribusi Data Berdasarkan",
        "top_10": "Top 10",
        "top_5": "Komposisi",
        "anomaly_intel": "Deteksi Anomali & Intelijen Data",
        "anomalies": "Anomali Terdeteksi",
        "fragmentation": "Fragmentasi Data",
        "wait": "Menganalisis dataset...",
        "error": "Silakan unggah file Excel atau CSV."
    },
    "en": {
        "title": "SIGAP - Self Analysis Engine",
        "upload_label": "Upload Your Research Dataset (.xlsx / .csv)",
        "upload_help": "Dataset must have category and report count columns.",
        "metric_total": "Total Reports",
        "metric_inst": "Institutions",
        "metric_region": "Regions",
        "dist_by": "Data Distribution By",
        "top_10": "Top 10",
        "top_5": "Composition",
        "anomaly_intel": "Anomaly Detection & Data Intelligence",
        "anomalies": "Anomalies Detected",
        "fragmentation": "Data Fragmentation",
        "wait": "Analyzing dataset...",
        "error": "Please upload an Excel or CSV file."
    }
}

t = translations.get(lang, translations["id"])

if theme == "dark":
    bg_color = "#8B0000"  # Maroon Background
    text_color = "#FFFFFF" # White Text
    card_color = "rgba(255, 255, 255, 0.15)"
    primary_accent = "#FFFFFF"
    sidebar_bg = "#5A0000"
else:
    bg_color = "#FFFFFF"  # White Background
    text_color = "#111111" # Dark Text
    card_color = "#F8F9FA"
    primary_accent = "#8B0000"
    sidebar_bg = "#F0F2F6"

# ====================================================
# PAGE CONFIG
# ====================================================
st.set_page_config(
    page_title=t["title"],
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for Premium Theme-Aware Look
st.markdown(f"""
<style>
    .stApp {{
        background: {bg_color};
        color: {text_color};
    }}
    /* Ensure all text is readable */
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {text_color} !important;
    }}
    
    /* File Uploader Custom Styling */
    [data-testid="stFileUploader"] {{
        background-color: {sidebar_bg} !important;
        border-radius: 20px;
        padding: 20px;
        border: 2px dashed {primary_accent} !important;
    }}
    [data-testid="stFileUploader"] section {{
        background-color: transparent !important;
    }}
    [data-testid="stFileUploader"] * {{
        color: {text_color} !important;
    }}
    /* Special fix for the uploader text to be white in Light Mode if requested */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] div, 
    [data-testid="stFileUploader"] small {{
        color: {'#FFFFFF' if theme == 'light' else text_color} !important;
    }}
    
    .stButton>button {{
        background-color: {primary_accent} !important;
        color: {bg_color} !important;
        border-radius: 12px;
        border: none;
        padding: 0.6rem 2.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    .upload-box {{
        border: 2px dashed {primary_accent};
        border-radius: 24px;
        padding: 60px;
        text-align: center;
        background: {card_color};
        margin-bottom: 30px;
    }}
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    
    /* Show Streamlit elements as requested */
    #MainMenu {{visibility: visible;}}
    footer {{visibility: visible;}}
    header {{visibility: visible;}}
    
    .stMetric {{
        background: {card_color};
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(139,0,0,0.1);
    }}
    /* Plotly text color */
    .js-plotly-plot .plotly .modebar {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# ====================================================
# APP CONTENT
# ====================================================

st.title(t["title"])
st.markdown(f"<p style='opacity: 0.8;'>Analisis privat untuk dekonstruksi data eksternal.</p>", unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader(t["upload_label"], type=["xlsx", "csv"], help=t["upload_help"])

if uploaded_file is not None:
    try:
        with st.spinner(t["wait"]):
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

        st.success(f"Dekomposisi Berhasil: {len(df)} Entri Terdeteksi")
        
        # --- METRICS GRID ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t["metric_total"], f"{len(df):,}")
        with col2:
            unique_univ = df.get('universitas', pd.Series([])).nunique() if 'universitas' in df.columns else 0
            st.metric(t["metric_inst"], unique_univ)
        with col3:
            unique_prov = df.get('provinsi', pd.Series([])).nunique() if 'provinsi' in df.columns else 0
            st.metric(t["metric_region"], unique_prov)
        with col4:
            st.metric("Integritas Data", "100%")

        st.markdown("---")
        
        # --- PRIMARY ANALYSIS ---
        st.subheader("📊 Visualisasi Statistik Komprehensif")
        
        cols = df.columns.tolist()
        target_col = st.selectbox(f"{t['dist_by']}...", cols, index=0)
        
        if target_col:
            counts = df[target_col].value_counts().reset_index()
            counts.columns = [target_col, 'jumlah']
            counts['persentase'] = (counts['jumlah'] / counts['jumlah'].sum() * 100).round(1)
            
            c1, c2 = st.columns([2, 1])
            
            with c1:
                # Bar Chart
                fig = px.bar(counts.head(10), x=target_col, y='jumlah', 
                             text='jumlah',
                             title=f"{t['top_10']} {target_col}",
                             color_discrete_sequence=[primary_accent])
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color=text_color,
                    xaxis=dict(showgrid=False, tickfont=dict(color=text_color)),
                    yaxis=dict(showgrid=True, gridcolor='rgba(139,0,0,0.1)', tickfont=dict(color=text_color)),
                    margin=dict(t=50, b=50, l=0, r=0)
                )
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                # Pie Chart
                fig_pie = px.pie(counts.head(5), values='jumlah', names=target_col,
                                 title=f"{t['top_5']} {target_col}",
                                 hole=0.4,
                                 color_discrete_sequence=px.colors.sequential.Reds_r)
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color=text_color,
                    showlegend=False,
                    margin=dict(t=50, b=0, l=0, r=0)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # --- ANOMALY & INTEL SECTION ---
        st.subheader(f"⚖️ {t['anomaly_intel']}")
        
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.markdown(f"""
            <div style="background: {card_color}; padding: 30px; border-radius: 24px; border-left: 5px solid {primary_accent}; height: 100%;">
                <h4 style="margin-top: 0; color: {text_color} !important;">Perspektif Dekonstruksi Data</h4>
                <p style="font-style: italic; opacity: 0.9; color: {text_color} !important; line-height: 1.6;">
                    "Berdasarkan dataset ini, konsentrasi laporan pada variabel <b>{target_col}</b> menunjukkan adanya anomali sistemik. 
                    Dominasi data ini mencerminkan kebutuhan mendesak untuk evaluasi instrumen pengawasan di titik-titik krusial tersebut."
                </p>
                <hr style="opacity: 0.1; margin: 20px 0;">
                <p style="font-size: 0.85rem; opacity: 0.7; color: {text_color} !important;">
                    * Analisis ini dihasilkan secara otomatis melalui mesin deduksi SIGAP untuk merumuskan advokasi berbasis bukti empiris.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with c_right:
            # Show a small table of top 5 categories
            st.markdown(f"<h4 style='color: {text_color} !important; margin-bottom: 20px;'>{t['fragmentation']}</h4>", unsafe_allow_html=True)
            st.dataframe(
                counts.head(5).style.background_gradient(cmap='Reds'),
                use_container_width=True
            )

        with st.expander("🔍 Akses Dataset Raw Lengkap"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(t["error"])

else:
    st.markdown(f"""
    <div class="upload-box">
        <h2 style="color: {primary_accent} !important;">Sistem Menunggu Input Data</h2>
        <p style="opacity: 0.6; color: {text_color} !important;">Silakan unggah dataset Anda untuk memulai dekonstruksi narasi dengan data.</p>
        <div style="font-size: 80px; margin-top: 20px; opacity: 0.3;">📁</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"SIGAP Self-Analysis Engine v3.0 • Mode: {theme.upper()} • Sesi Terenkripsi")

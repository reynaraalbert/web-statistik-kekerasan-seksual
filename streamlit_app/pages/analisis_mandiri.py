"""
pages/analisis_mandiri.py
Halaman Upload Data Mandiri — Auto Storytelling dari data user
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.navbar import render_navbar, render_footer, render_section_header, render_story_box
from components.storytelling import generate_auto_story
from components.charts import (chart_trend_tahunan, chart_jenis_kekerasan, chart_pelaku,
                                chart_top_universitas, chart_provinsi_bar, chart_bulanan_heatmap)

# Kolom standar RISET yang dikenali sistem
STANDARD_COLS = {
    "universitas": ["universitas", "kampus", "perguruan tinggi", "university", "institusi", "pt"],
    "provinsi": ["provinsi", "province", "wilayah", "region"],
    "kota": ["kota", "kabupaten", "city", "kabkota"],
    "jenis_kekerasan": ["jenis_kekerasan", "jenis kekerasan", "jenis", "type", "kategori", "kategori_kekerasan"],
    "pelaku": ["pelaku", "perpetrator", "tersangka", "aktor"],
    "tahun": ["tahun", "year", "thn"],
    "bulan": ["bulan", "month", "bln"],
    "status_pt": ["status_pt", "status pt", "akreditasi", "negeri_swasta", "tipe_pt"],
}


def detect_columns(df_cols: list) -> dict:
    """Auto-detect column mapping from user file"""
    mapping = {}
    cols_lower = {c: c.lower().strip() for c in df_cols}
    for std_col, aliases in STANDARD_COLS.items():
        for orig_col, col_low in cols_lower.items():
            if col_low in aliases or any(a in col_low for a in aliases):
                mapping[std_col] = orig_col
                break
    return mapping


def render_mandiri():
    render_navbar("Analisis Mandiri")

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.8rem; font-weight:800;
                   color:#1A1A2E; margin-bottom:0.4rem;">📤 Analisis Data Mandiri</h2>
        <p style="color:#6C757D; font-size:0.92rem; font-family:'Inter',sans-serif;">
            Miliki data kekerasan seksual yang berbeda? Upload file Excel atau CSV Anda dan
            sistem akan otomatis membuat visualisasi serta narasi storytelling yang sesuai.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---- Panduan Format ----
    with st.expander("📋 Panduan Format Data yang Didukung", expanded=False):
        st.markdown("""
        <div class="upload-guide">
            <h4>Kolom yang Dikenali Secara Otomatis</h4>
            <p style="font-size:0.83rem; color:#6C757D; margin-bottom:0.7rem;">
                Sistem akan mendeteksi kolom-kolom berikut secara otomatis berdasarkan nama kolomnya.
                Kolom tidak harus persis sama — sistem mengenali berbagai variasi nama.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Kolom Utama (disarankan ada):**")
            for col, aliases in list(STANDARD_COLS.items())[:4]:
                badges = " ".join([f'<span class="col-badge">{a}</span>' for a in aliases[:3]])
                st.markdown(f"**`{col}`** → {badges}", unsafe_allow_html=True)
        with col_b:
            st.markdown("**Kolom Tambahan (opsional):**")
            for col, aliases in list(STANDARD_COLS.items())[4:]:
                badges = " ".join([f'<span class="col-badge optional">{a}</span>' for a in aliases[:3]])
                st.markdown(f"**`{col}`** → {badges}", unsafe_allow_html=True)

        st.markdown("""
        <div class="alert-box info" style="margin-top:0.75rem;">
            💡 <strong>Tips:</strong> Data tidak harus hanya tentang kekerasan seksual — sistem bisa
            menganalisis data apapun yang memiliki kolom lokasi, waktu, dan kategori.
            Semakin banyak kolom yang cocok, semakin kaya analisis yang dihasilkan.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Upload Zone ----
    render_section_header("Upload File Data")
    uploaded_file = st.file_uploader(
        "Drag & drop file di sini, atau klik untuk memilih",
        type=["xlsx", "xls", "csv"],
        help="Format yang didukung: Excel (.xlsx, .xls) dan CSV (.csv)"
    )

    if uploaded_file is None:
        # Show example/demo mode
        st.markdown("""
        <div style="text-align:center; padding:3rem 2rem; background:#F8F9FA; border-radius:12px;
                    border: 2px dashed #DEE2E6; margin:1rem 0;">
            <div style="font-size:3rem; margin-bottom:1rem;">📊</div>
            <h3 style="font-family:'Plus Jakarta Sans',sans-serif; color:#1A1A2E; margin-bottom:0.5rem;">
                Belum ada file yang diupload
            </h3>
            <p style="color:#6C757D; font-size:0.88rem; max-width:400px; margin:0 auto;">
                Upload file Excel atau CSV Anda di atas untuk mendapatkan analisis statistik
                dan narasi storytelling otomatis dari data Anda.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("Atau Coba Demo dengan Data RISET Resmi")
        if st.button("🎯 Jalankan Demo dengan Data Bawaan", type="primary"):
            st.session_state["use_demo"] = True
            st.rerun()
    else:
        st.session_state["use_demo"] = False

    # ---- Load Data ----
    df_user = None
    source_label = ""

    if st.session_state.get("use_demo", False) and uploaded_file is None:
        base = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base, "data")
        riset_files = sorted([f for f in os.listdir(data_dir) if f.startswith("RISET_") and f.endswith(".xlsx")], reverse=True)
        if riset_files:
            df_user = pd.read_excel(os.path.join(data_dir, riset_files[0]))
            source_label = f"📦 Demo: {riset_files[0]}"

    elif uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                # Try different encodings
                for enc in ["utf-8", "latin-1", "cp1252"]:
                    try:
                        uploaded_file.seek(0)
                        df_user = pd.read_csv(uploaded_file, encoding=enc)
                        break
                    except UnicodeDecodeError:
                        continue
            else:
                df_user = pd.read_excel(uploaded_file)
            source_label = f"📄 {uploaded_file.name}"
        except Exception as e:
            st.error(f"❌ Gagal membaca file: {str(e)}")
            return

    # ---- Process & Display ----
    if df_user is not None:
        st.markdown(f"""
        <div class="upload-success">
            ✅ <strong>File berhasil dimuat!</strong> {source_label} —
            <strong>{len(df_user):,} baris</strong>, <strong>{len(df_user.columns)} kolom</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- Column Detection ----
        kolom_map = detect_columns(df_user.columns.tolist())
        n_detected = len(kolom_map)

        render_section_header("Deteksi Kolom Otomatis", f"{n_detected}/{len(STANDARD_COLS)} kolom standar terdeteksi")

        # Show mapping
        col_info_a, col_info_b = st.columns(2)
        with col_info_a:
            st.markdown("**Kolom Terdeteksi:**")
            if kolom_map:
                for std, orig in kolom_map.items():
                    st.markdown(f"✅ `{std}` ← **{orig}**")
            else:
                st.markdown("*Tidak ada kolom standar yang terdeteksi*")

        with col_info_b:
            st.markdown("**Semua Kolom di File Anda:**")
            for c in df_user.columns:
                is_mapped = c in kolom_map.values()
                badge = "✅" if is_mapped else "⬜"
                st.markdown(f"{badge} `{c}`")

        # Allow manual override
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("⚙️ Atur Mapping Kolom Secara Manual"):
            all_cols = [None] + df_user.columns.tolist()
            manual_map = {}
            col_m1, col_m2 = st.columns(2)
            std_keys = list(STANDARD_COLS.keys())
            for i, std_col in enumerate(std_keys):
                target_col = col_m1 if i < len(std_keys)//2 else col_m2
                with target_col:
                    default_val = kolom_map.get(std_col, None)
                    sel = st.selectbox(
                        f"{std_col}",
                        options=all_cols,
                        index=all_cols.index(default_val) if default_val in all_cols else 0,
                        key=f"map_{std_col}"
                    )
                    if sel:
                        manual_map[std_col] = sel

            if manual_map:
                kolom_map = manual_map

        # ---- Rename to standard ----
        df_std = df_user.rename(columns={v: k for k, v in kolom_map.items() if v in df_user.columns})
        if "tahun" in df_std.columns:
            df_std["tahun"] = pd.to_numeric(df_std["tahun"], errors="coerce")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ============================
        # AUTO STORYTELLING
        # ============================
        render_section_header("Ringkasan Data", "Auto-generated dari file Anda")

        total_rows = len(df_std)
        st.markdown(f"""
        <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1rem;">
            <div class="stat-card" style="flex:1; min-width:150px;">
                <div class="stat-card-value">{total_rows:,}</div>
                <div class="stat-card-label">Total Baris</div>
            </div>
            <div class="stat-card" style="flex:1; min-width:150px; border-left-color:#1A1A2E;">
                <div class="stat-card-value" style="color:#1A1A2E;">{len(df_std.columns)}</div>
                <div class="stat-card-label">Jumlah Kolom</div>
            </div>
            <div class="stat-card" style="flex:1; min-width:150px; border-left-color:#D4A017;">
                <div class="stat-card-value" style="color:#D4A017;">{n_detected}</div>
                <div class="stat-card-label">Kolom Terdeteksi</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ---- Data Preview ----
        with st.expander("👁️ Preview Data (5 baris pertama)"):
            st.dataframe(df_std.head(5), use_container_width=True)

        # ---- Generate Visualizations ----
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("Visualisasi Otomatis", "Chart yang dihasilkan dari data Anda")

        # Only show charts for detected columns
        tabs_to_show = []
        if "tahun" in df_std.columns:
            tabs_to_show.append("📈 Tren Tahunan")
        if "jenis_kekerasan" in df_std.columns:
            tabs_to_show.append("⚡ Jenis Kekerasan")
        if "pelaku" in df_std.columns:
            tabs_to_show.append("👤 Pelaku")
        if "universitas" in df_std.columns:
            tabs_to_show.append("🏛️ Universitas")
        if "provinsi" in df_std.columns:
            tabs_to_show.append("🗾 Provinsi")
        if "bulan" in df_std.columns and "tahun" in df_std.columns:
            tabs_to_show.append("📅 Bulanan")

        if not tabs_to_show:
            st.markdown("""
            <div class="alert-box warning">
                ⚠️ Tidak ada kolom standar yang terdeteksi untuk membuat visualisasi otomatis.
                Gunakan <strong>Atur Mapping Kolom Secara Manual</strong> di atas untuk menetapkan kolom secara manual.
            </div>
            """, unsafe_allow_html=True)
        else:
            if len(tabs_to_show) > 1:
                tabs = st.tabs(tabs_to_show)
            else:
                tabs = [st.container()]

            for i, tab_name in enumerate(tabs_to_show):
                with tabs[i]:
                    if "Tren" in tab_name and "tahun" in df_std.columns:
                        fig = chart_trend_tahunan(df_std)
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        if "tahun" in df_std.columns:
                            from components.storytelling import story_trend
                            render_story_box("Narasi Tren", story_trend(df_std))

                    elif "Jenis" in tab_name:
                        fig = chart_jenis_kekerasan(df_std)
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        from components.storytelling import story_jenis_kekerasan
                        render_story_box("Narasi Jenis Kekerasan", story_jenis_kekerasan(df_std))

                    elif "Pelaku" in tab_name:
                        fig = chart_pelaku(df_std)
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        from components.storytelling import story_pelaku
                        render_story_box("Narasi Pelaku", story_pelaku(df_std))

                    elif "Universitas" in tab_name:
                        fig = chart_top_universitas(df_std)
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        from components.storytelling import story_universitas
                        render_story_box("Narasi Universitas", story_universitas(df_std))

                    elif "Provinsi" in tab_name:
                        fig = chart_provinsi_bar(df_std)
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        from components.storytelling import story_provinsi
                        render_story_box("Narasi Provinsi", story_provinsi(df_std))

                    elif "Bulanan" in tab_name:
                        fig = chart_bulanan_heatmap(df_std)
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ---- Download Raw Data ----
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("Unduh Data")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            csv_data = df_std.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="⬇️ Download Data (CSV)",
                data=csv_data.encode("utf-8-sig"),
                file_name="sigap_analisis.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_dl2:
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df_std.to_excel(writer, index=False, sheet_name="Data")
            st.download_button(
                label="⬇️ Download Data (Excel)",
                data=buffer.getvalue(),
                file_name="sigap_analisis.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    render_footer()

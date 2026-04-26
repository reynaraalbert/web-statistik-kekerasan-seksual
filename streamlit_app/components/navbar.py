"""
components/navbar.py
Custom navbar & shared UI components for SIGAP dashboard
"""
import streamlit as st
import os

def load_css():
    """Load custom CSS from assets/style.css"""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_navbar(active_page="Beranda"):
    """Render IDX-style top navbar"""
    pages = {
        "Beranda": "🏠",
        "Statistik": "📊",
        "Peta Sebaran": "🗺️",
        "Media & YouTube": "📱",
        "Analisis Mandiri": "📤",
    }
    active_class = lambda p: "active" if p == active_page else ""
    links_html = "".join([
        f'<span class="sigap-nav-link {active_class(p)}">{icon} {p}</span>'
        for p, icon in pages.items()
    ])
    st.markdown(f"""
    <div class="sigap-navbar">
        <div class="sigap-logo">
            <div class="sigap-logo-mark">S</div>
            <div class="sigap-logo-text">
                <div class="sigap-logo-name">SIGAP</div>
                <div class="sigap-logo-tagline">Sistem Informasi Kekerasan Seksual di PT</div>
            </div>
        </div>
        <div class="sigap-nav-links">
            {links_html}
        </div>
        <div>
            <span class="sigap-badge">Live Data 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = ""):
    """Render a styled section header with red bar"""
    sub_html = f'<span class="section-header-sub">{subtitle}</span>' if subtitle else ""
    st.markdown(f"""
    <div class="section-header">
        <div class="section-header-bar"></div>
        <span class="section-header-title">{title}</span>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_story_box(title: str, content: str):
    """Render a storytelling narration box"""
    st.markdown(f"""
    <div class="story-box">
        <div class="story-box-title">📖 {title}</div>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def render_stat_card(value, label: str, desc: str = "", color: str = "var(--primary)"):
    """Render a single stat card"""
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: {color};">
        <div class="stat-card-value" style="color: {color};">{value}</div>
        <div class="stat-card-label">{label}</div>
        <div class="stat-card-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def render_hero(total_kasus, total_kampus, total_provinsi, tahun_range):
    """Render the main hero section"""
    st.markdown(f"""
    <div class="sigap-hero">
        <div class="sigap-hero-eyebrow">🔴 Laporan Eksklusif · Data Terverifikasi</div>
        <h1>Krisis Tersembunyi di Perguruan Tinggi Indonesia</h1>
        <p class="sigap-hero-sub">
            Data komprehensif kekerasan seksual di kampus yang dikumpulkan melalui
            scraping media nasional, YouTube, dan laporan resmi. Visualisasi interaktif
            berbasis pendekatan <strong>storytelling with data</strong> untuk mendorong
            transparansi dan kebijakan yang lebih baik.
        </p>
        <div class="sigap-hero-stats">
            <div class="sigap-hero-stat">
                <div class="sigap-hero-stat-num">{total_kasus:,}</div>
                <div class="sigap-hero-stat-label">Total Laporan</div>
            </div>
            <div class="sigap-hero-stat">
                <div class="sigap-hero-stat-num">{total_kampus}</div>
                <div class="sigap-hero-stat-label">Kampus Terdampak</div>
            </div>
            <div class="sigap-hero-stat">
                <div class="sigap-hero-stat-num">{total_provinsi}</div>
                <div class="sigap-hero-stat-label">Provinsi</div>
            </div>
            <div class="sigap-hero-stat">
                <div class="sigap-hero-stat-num">{tahun_range}</div>
                <div class="sigap-hero-stat-label">Rentang Tahun</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render page footer"""
    st.markdown("""
    <div class="sigap-footer">
        <strong>SIGAP</strong> — Sistem Informasi Kekerasan Seksual di Perguruan Tinggi Indonesia<br>
        Data dikumpulkan dari scraping media nasional, YouTube, dan sumber publik lainnya.<br>
        <small>Dibuat untuk keperluan riset akademik · Tidak untuk keperluan komersial</small>
    </div>
    """, unsafe_allow_html=True)


def render_ticker(headlines: list):
    """Render scrolling news ticker"""
    items = " &nbsp;|&nbsp; ".join(f"🔴 {h}" for h in headlines[:8])
    st.markdown(f"""
    <div class="ticker-wrapper">
        <span class="ticker-label">TERKINI</span>
        <span class="ticker-content">{items}</span>
    </div>
    """, unsafe_allow_html=True)

"""
SIBS: Shipyard Integrated Business System
Sistem Integrasi Bisnis & Operasional Galangan Kapal
Enterprise Multi-Theme Edition (Light & Dark Mode) — Powered by Supabase

Version: 4.2.0
Berdasarkan:
1. Skripsi Ratih Laratasari Pagayang (Unhas, 2025)
2. Sistem Informasi Galangan Kecil.xlsm (230+ sheet)
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime

# Import core configurations & utilities
from config import app_config, DEPARTMENTS, supabase_config, DEFAULT_USERS
from database import db_manager
from auth import auth_manager, hash_password
from utils import (
    apply_sibs_theme, render_kpi, render_page_header,
    status_pill, format_currency, format_percentage, format_date,
    show_success, show_error, show_warning, show_info,
    get_asset_base64
)

# Import 7 department modules
from departments import (
    perencanaan,
    produksi,
    pembelian,
    qaqc,
    gudang,
    fasilitas,
    eksekutif
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="SIBS — Sistem Integrasi Bisnis Galangan Kapal",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INITIALIZATION ====================
def init_session_state():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}
    if "nav_menu" not in st.session_state:
        st.session_state.nav_menu = "Dashboard Eksekutif"
    if "active_project" not in st.session_state:
        st.session_state.active_project = "NB-002"
    if "last_sync" not in st.session_state:
        st.session_state.last_sync = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

init_session_state()

# Apply selected theme (Light or Dark)
apply_sibs_theme(st.session_state.theme)


# ==================== LANDING PAGE ====================
def render_landing_page():
    """
    Halaman muka resmi SIBS dengan tata letak corporate maritim modern,
    merujuk pada referensi website galangan profesional (PT. SCM-INDONESIA).
    Dilengkapi floating navbar, gambar hero galangan kapal sunset, switch mode di kanan atas hero,
    dan tombol dinamis responsif berstandar industri.
    """
    is_dark = st.session_state.theme == "dark"

    # 1. Top Navbar Header (Mirroring Reference PT. SCM-INDONESIA)
    brand_sub_color = "#94A3B8" if is_dark else "#64748B"
    brand_title_color = "#FFFFFF" if is_dark else "#0F172A"
    
    st.markdown(f"""
        <div id="beranda"></div>
        <div class="sibs-navbar-container">
            <div class="sibs-brand-title">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <polygon points="12,2 22,8.5 22,15.5 12,22 2,15.5 2,8.5" stroke="#38BDF8" stroke-width="2.2" fill="rgba(56, 189, 248, 0.18)"/>
                    <line x1="12" y1="2" x2="12" y2="22" stroke="#38BDF8" stroke-width="1.8"/>
                    <line x1="12" y1="12" x2="22" y2="8.5" stroke="#38BDF8" stroke-width="1.8"/>
                    <line x1="12" y1="12" x2="2" y2="8.5" stroke="#38BDF8" stroke-width="1.8"/>
                </svg>
                <span style="color: {brand_title_color}; font-weight: 800; font-size: 19px; letter-spacing: 0.5px;">SIBS INDONESIA</span>
                <span class="sibs-brand-sub" style="color: {brand_sub_color};">SHIPYARD INTEGRATED BUSINESS SYSTEM</span>
            </div>
            <ul class="sibs-nav-links">
                <li><a href="#beranda" class="sibs-nav-link active">Beranda</a></li>
                <li><a href="#kpi-section" class="sibs-nav-link">Ringkasan KPI</a></li>
                <li><a href="#modul-departemen" class="sibs-nav-link">7 Departemen</a></li>
                <li><a href="#standar-bki" class="sibs-nav-link">Standar BKI</a></li>
                <li><a href="#kapal-riset" class="sibs-nav-link">Spesifikasi Ro-Ro</a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # 2. Hero Section with Background Image & Top-Right Switch Mode
    with st.container(key="sibs_hero_section"):
        # Top Row of Hero Section: Left Eyebrow & Right Switch Mode Button
        col_hero_tag, col_hero_switch = st.columns([7.2, 2.8])
        with col_hero_tag:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 10px; padding-top: 4px;">
                    <span class="sibs-hero-tag">SISTEM INTEGRASI BISNIS GALANGAN</span>
                    <span class="sibs-hero-badge">STANDAR BKI KELAS 750 GT</span>
                </div>
            """, unsafe_allow_html=True)
        with col_hero_switch:
            # Switch Mode toggle positioned exactly at the top right of the hero section
            if is_dark:
                if st.button("Mode: Terang", key="hero_switch_theme", use_container_width=True):
                    st.session_state.theme = "light"
                    st.rerun()
            else:
                if st.button("Mode: Gelap", key="hero_switch_theme", use_container_width=True):
                    st.session_state.theme = "dark"
                    st.rerun()

        # Hero Main Body (Left-Aligned, Large Display Title, High Legibility Paragraph)
        st.markdown("""
            <div style="margin: 16px 0 24px 0;">
                <div class="sibs-hero-sub-title">SISTEM INTEGRASI BISNIS & OPERASIONAL GALANGAN</div>
                <h1 class="sibs-hero-main-title">Shipyard Integrated Business System</h1>
                <p class="sibs-hero-paragraph">
                    Platform tata kelola terpadu pembangunan kapal baru berbasis Block Construction Method (PWBS) 
                    dan pemeliharaan armada maritim nasional. Mengintegrasikan sinkronisasi jadwal perakitan 7 departemen, 
                    pengendalian serapan anggaran konstruksi real-time, ketertelusuran rantai pasok material baja, 
                    serta pemenuhan 39 standar inspeksi klasifikasi BKI.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Responsive Dynamic Action Buttons (Matching Reference CTA Style)
        col_cta1, col_cta2, col_blank = st.columns([2.6, 2.6, 4.8])
        with col_cta1:
            if st.button("Masuk Portal SIBS", type="primary", key="hero_enter_portal", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
        with col_cta2:
            if st.button("Standar Mutu BKI (39)", key="hero_bki_guide", use_container_width=True):
                st.toast("Standar Klasifikasi BKI Volume II (Hull Construction) terdaftar: 39 kategori inspeksi aktif.")

        # Cockpit Real-time Stats Footer Strip
        st.markdown("""
            <div class="sibs-hero-footer-bar">
                <div class="sibs-footer-stat-item">
                    <span class="stat-label">PROJECT AKTIF</span>
                    <span class="stat-value">KM. Nusantara (Ro-Ro 750 GT)</span>
                </div>
                <div class="sibs-footer-stat-item">
                    <span class="stat-label">METODE KONSTRUKSI</span>
                    <span class="stat-value">PWBS 7 Tahap (HS-04 & HS-06)</span>
                </div>
                <div class="sibs-footer-stat-item">
                    <span class="stat-label">PROGRESS FISIK</span>
                    <span class="stat-value" style="color: #34D399;">55.70% (Tepat Waktu)</span>
                </div>
                <div class="sibs-footer-stat-item">
                    <span class="stat-label">BASIS DATA CLOUD</span>
                    <span class="stat-value" style="color: #60A5FA;">Supabase PostgreSQL Live</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 3. 4 Executive Glass KPI Cards
    st.markdown('<div id="kpi-section" style="margin-top: 10px;"></div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi("INTEGRASI UNIT KERJA", "7 Departemen", "Sinkronisasi Real-Time PWBS", "#38BDF8")
    with k2:
        render_kpi("STANDAR MUTU BKI", "39 Kategori", "Rules Vol. II Hull Construction", "#34D399")
    with k3:
        render_kpi("PEMANTAUAN ANGGARAN", "Terkontrol", "Material, Upah & Utilisasi Alat", "#38BDF8")
    with k4:
        render_kpi("LEGALITAS BERKAS", "Cetak BAP", "Berita Acara Digital Siap Cetak", "#34D399")

    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

    # 4. Modul 7 Departemen Terintegrasi (Interactive Glassmorphic Grid)
    st.markdown('<div id="modul-departemen"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 16px;">
            <div>
                <span class="status-pill-navy" style="margin-bottom: 6px;">ARSITEKTUR ERP MARITIM</span>
                <h3 style="margin: 4px 0 0 0; font-size: 22px; font-weight: 800;">Modul 7 Departemen Terintegrasi</h3>
            </div>
            <span style="font-size: 11.5px; opacity: 0.75; font-weight: 600;">STANDAR PWBS & BKI KELAS 750 GT</span>
        </div>
    """, unsafe_allow_html=True)

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:10px; font-weight:800; color:#38BDF8; background:rgba(56, 189, 248, 0.15); padding:3px 8px; border-radius:999px; border:1px solid rgba(56, 189, 248, 0.35);">MODUL 01</span>
                <span style="font-size:10px; font-weight:700; color:#94A3B8;">PWBS LV. 1-4</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:#FFFFFF; font-size:15px; font-weight:700;">Perencanaan & Desain</h4>
            <p style="font-size:12px; margin:0 0 12px 0; opacity:0.85; line-height:1.6;">Dimensi utama kapal, manajemen blok lambung (HS-04/06), dan hirarki PWBS level 1-4.</p>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:8px; font-size:10.5px; color:#38BDF8; font-weight:600;">Lines Plan • Hydrostatic • Blok</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:10px; font-weight:800; color:#38BDF8; background:rgba(56, 189, 248, 0.15); padding:3px 8px; border-radius:999px; border:1px solid rgba(56, 189, 248, 0.35);">MODUL 02</span>
                <span style="font-size:10px; font-weight:700; color:#94A3B8;">FABRIKASI & ERECTION</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:#FFFFFF; font-size:15px; font-weight:700;">Produksi Lapangan</h4>
            <p style="font-size:12px; margin:0 0 12px 0; opacity:0.85; line-height:1.6;">Jadwal perakitan 7 tahap, monitoring pemotongan/pengelasan, dan requisition material.</p>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:8px; font-size:10.5px; color:#38BDF8; font-weight:600;">Jadwal 7 Tahap • SPK • Progres</div>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:10px; font-weight:800; color:#38BDF8; background:rgba(56, 189, 248, 0.15); padding:3px 8px; border-radius:999px; border:1px solid rgba(56, 189, 248, 0.35);">MODUL 03</span>
                <span style="font-size:10px; font-weight:700; color:#94A3B8;">SUPPLY CHAIN ERP</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:#FFFFFF; font-size:15px; font-weight:700;">Pembelian & Logistik</h4>
            <p style="font-size:12px; margin:0 0 12px 0; opacity:0.85; line-height:1.6;">Master database supplier maritim, penerbitan Purchase Order resmi, dan pelacakan DO.</p>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:8px; font-size:10.5px; color:#38BDF8; font-weight:600;">Vendor BKI • PO • Delivery Order</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:10px; font-weight:800; color:#34D399; background:rgba(16, 185, 129, 0.15); padding:3px 8px; border-radius:999px; border:1px solid rgba(52, 211, 153, 0.35);">MODUL 04</span>
                <span style="font-size:10px; font-weight:700; color:#34D399;">39 KATEGORI BKI</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:#FFFFFF; font-size:15px; font-weight:700;">Kontrol Mutu (QA/QC)</h4>
            <p style="font-size:12px; margin:0 0 12px 0; opacity:0.85; line-height:1.6;">Verifikasi pengujian NDT las (UT/RT), checklist 39 kategori BKI, approval, dan remedial defect.</p>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:8px; font-size:10.5px; color:#34D399; font-weight:600;">Inspeksi BKI • NDT Las • Remedial</div>
        </div>
        """, unsafe_allow_html=True)

    with d3:
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:10px; font-weight:800; color:#38BDF8; background:rgba(56, 189, 248, 0.15); padding:3px 8px; border-radius:999px; border:1px solid rgba(56, 189, 248, 0.35);">MODUL 05</span>
                <span style="font-size:10px; font-weight:700; color:#94A3B8;">INVENTORY & STOCK</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:#FFFFFF; font-size:15px; font-weight:700;">Material & Gudang</h4>
            <p style="font-size:12px; margin:0 0 12px 0; opacity:0.85; line-height:1.6;">Stok pelat Grade A, profil baja, kawat las E7018, mutasi barang keluar/masuk, dan alert minimum.</p>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:8px; font-size:10.5px; color:#38BDF8; font-weight:600;">Pelat Baja • Consumable • Mutasi</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:10px; font-weight:800; color:#38BDF8; background:rgba(56, 189, 248, 0.15); padding:3px 8px; border-radius:999px; border:1px solid rgba(56, 189, 248, 0.35);">MODUL 06</span>
                <span style="font-size:10px; font-weight:700; color:#94A3B8;">ASSET & HEAVY DOCK</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:#FFFFFF; font-size:15px; font-weight:700;">Manajemen Fasilitas</h4>
            <p style="font-size:12px; margin:0 0 12px 0; opacity:0.85; line-height:1.6;">Gantry crane 50T, CNC plasma, graving dock, jadwal preventive maintenance, dan tarif sewa.</p>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:8px; font-size:10.5px; color:#38BDF8; font-weight:600;">Drydock • Crane • Maintenance</div>
        </div>
        """, unsafe_allow_html=True)

    with d4:
        st.markdown("""
        <div class="sibs-card" style="border-top-color:#34D399 !important; border-left-color:rgba(52, 211, 153, 0.4) !important;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:10px; font-weight:800; color:#34D399; background:rgba(16, 185, 129, 0.15); padding:3px 8px; border-radius:999px; border:1px solid rgba(52, 211, 153, 0.35);">MODUL 07</span>
                <span style="font-size:10px; font-weight:700; color:#34D399;">EXECUTIVE DASHBOARD</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:#34D399; font-size:15px; font-weight:700;">Eksekutif & BAP</h4>
            <p style="font-size:12px; margin:0 0 12px 0; opacity:0.85; line-height:1.6;">Kurva S kumulatif fisik, serapan anggaran konstruksi riil, dan cetak Berita Acara Pemeriksaan (BAP) standar A4.</p>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:8px; font-size:10.5px; color:#34D399; font-weight:600;">Kurva S • Rekap Biaya • Cetak BAP</div>
        </div>
        """, unsafe_allow_html=True)

    # 5. Spesifikasi Kapal Riset & Standar Mutu BKI (Glass Tables)
    st.markdown('<div id="standar-bki"></div><div id="kapal-riset"></div>', unsafe_allow_html=True)
    col_ship_spec, col_bki_spec = st.columns([1, 1])
    with col_ship_spec:
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <h4 style="margin:0; font-size:15px; font-weight:700; color:#FFFFFF;">Proyek Aktif: KM. Nusantara (Ferry Ro-Ro 750 GT)</h4>
                <span class="status-pill-navy">DATA TEKNIS</span>
            </div>
            <table style="width:100%; font-size:12.5px; border-collapse:collapse; opacity:0.92;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Panjang Keseluruhan (LOA)</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">56.02 m</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Panjang Antara Garis Tegak (LBP)</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">49.80 m</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Lebar Moulded (B)</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">14.00 m</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Tinggi Moulded (H)</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">4.10 m</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Sarat Air Rancang (T)</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">2.70 m</td></tr>
                <tr><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Kecepatan Dinas (Vs)</td><td style="text-align:right; font-weight:700; color:#38BDF8;">11.00 knot</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with col_bki_spec:
        st.markdown("""
        <div class="sibs-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <h4 style="margin:0; font-size:15px; font-weight:700; color:#FFFFFF;">Verifikasi Standar Mutu Biro Klasifikasi Indonesia</h4>
                <span class="status-pill-green">BKI COMPLIANT</span>
            </div>
            <table style="width:100%; font-size:12.5px; border-collapse:collapse; opacity:0.92;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Regulasi Acuan</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">BKI Vol. II (Hull Construction)</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Kategori Inspeksi</td><td style="text-align:right; font-weight:700; color:#34D399;">39 Kategori Pengujian Aktif</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Metode NDT Pengelasan</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">UT (Ultrasonic) & RT (Radiographic)</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Sertifikasi Material</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">Marine Grade Steel Mill Certificate</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);"><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Output Dokumen Legal</td><td style="text-align:right; font-weight:700; color:#FFFFFF;">Berita Acara Pemeriksaan (BAP) Fisik</td></tr>
                <tr><td style="padding:6px 0; font-weight:600; color:#94A3B8;">Audit Trail</td><td style="text-align:right; font-weight:700; color:#38BDF8;">Digital Timestamp & Inspector Sign</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # 6. Floating Support Widget (Matching Reference Glass Capsule)
    st.markdown("""
        <a href="#beranda" class="sibs-floating-support">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12C2 13.85 2.5 15.58 3.37 17.07L2 22L7.07 20.67C8.54 21.52 10.21 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM16.5 15.5C16.3 16 15.1 16.6 14.6 16.7C14.1 16.8 13.5 16.8 12.9 16.6C11.8 16.2 10.7 15.5 9.7 14.5C8.7 13.5 8 12.4 7.6 11.3C7.4 10.7 7.4 10.1 7.5 9.6C7.6 9.1 8.2 7.9 8.7 7.7C8.9 7.6 9.1 7.6 9.3 7.6C9.5 7.6 9.7 7.6 9.8 8C10.1 8.7 10.6 9.9 10.7 10.1C10.8 10.3 10.8 10.5 10.7 10.7C10.6 10.9 10.5 11 10.4 11.1C10.3 11.2 10.2 11.3 10.1 11.4C10 11.5 9.9 11.6 10 11.8C10.2 12.2 10.6 12.9 11.2 13.5C11.8 14.1 12.5 14.5 12.9 14.7C13.1 14.8 13.2 14.7 13.3 14.6C13.4 14.5 13.5 14.4 13.6 14.3C13.7 14.2 13.8 14.1 14 14.2C14.2 14.3 15.4 14.8 15.7 15C16 15.2 16.1 15.3 16.1 15.4C16.2 15.4 16.7 15 16.5 15.5Z"/>
            </svg>
            <span>Pusat Bantuan SIBS</span>
        </a>
    """, unsafe_allow_html=True)

    # 7. Corporate Footer
    st.markdown("<hr style='margin:30px 0 16px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; font-size: 11.5px; opacity:0.75; padding-bottom: 24px;">
            SIBS Versi {app_config.VERSION} | Sistem Integrasi Bisnis Galangan Kapal — Berdasarkan Riset Unhas & Galangan Kapal Nasional<br>
            Didukung oleh Supabase PostgreSQL. Seluruh aktivitas transaksi operasional tercatat pada audit trail resmi.
        </div>
    """, unsafe_allow_html=True)


# ==================== LOGIN PAGE ====================
def render_login_page():
    """Halaman login formal SIBS dengan switch mode di kanan atas."""
    is_dark = st.session_state.theme == "dark"
    col_back, col_spacer, col_theme = st.columns([2, 5, 1.8])
    with col_back:
        if st.button("Kembali ke Halaman Utama", use_container_width=True):
            st.session_state.show_login = False
            st.rerun()
    with col_theme:
        if is_dark:
            if st.button("Mode: Terang", key="login_theme_btn", use_container_width=True):
                st.session_state.theme = "light"
                st.rerun()
        else:
            if st.button("Mode: Gelap", key="login_theme_btn", use_container_width=True):
                st.session_state.theme = "dark"
                st.rerun()

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="sibs-card">
                <span class="status-pill-navy">PORTAL OTENTIKASI RESMI</span>
                <h3 style="margin:8px 0 4px 0; font-size:20px; font-weight:800;">Masuk ke Portal SIBS</h3>
                <p style="font-size:12px; opacity:0.8; margin-bottom:16px;">
                    Gunakan kredensial akun departemen Anda untuk mengakses sistem.
                </p>
            </div>
        """, unsafe_allow_html=True)

        if not db_manager.is_connected:
            st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

        with st.form("form_login"):
            username = st.text_input("Username Departemen / NIP *", placeholder="Contoh: admin, produksi, qaqc")
            password = st.text_input("Kata Sandi *", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("Masuk ke Sistem", use_container_width=True)

            if submit_login:
                ok, user_info, msg = auth_manager.authenticate_user(username.strip(), password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.user_info = user_info
                    st.session_state.show_login = False
                    st.session_state.last_sync = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    
                    role = user_info.get("role", "")
                    role_map = {
                        "perencanaan": "Desain & Perencanaan",
                        "produksi": "Produksi Lapangan",
                        "pembelian": "Pembelian & Logistik",
                        "qaqc": "Quality Control (QA/QC)",
                        "gudang": "Material & Gudang",
                        "fasilitas": "Manajemen Fasilitas",
                        "eksekutif": "Manajemen Eksekutif & BAP",
                        "admin": "Dashboard Eksekutif"
                    }
                    st.session_state.nav_menu = role_map.get(role, "Dashboard Eksekutif")
                    show_success(f"Selamat datang, {user_info.get('nama_lengkap')}!")
                    st.rerun()
                else:
                    show_error(msg)

        with st.expander("Daftar Akun Departemen Bawaan (Default)"):
            st.markdown("""
            | Role | Username | Password | Departemen |
            | :--- | :--- | :--- | :--- |
            | Administrator | `admin` | `admin123` | Akses Penuh / IT |
            | Perencanaan | `perencanaan` | `super123` | Desain & PWBS |
            | Produksi | `produksi` | `super123` | Operasional Lapangan |
            | Pembelian | `pembelian` | `super123` | Pengadaan & PO |
            | QA / QC | `qaqc` | `super123` | Mutu & Inspeksi |
            | Gudang | `gudang` | `super123` | Inventaris & Mutasi |
            | Fasilitas | `fasilitas` | `super123` | Alat & Maintenance |
            | Eksekutif | `eksekutif` | `super123` | Pimpinan Galangan |
            """)


# ==================== ADMIN VIEW ====================
def render_admin_view(user_info: dict):
    """Halaman Pengaturan Administrator & Audit Log."""
    render_page_header(
        title="Pengaturan Sistem & Audit Log",
        subtitle="Manajemen Pengguna, Hak Akses Departemen, dan Pemantauan Jejak Audit",
        badge="ADMINISTRATOR"
    )

    tab_users, tab_new_user, tab_audit = st.tabs([
        "Daftar Pengguna Sistem",
        "Tambah Pengguna Baru",
        "Log Audit Aktivitas"
    ])

    with tab_users:
        st.markdown("### Daftar Pengguna Terdaftar")
        users = db_manager.get_all_users()
        if users:
            st.dataframe(pd.DataFrame(users), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pengguna yang terbaca dari database.")

    with tab_new_user:
        st.markdown("### Pendaftaran Pengguna Baru")
        with st.form("form_add_user"):
            c1, c2 = st.columns(2)
            with c1:
                u_name = st.text_input("Username *")
                u_fullname = st.text_input("Nama Lengkap *")
                u_pw = st.text_input("Password Awal *", type="password")
            with c2:
                u_role = st.selectbox("Role / Hak Akses *", list(DEPARTMENTS.keys()))
                u_dept = st.text_input("Nama Divisi / Bagian", value="Galangan Kapal")

            submit_u = st.form_submit_button("Daftarkan Pengguna")
            if submit_u:
                if not u_name or not u_pw or not u_fullname:
                    show_error("Username, Nama Lengkap, dan Password wajib diisi.")
                else:
                    new_user = {
                        "username": u_name.strip(),
                        "password_hash": hash_password(u_pw),
                        "nama_lengkap": u_fullname.strip(),
                        "role": u_role,
                        "departemen": u_dept.strip(),
                        "is_active": True
                    }
                    ok = db_manager.create_user(new_user)
                    if ok:
                        db_manager.log_action(user_info.get("username", "admin"), "CREATE_USER", "users", u_name, keterangan=f"Pendaftaran user {u_name}")
                        show_success(f"Pengguna '{u_name}' berhasil didaftarkan!")
                        st.rerun()
                    else:
                        show_error("Gagal mendaftarkan pengguna (mungkin username sudah digunakan).")

    with tab_audit:
        st.markdown("### Jejak Audit Sistem (Audit Trail)")
        st.caption("Seluruh aktivitas transaksi, modifikasi data, dan otentikasi tercatat secara permanen.")
        logs = db_manager.get_audit_logs(limit=150)
        if logs:
            st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada catatan log audit.")


# ==================== MAIN APPLICATION ROUTER ====================
def main():
    if not st.session_state.logged_in:
        if st.session_state.show_login:
            render_login_page()
        else:
            render_landing_page()
        return

    # User is logged in — render App Layout
    user = st.session_state.user_info
    role = user.get("role", "viewer")

    # ------------------ SIDEBAR ------------------
    with st.sidebar:
        # Brand Header
        brand_color = "#3B82F6" if st.session_state.theme == "dark" else "#1E3A8A"
        st.markdown(f"""
            <div style="padding: 10px 0 14px 0; border-bottom: 1px solid rgba(148, 163, 184, 0.2); margin-bottom: 14px;">
                <div style="font-size: 20px; font-weight: 800; color: {brand_color}; letter-spacing: 0.5px;">SIBS</div>
                <div style="font-size: 10.5px; font-weight: 600; opacity: 0.7;">SHIPYARD INTEGRATED BUSINESS SYSTEM</div>
            </div>
        """, unsafe_allow_html=True)

        # Theme Switcher (Dark / Light Mode)
        col_t1, col_t2 = st.columns([1.1, 1.2])
        with col_t1:
            st.markdown("<div style='padding-top:5px; font-size:12px; font-weight:600;'>Mode Tema:</div>", unsafe_allow_html=True)
        with col_t2:
            current_theme_idx = 0 if st.session_state.theme == "light" else 1
            theme_choice = st.radio("ThemeToggle", ["Terang", "Gelap"], index=current_theme_idx, horizontal=True, label_visibility="collapsed")
            new_theme = "light" if theme_choice == "Terang" else "dark"
            if new_theme != st.session_state.theme:
                st.session_state.theme = new_theme
                st.rerun()

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # User Profile Card
        st.markdown(f"""
            <div style="border: 1px solid rgba(148, 163, 184, 0.25); border-radius: 6px; padding: 10px 12px; margin-bottom: 14px;">
                <div style="font-size: 13px; font-weight: 700;">{user.get('nama_lengkap', 'User')}</div>
                <div style="font-size: 11px; color: #3B82F6; font-weight: 600; margin-top: 1px;">{user.get('department_display', role.upper())}</div>
                <div style="font-size: 10px; opacity:0.65; margin-top: 3px;">User: @{user.get('username')}</div>
            </div>
        """, unsafe_allow_html=True)

        # Database connection indicator
        if db_manager.is_connected:
            st.markdown('<span class="status-pill-green">ONLINE: SUPABASE</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill-red">OFFLINE: DATABASE</span>', unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Active Project Selector
        all_ships = db_manager.get_all_kapal()
        if all_ships:
            ship_options = {f"{s['id_project']} — {s.get('nama_kapal', '')}": s["id_project"] for s in all_ships}
            current_idx = 0
            keys_list = list(ship_options.keys())
            for idx, k in enumerate(keys_list):
                if ship_options[k] == st.session_state.active_project:
                    current_idx = idx
                    break
            sel_ship_label = st.selectbox("Proyek Kapal Aktif:", keys_list, index=current_idx)
            st.session_state.active_project = ship_options[sel_ship_label]
        else:
            st.session_state.active_project = "NB-002"
            st.caption(f"Proyek Aktif: **{st.session_state.active_project}** (Default)")

        st.markdown("<hr style='margin: 12px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)

        # Navigation Menu
        nav_options = [
            "Dashboard Eksekutif",
            "Desain & Perencanaan",
            "Produksi Lapangan",
            "Pembelian & Logistik",
            "Quality Control (QA/QC)",
            "Material & Gudang",
            "Manajemen Fasilitas",
            "Manajemen Eksekutif & BAP"
        ]
        if role == "admin":
            nav_options.append("Pengaturan & Audit Log")

        selected_page = st.radio("Navigasi Departemen:", nav_options, index=nav_options.index(st.session_state.nav_menu) if st.session_state.nav_menu in nav_options else 0)
        st.session_state.nav_menu = selected_page

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Logout Button
        if st.button("Keluar Sistem", use_container_width=True):
            db_manager.log_action(user.get("username", "user"), "LOGOUT", keterangan="Logout dari sistem")
            st.session_state.logged_in = False
            st.session_state.user_info = {}
            st.session_state.show_login = False
            st.rerun()

    # ------------------ MAIN ROUTER ------------------
    active_proj = st.session_state.active_project

    dept_key_map = {
        "Desain & Perencanaan": "perencanaan",
        "Produksi Lapangan": "produksi",
        "Pembelian & Logistik": "pembelian",
        "Quality Control (QA/QC)": "qaqc",
        "Material & Gudang": "gudang",
        "Manajemen Fasilitas": "fasilitas",
        "Manajemen Eksekutif & BAP": "eksekutif"
    }

    req_dept = dept_key_map.get(selected_page)
    if req_dept and not auth_manager.can_access_department(user, req_dept):
        st.warning(f"[AKSES TERBATAS] Anda login sebagai {user.get('department_display')}. Departemen ini hanya dapat diakses oleh personil terkait atau Administrator.")

    if selected_page in ["Dashboard Eksekutif", "Manajemen Eksekutif & BAP"]:
        eksekutif.render(user, active_proj)
    elif selected_page == "Desain & Perencanaan":
        perencanaan.render(user, active_proj)
    elif selected_page == "Produksi Lapangan":
        produksi.render(user, active_proj)
    elif selected_page == "Pembelian & Logistik":
        pembelian.render(user, active_proj)
    elif selected_page == "Quality Control (QA/QC)":
        qaqc.render(user, active_proj)
    elif selected_page == "Material & Gudang":
        gudang.render(user, active_proj)
    elif selected_page == "Manajemen Fasilitas":
        fasilitas.render(user, active_proj)
    elif selected_page == "Pengaturan & Audit Log" and role == "admin":
        render_admin_view(user)
    else:
        eksekutif.render(user, active_proj)


if __name__ == "__main__":
    main()

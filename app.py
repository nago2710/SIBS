"""
NAV-MIS: Sistem Integrasi Manajemen Galangan Kapal (Shipyard Management System)
Modern and fully structured version with modular architecture

Version: 2.0.0
Last Updated: 2026
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime

# Import modules
from config import app_config, ui_config, DEPARTMENTS
from database import db_manager
from auth import auth_manager
from utils import (
    apply_custom_styling, render_sidebar_header, render_user_info,
    render_login_header, render_dashboard_header, render_premium_card,
    show_success_toast, show_error_toast, show_warning_toast, show_info_toast,
    format_currency, create_metric_card
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title=app_config.APP_TITLE,
    page_icon=app_config.APP_ICON,
    layout=app_config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Initialize database
db_manager.initialize_database()

# ==================== SESSION STATE MANAGEMENT ====================

def init_session_state():
    """Initialize all session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
    if 'last_action' not in st.session_state:
        st.session_state.last_action = None


init_session_state()

# ==================== AUTHENTICATION PAGE ====================

def render_login_page():
    """Render login/authentication page"""
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Login header
        render_login_header()
        
        # Login form container
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### Autentikasi Akses Sistem")
            
            username = st.text_input(
                "📧 Username",
                placeholder="Masukkan username Anda",
                help="Default: ahmad.fauzi"
            )
            
            password = st.text_input(
                "🔐 Password",
                type="password",
                placeholder="Masukkan password Anda",
                help="Default: admin123"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    show_error_toast("Username dan password tidak boleh kosong")
                else:
                    success, user_info, message = auth_manager.authenticate_user(username, password)
                    
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_info = user_info
                        show_success_toast(f"Selamat datang {username}!")
                        logger.info(f"User {username} logged in successfully")
                        st.rerun()
                    else:
                        show_error_toast(message)
                        logger.warning(f"Login failed for user {username}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer info
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='text-align: center; color: #64748b; font-size: 12px;'>
                <p>NAV-MIS v{app_config.VERSION} | Galangan Kapal Terintegrasi</p>
                <p>© 2026 PT Krakatau Steel Shipyard Division</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================== SIDEBAR NAVIGATION ====================

def render_sidebar():
    """Render sidebar with navigation and user info"""
    with st.sidebar:
        # Sidebar header
        render_sidebar_header("NAV-MIS", f"v{app_config.VERSION}")
        
        # User info
        user_info = st.session_state.user_info
        render_user_info(
            user_info['username'],
            user_info['department_display'],
            user_info['department']
        )
        
        st.markdown("---")
        
        # Navigation menu
        st.markdown(
            "<p style='color: #475569; font-size: 11px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;'>📋 Menu Utama</p>",
            unsafe_allow_html=True
        )
        
        nav_page = st.radio(
            "Navigasi",
            ["Dashboard Terpusat", "Manajemen Data", "Laporan & Analisis", "Pengaturan Sistem"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Keluar (Sign Out)", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user_info = {}
            logger.info(f"User {user_info['username']} logged out")
            st.rerun()
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # Footer info
        st.markdown(
            f"""
            <div style='text-align: center; color: #64748b; font-size: 11px; border-top: 1px solid {ui_config.BORDER_COLOR}; padding-top: 12px;'>
                <p style='margin: 0;'>Last Login: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return nav_page
    
# ==================== DASHBOARD PAGE ====================

def render_dashboard():
    """Render main dashboard page"""
    render_dashboard_header(
        "📊 Dashboard Admin Sistem",
        "Konsolidasi data operasional galangan, regulasi kelas lambung, dan penelusuran aset alat berat"
    )
    
    # Get all project data
    db = db_manager.get_all_project_data()
    
    if not db:
        show_error_toast("Gagal memuat data dari database")
        return
    
    # ==================== KEY METRICS ====================
    anggaran = int(db.get("Anggaran Alokasi Proyek", 0))
    terpakai = int(db.get("Biaya Konstruksi Terpakai", 0))
    sisa_dana = anggaran - terpakai
    
    # Calculate metrics percentage
    utilization_pct = (terpakai / anggaran * 100) if anggaran > 0 else 0
    remaining_pct = ((sisa_dana / anggaran) * 100) if anggaran > 0 else 0
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="navistock-metric">
                <div class="navistock-label">💰 Total Alokasi Finansial</div>
                <div class="navistock-value">{format_currency(anggaran)}</div>
                <div class="navistock-subtext">Rencana Anggaran Biaya (RAB)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="navistock-metric">
                <div class="navistock-label">📊 Realisasi Dana Konstruksi</div>
                <div class="navistock-value" style="color: #f87171;">{format_currency(terpakai)}</div>
                <div class="navistock-subtext">Utilization: {utilization_pct:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="navistock-metric">
                <div class="navistock-label">✅ Sisa Cadangan Anggaran</div>
                <div class="navistock-value" style="color: #4ade80;">{format_currency(sisa_dana)}</div>
                <div class="navistock-subtext">Safety margin: {remaining_pct:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== PROJECT STATUS ====================
    st.markdown(render_premium_card("🏗️ Status Proyek Aktif"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Nama Proyek:** {db.get('Nama Proyek Aktif', 'N/A')}")
        st.markdown(f"**Jadwal Master:** {db.get('Master Schedule', 'N/A')}")
        st.markdown(f"**PWBS / Area Kerja:** {db.get('PWBS / Area Kerja', 'N/A')}")
    
    with col2:
        st.markdown(f"**Target Delivery:** {db.get('Target Waktu Peluncuran (Delivery)', 'N/A')}")
        st.markdown(f"**Vendor Utama:** {db.get('Vendor Utama Logistik', 'N/A')}")
        st.markdown(f"**Status QA/QC:** {db.get('Status Inspeksi QA/QC', 'N/A')}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== SEVEN DEPARTMENT TABS ====================
    st.markdown(render_premium_card("🏢 Stasiun Pengawasan Alur Informasi Departemen"), unsafe_allow_html=True)
    
    tabs = st.tabs([
        "📐 Desain & Perencanaan",
        "⚙️ Produksi Lapangan",
        "📦 Pembelian & Logistik",
        "✔️ QA / QC",
        "🏭 Gudang Material",
        "🔧 Manajemen Fasilitas",
        "📈 Eksekutif Pemantau"
    ])
    
    # ==================== TAB 1: PERENCANAAN ====================
    with tabs[0]:
        render_department_perencanaan(db)
    
    # ==================== TAB 2: PRODUKSI ====================
    with tabs[1]:
        render_department_produksi(db)
    
    # ==================== TAB 3: PEMBELIAN ====================
    with tabs[2]:
        render_department_pembelian(db)
    
    # ==================== TAB 4: QA/QC ====================
    with tabs[3]:
        render_department_qaqa(db)
    
    # ==================== TAB 5: GUDANG ====================
    with tabs[4]:
        render_department_gudang(db)
    
    # ==================== TAB 6: FASILITAS ====================
    with tabs[5]:
        render_department_fasilitas(db)
    
    # ==================== TAB 7: EKSEKUTIF ====================
    with tabs[6]:
        render_department_eksekutif(db)


# ==================== DEPARTMENT MODULES ====================

def render_department_perencanaan(db: dict):
    """Planning & Design Department"""
    st.markdown("### 📐 Departemen Perencanaan & Desain Produksi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_schedule = st.text_input(
            "Master Schedule Konstruksi Lambung",
            value=db.get("Master Schedule", ""),
            key="perencanaan_schedule"
        )
    
    with col2:
        new_pwbs = st.text_input(
            "Pembagian Blok Struktur (PWBS)",
            value=db.get("PWBS / Area Kerja", ""),
            key="perencanaan_pwbs"
        )
    
    if st.button("💾 Update Data Perencanaan", use_container_width=True, key="btn_update_perencanaan"):
        success1 = db_manager.update_single_data("Master Schedule", new_schedule, st.session_state.user_info['username'])
        success2 = db_manager.update_single_data("PWBS / Area Kerja", new_pwbs, st.session_state.user_info['username'])
        
        if success1 and success2:
            show_success_toast("Data perencanaan berhasil diperbarui")
            st.rerun()
        else:
            show_error_toast("Gagal memperbarui data perencanaan")


def render_department_produksi(db: dict):
    """Production Department"""
    st.markdown("### ⚙️ Departemen Produksi Lapangan")
    
    st.info(f"📋 **Referensi:** {db.get('Master Schedule', 'N/A')} | {db.get('PWBS / Area Kerja', 'N/A')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prog_val = st.slider(
            "Persentase Progres Perakitan Blok Lambung (%)",
            min_value=0, max_value=100, value=65, step=5,
            key="slider_progres_produksi"
        )
        st.progress(prog_val / 100)
    
    with col2:
        biaya_input = st.number_input(
            "Biaya Operasional Tambahan Lapangan (Rp)",
            min_value=0, step=5000000, value=0,
            key="input_biaya_produksi"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📤 Kirim Laporan Validasi Produksi", use_container_width=True, key="btn_produksi"):
        if biaya_input > 0:
            total_baru = int(db.get("Biaya Konstruksi Terpakai", 0)) + int(biaya_input)
            success = db_manager.update_single_data("Biaya Konstruksi Terpakai", str(total_baru), st.session_state.user_info['username'])
            
            if success:
                show_success_toast(f"Biaya tambahan {format_currency(biaya_input)} telah dicatat")
                st.rerun()
            else:
                show_error_toast("Gagal memperbarui biaya")
        else:
            show_warning_toast("Masukkan biaya tambahan yang valid")


def render_department_pembelian(db: dict):
    """Procurement Department"""
    st.markdown("### 📦 Departemen Pembelian & Logistik")
    
    with st.form("form_pembelian", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            v_name = st.text_input(
                "Mitra Pabrikan / Supplier",
                value=db.get("Vendor Utama Logistik", ""),
                placeholder="Masukkan nama vendor"
            )
        
        with col2:
            v_vol = st.number_input(
                "Volume Pengadaan Komponen (Ton)",
                min_value=0, step=10, value=50
            )
        
        v_target_date = st.date_input("Target Kedatangan Material")
        
        if st.form_submit_button("📋 Ajukan Nota Permintaan Pembelian", use_container_width=True):
            if v_name and v_vol > 0:
                success = db_manager.update_single_data("Vendor Utama Logistik", v_name, st.session_state.user_info['username'])
                if success:
                    show_warning_toast(f"✅ Permintaan diteruskan: {v_vol} Ton dari {v_name} | Target: {v_target_date}")
                    st.rerun()
            else:
                show_error_toast("Isi semua field dengan benar")


def render_department_qaqa(db: dict):
    """Quality Assurance Department"""
    st.markdown("### ✔️ Departemen QA / QC")
    
    st.info(f"📋 **Log Terakhir:** {db.get('Status Inspeksi QA/QC', 'N/A')}")
    
    status_options = [
        "Lolos Uji NDT Radiography Butt Joint Blok M1",
        "Sertifikasi Material Mill Certificate Pelat Baja Disetujui BKI",
        "Ditemukan Deformasi Pelat pada Area Blok Bow (Butuh Rework)",
        "Sertifikasi Lasan Blok Stern Disetujui Class Society"
    ]
    
    status_qa = st.selectbox(
        "Perbarui Kualifikasi Mutu Konstruksi",
        status_options,
        key="select_status_qa"
    )
    
    notes = st.text_area(
        "Catatan Inspeksi (Opsional)",
        placeholder="Masukkan detail inspeksi..."
    )
    
    if st.button("✅ Validasi Dokumen Mutu", use_container_width=True, key="btn_qaqa"):
        success = db_manager.update_single_data("Status Inspeksi QA/QC", status_qa, st.session_state.user_info['username'])
        if success:
            show_success_toast("Status inspeksi berhasil dipublikasikan")
            st.rerun()
        else:
            show_error_toast("Gagal memperbarui status")


def render_department_gudang(db: dict):
    """Warehouse Department"""
    st.markdown("### 🏭 Departemen Gudang Material")
    
    stok_current = int(db.get("Volume Stok Pelat Baja (Gudang)", 0))
    
    st.markdown(f"**Stok Saat Ini:** <span style='color: #38bdf8; font-size: 20px; font-weight: bold;'>{stok_current} Ton</span>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        tipe_mutasi = st.radio(
            "Aksi Mutasi Inventaris",
            [
                "Material Masuk (Lolos Inspeksi)",
                "Pengambilan untuk Bengkel Produksi"
            ],
            key="radio_gudang"
        )
    
    with col2:
        vol_mutasi = st.number_input(
            "Kuantitas Berat Material (Ton)",
            min_value=1, value=15, step=5,
            key="input_gudang"
        )
    
    if st.button("💾 Eksekusi Mutasi Gudang", use_container_width=True, key="btn_gudang"):
        if "Masuk" in tipe_mutasi:
            stok_akhir = stok_current + vol_mutasi
            action = "Penerimaan Material"
        else:
            if vol_mutasi > stok_current:
                show_error_toast(f"Stok tidak cukup. Tersedia: {stok_current} Ton")
                return
            stok_akhir = stok_current - vol_mutasi
            action = "Pengeluaran Material"
        
        success = db_manager.update_single_data("Volume Stok Pelat Baja (Gudang)", str(stok_akhir), st.session_state.user_info['username'])
        if success:
            show_success_toast(f"✅ {action}: {vol_mutasi} Ton | Stok Akhir: {stok_akhir} Ton")
            st.rerun()
        else:
            show_error_toast("Gagal mencatat mutasi")


def render_department_fasilitas(db: dict):
    """Facilities Management Department"""
    st.markdown("### 🔧 Departemen Manajemen Fasilitas")
    
    st.info(f"🏗️ **Status Infrastruktur:** {db.get('Kelayakan Fasilitas Gantry Crane', 'N/A')}")
    
    fasilitas_options = [
        "Operasional Normal - Sertifikasi Aktif",
        "Gantry Crane Jalur Rel Selatan dalam Kalibrasi Rutin",
        "Fasilitas Slipway Luncuran Kosong dan Siap",
        "Maintenance Crane Utama - Tidak Beroperasi"
    ]
    
    status_fasilitas = st.selectbox(
        "Perbarui Log Kondisi Fasilitas Mekanis",
        fasilitas_options,
        key="select_fasilitas"
    )
    
    maintenance_notes = st.text_area(
        "Catatan Pemeliharaan",
        placeholder="Masukkan catatan maintenance..."
    )
    
    if st.button("🔧 Update Log Fasilitas", use_container_width=True, key="btn_fasilitas"):
        success = db_manager.update_single_data("Kelayakan Fasilitas Gantry Crane", status_fasilitas, st.session_state.user_info['username'])
        if success:
            show_success_toast("Kondisi fasilitas berhasil diperbarui")
            st.rerun()
        else:
            show_error_toast("Gagal memperbarui fasilitas")


def render_department_eksekutif(db: dict):
    """Executive Dashboard"""
    st.markdown("### 📈 Dashboard Eksekutif Pemantau")
    
    st.markdown("**Status Konsolidasi Parameter Riil (SQLite Database)**")
    
    # Create dataframe for display
    df_data = pd.DataFrame(
        list(db.items()),
        columns=['Parameter Manufaktur Galangan', 'Status Valid Terkini']
    )
    
    st.dataframe(df_data, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2 = st.columns(2)
    
    with col1:
        anggaran = int(db.get("Anggaran Alokasi Proyek", 0))
        terpakai = int(db.get("Biaya Konstruksi Terpakai", 0))
        utilization = (terpakai / anggaran * 100) if anggaran > 0 else 0
        st.metric("💰 Budget Utilization", f"{utilization:.1f}%", f"{format_currency(terpakai)}")
    
    with col2:
        stok = int(db.get("Volume Stok Pelat Baja (Gudang)", 0))
        st.metric("📦 Inventory Status", f"{stok} Ton", "Material Baja")


# ==================== MANAJEMEN DATA PAGE ====================

def render_manajemen_data():
    """Data management page"""
    render_dashboard_header(
        "🗂️ Manajemen Data Sistem",
        "Kelola data pengguna, backup, dan konfigurasi database"
    )
    
    tabs = st.tabs(["👥 Manajemen Pengguna", "📊 Manajemen Data", "🔄 Backup & Restore"])
    
    with tabs[0]:
        render_user_management()
    
    with tabs[1]:
        render_data_management()
    
    with tabs[2]:
        render_backup_section()


def render_user_management():
    """User management section"""
    st.markdown(render_premium_card("👥 Daftar Pengguna Sistem"), unsafe_allow_html=True)
    
    users = db_manager.get_all_users()
    if users:
        df_users = pd.DataFrame(users)
        st.dataframe(df_users, use_container_width=True, hide_index=True)
    else:
        show_info_toast("Tidak ada data pengguna")


def render_data_management():
    """Data management section"""
    st.markdown(render_premium_card("📊 Manajemen Data Proyek"), unsafe_allow_html=True)
    
    db = db_manager.get_all_project_data()
    df = pd.DataFrame(list(db.items()), columns=['Parameter', 'Nilai'])
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("✏️ Edit Parameter Data"):
        selected_param = st.selectbox(
            "Pilih Parameter",
            list(db.keys()),
            key="select_edit_param"
        )
        
        new_value = st.text_input(
            "Nilai Baru",
            value=db[selected_param],
            key="input_edit_param"
        )
        
        if st.button("💾 Simpan Perubahan", key="btn_edit_param"):
            success = db_manager.update_single_data(selected_param, new_value, st.session_state.user_info['username'])
            if success:
                show_success_toast(f"Parameter '{selected_param}' berhasil diperbarui")
                st.rerun()
            else:
                show_error_toast("Gagal memperbarui parameter")


def render_backup_section():
    """Backup and restore section"""
    st.markdown(render_premium_card("🔄 Backup & Restore Database"), unsafe_allow_html=True)
    
    st.info("Fitur backup dan restore akan diimplementasikan di versi selanjutnya")
    
    if st.button("📥 Backup Database Sekarang", use_container_width=True):
        show_info_toast("Backup functionality coming soon...")


# ==================== LAPORAN PAGE ====================

def render_laporan():
    """Reports and analytics page"""
    render_dashboard_header(
        "📈 Laporan & Analisis",
        "Laporan komprehensif dan analisis data operasional"
    )
    
    tabs = st.tabs(["📊 Analisis Keuangan", "📦 Analisis Inventori", "📋 Audit Log"])
    
    with tabs[0]:
        budget_status = db_manager.get_budget_status()
        if budget_status:
            df_budget = pd.DataFrame(list(budget_status.items()), columns=['Parameter', 'Nilai'])
            st.dataframe(df_budget, use_container_width=True, hide_index=True)
        else:
            show_info_toast("Tidak ada data keuangan")
    
    with tabs[1]:
        inventory_status = db_manager.get_inventory_status()
        if inventory_status:
            df_inventory = pd.DataFrame(list(inventory_status.items()), columns=['Parameter', 'Nilai'])
            st.dataframe(df_inventory, use_container_width=True, hide_index=True)
        else:
            show_info_toast("Tidak ada data inventori")
    
    with tabs[2]:
        audit_logs = db_manager.get_audit_logs(limit=50)
        if audit_logs:
            df_audit = pd.DataFrame(audit_logs)
            st.dataframe(df_audit, use_container_width=True, hide_index=True)
        else:
            show_info_toast("Tidak ada audit log")


# ==================== PENGATURAN SISTEM PAGE ====================

def render_pengaturan():
    """System settings page"""
    render_dashboard_header(
        "⚙️ Pengaturan Sistem",
        "Konfigurasi dan pengaturan aplikasi"
    )
    
    tabs = st.tabs(["🔧 Konfigurasi Umum", "🔐 Keamanan", "📋 Tentang Sistem"])
    
    with tabs[0]:
        st.markdown(render_premium_card("🔧 Konfigurasi Aplikasi"), unsafe_allow_html=True)
        st.write(f"**Aplikasi:** {app_config.APP_TITLE}")
        st.write(f"**Versi:** {app_config.VERSION}")
        st.write(f"**Mode Debug:** {'✅ Enabled' if app_config.DEBUG else '❌ Disabled'}")
    
    with tabs[1]:
        st.markdown(render_premium_card("🔐 Pengaturan Keamanan"), unsafe_allow_html=True)
        st.write(f"**Min Password Length:** {security_config.PASSWORD_MIN_LENGTH} karakter")
        st.write(f"**Max Login Attempts:** {security_config.MAX_LOGIN_ATTEMPTS} percobaan")
        st.write(f"**Session Timeout:** {security_config.SESSION_TIMEOUT} detik")
    
    with tabs[2]:
        st.markdown(render_premium_card("📋 Tentang NAV-MIS"), unsafe_allow_html=True)
        st.markdown("""
        **NAV-MIS: Sistem Integrasi Manajemen Galangan Kapal**
        
        Sistem modern dan terstruktur untuk manajemen operasional galangan kapal dengan fitur:
        - ✅ Dashboard terpadu
        - ✅ Manajemen multi-departemen
        - ✅ Tracking budget dan inventori
        - ✅ Audit logging lengkap
        - ✅ Interface user-friendly
        
        © 2026 PT Krakatau Steel Shipyard Division
        """)


# ==================== IMPORT SECURITY CONFIG ====================
from config import security_config


# ==================== MAIN APPLICATION FLOW ====================

def main():
    """Main application flow"""
    
    # Show login page if not authenticated
    if not st.session_state.logged_in:
        render_login_page()
    else:
        # Render sidebar and get navigation choice
        page = render_sidebar()
        
        # Route to appropriate page
        if page == "Dashboard Terpusat":
            render_dashboard()
        elif page == "Manajemen Data":
            render_manajemen_data()
        elif page == "Laporan & Analisis":
            render_laporan()
        elif page == "Pengaturan Sistem":
            render_pengaturan()


# ==================== RUN APPLICATION ====================

if __name__ == "__main__":
    main()
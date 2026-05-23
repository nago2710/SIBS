import streamlit as st
import pandas as pd
import sqlite3

# --- 1. SET HALAMAN & CONFIG ---
st.set_page_config(page_title="NAV-MIS: Integrated Shipyard System", layout="wide", page_icon="⚓")

# --- 2. EXTREME CUSTOM CSS (TEMA PREMIUM DARK MODE & UI REFERENSI NAVISTOCK) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset total warna dasar ke Deep Navy Dark */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
    }
    
    /* Menghilangkan margin bawaan streamlit yang mengganggu layout */
    [data-testid="stSidebar"] {
        background-color: #0f1626 !important;
        border-right: 1px solid #1f293d !important;
    }
    
    /* Desain Banner Atas Dashboard */
    .dashboard-header {
        margin-bottom: 25px;
    }
    .dashboard-header h1 {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin-bottom: 4px;
    }
    .dashboard-header p {
        color: #94a3b8 !important;
        font-size: 14px;
    }
    
    /* Wadah Utama Konten / Grid Container Box */
    .premium-card {
        background: #111827;
        border: 1px solid #1f293d;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .card-title {
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 15px;
    }

    /* Kustomisasi Grid Metrik Eksklusif ala NaviStock */
    .navistock-grid {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
    }
    .navistock-metric {
        flex: 1;
        background: #111827;
        border: 1px solid #1f293d;
        border-radius: 10px;
        padding: 20px;
        position: relative;
    }
    .navistock-label {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    .navistock-value {
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
    }
    .navistock-subtext {
        font-size: 12px;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Desain Tombol Kustom Biru Terang */
    div.stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }

    /* Merombak Tampilan Tab Bawaan Menjadi Navigasi Menu Horizontal yang Bersih */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0f1626;
        padding: 6px;
        border-radius: 8px;
        border: 1px solid #1f293d;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 6px;
        color: #94a3b8;
        font-weight: 500;
        background-color: transparent;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }
    
    /* Memaksa Tabel Data Pandas Agar Sinkron dengan Tema Gelap */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: #111827 !important;
        border: 1px solid #1f293d !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION & RE-STRUCTURE (SESUAI DOKUMEN TA) ---
DB_FILE = "database_galangan.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT, departemen TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS proyek_data (indikator TEXT PRIMARY KEY, nilai TEXT)')
    
    # Cek ketersediaan data dummy dasar
    cursor.execute("SELECT COUNT(*) FROM proyek_data")
    if cursor.fetchone()[0] == 0:
        # Menyuplai data dummy komprehensif galangan sesuai isi bab III dokumen TA kamu
        data_awal = [
            ("Nama Proyek Aktif", "Hull No. 284 - General Cargo Vessel 5000 DWT"),
            ("Master Schedule", "Tahap Erection Blok & Instalasi Pipa Lambung"),
            ("PWBS / Area Kerja", "Blok Midship M1 s/d M4"),
            ("Anggaran Alokasi Proyek", "18500000000"),
            ("Biaya Konstruksi Terpakai", "9240000000"),
            ("Volume Stok Pelat Baja (Gudang)", "342"),
            ("Status Inspeksi QA/QC", "Lolos Uji NDT Radiography Butt Joint Blok M1"),
            ("Kelayakan Fasilitas Gantry Crane", "Operasional Normal - Sertifikasi Aktif"),
            ("Target Waktu Peluncuran (Delivery)", "14 November 2026"),
            ("Vendor Utama Logistik", "PT Krakatau Steel Tbk")
        ]
        cursor.executemany("INSERT INTO proyek_data VALUES (?, ?)", data_awal)
        
        # Pengguna default sistem korporasi
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", ("ahmad.fauzi", "admin123", "admin", "IT"))
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", ("budi.santoso", "super123", "supervisor", "Operations"))
    conn.commit()
    conn.close()

def ambil_semua_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM proyek_data", conn)
    conn.close()
    return dict(zip(df['indikator'], df['nilai']))

def update_data_tunggal(indikator, nilai_baru):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE proyek_data SET nilai = ? WHERE indikator = ?", (str(nilai_baru), indikator))
    conn.commit()
    conn.close()

def cek_login_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, departemen FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

init_db()

# Mengatur state sesi login pengguna
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}

# --- 4. TAMPILAN AUTH / PORTAL LOGIN PREMIUM ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; margin-bottom: 30px;'>
                <div style='background: #2563eb; width: 50px; height: 50px; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white;'>⚓</div>
                <h2 style='color: white; margin-top: 15px; font-size: 24px;'>Sistem Integrasi NAV-MIS</h2>
                <p style='color: #64748b; font-size: 13px;'>Portal Manajemen Galangan Kapal Terpadu</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        input_user = st.text_input("ID Pengguna / Username", value="ahmad.fauzi")
        input_pass = st.text_input("Kata Sandi / Password", type="password", value="admin123")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Autentikasi Akses"):
            user_data = cek_login_user(input_user, input_pass)
            if user_data:
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = {"username": input_user, "role": user_data[0], "dept": user_data[1]}
                st.rerun()
            else:
                st.error("Gagal melakukan verifikasi akun. Periksa kembali kredensial Anda.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. TAMPILAN DASHBOARD MANAGEMENT UTAMA ---
else:
    u_info = st.session_state['user_info']
    
    # Kustomisasi Ruang Lingkup Sidebar Kiri (Meniru Persis Layout Menu NaviStock)
    with st.sidebar:
        st.markdown(f"""
            <div style='padding: 10px 0px; margin-bottom: 20px; border-bottom: 1px solid #1f293d;'>
                <h4 style='color: white; margin: 0;'>⚓ NAV-MIS</h4>
                <p style='color: #64748b; font-size: 12px; margin: 0;'>Galangan Terintegrasi v1.0</p>
            </div>
            <div style='background: #111827; padding: 12px; border-radius: 8px; border: 1px solid #1f293d; margin-bottom: 25px;'>
                <div style='font-size: 11px; color: #64748b; text-transform: uppercase;'>User Aktif</div>
                <div style='font-weight: 600; color: white; font-size: 14px;'>{u_info['username']}</div>
                <div style='font-size: 12px; color: #38bdf8;'>Role: {u_info['role'].upper()} ({u_info['dept']})</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Menu Navigasi Samping Bertingkat
        st.markdown("<p style='color: #475569; font-size: 11px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;'>Menu Utama</p>", unsafe_allow_html=True)
        nav_selection = st.radio("Navigasi", ["Dashboard Terpusat", "Konfigurasi Sistem"], label_visibility="collapsed")
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("Keluar (Sign Out)"):
            st.session_state['logged_in'] = False
            st.session_state['user_info'] = {}
            st.rerun()

    # Pintu Masuk Konten Dashboard
    if nav_selection == "Dashboard Terpusat":
        st.markdown("""
            <div class="dashboard-header">
                <h1>Dashboard Admin Sistem</h1>
                <p>Konsolidasi data operasional galangan, regulasi kelas lambung, dan penelusuran aset alat berat.</p>
            </div>
        """, unsafe_allow_html=True)
        
        db = ambil_semua_data()
        
        # TIGA KOTAK METRIK UTAMA DENGAN DESAIN IDENTIK NAVISTOCK CARD
        anggaran = int(db["Anggaran Alokasi Proyek"])
        terpakai = int(db["Biaya Konstruksi Terpakai"])
        sisa_dana = anggaran - terpakai
        
        st.markdown(f"""
            <div class="navistock-grid">
                <div class="navistock-metric">
                    <div class="navistock-label">Total Alokasi Finansial Proyek</div>
                    <div class="navistock-value">Rp {anggaran:,}</div>
                    <div class="navistock-subtext" style="color: #64748b;">Sumber: Rencana Anggaran Biaya (RAB)</div>
                </div>
                <div class="navistock-metric">
                    <div class="navistock-label">Realisasi Dana Konstruksi Lapangan</div>
                    <div class="navistock-value" style="color: #f87171;">Rp {terpakai:,}</div>
                    <div class="navistock-subtext" style="color: #ef4444;">Beban pengerjaan aktual saat ini</div>
                </div>
                <div class="navistock-metric">
                    <div class="navistock-label">Sisa Cadangan Anggaran</div>
                    <div class="navistock-value" style="color: #4ade80;">Rp {sisa_dana:,}</div>
                    <div class="navistock-subtext" style="color: #10b981;">Safety margin keuangan proyek</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ALUR INTERKONEKSI DATA 7 DEPARTEMEN SESUAI FLOWCHART DOKUMEN TA
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Stasiun Pengawasan Alur Informasi Departemen Terintegrasi</div>', unsafe_allow_html=True)
        
        tabs = st.tabs([
            "1. Perencanaan & Desain", "2. Produksi Lapangan", "3. Pembelian & Logistik", 
            "4. QA / QC", "5. Gudang Material", "6. Manajemen Fasilitas", "7. Eksekutif Pemantau"
        ])
        
        # TAB 1: DESAIN & PERENCANAAN PRODUKSI
        with tabs[0]:
            col1, col2 = st.columns(2)
            with col1:
                new_schedule = st.text_input("Master Schedule Konstruksi Lambung", value=db["Master Schedule"])
            with col2:
                new_pwbs = st.text_input("Pembagian Blok Struktur (PWBS)", value=db["PWBS / Area Kerja"])
            if st.button("Update Data Perencanaan"):
                update_data_tunggal("Master Schedule", new_schedule)
                update_data_tunggal("PWBS / Area Kerja", new_pwbs)
                st.success("Sinkronisasi data perencanaan sukses dilakukan.")
                st.rerun()
                
        # TAB 2: DEPARTEMEN PRODUKSI
        with tabs[1]:
            st.markdown(f"<p style='font-size:14px;'><b>Acuan Desain yang Digunakan:</b> {db['Master Schedule']} | {db['PWBS / Area Kerja']}</p>", unsafe_allow_html=True)
            prog_val = st.slider("Persentase Progres Perakitan Blok Lambung", 0, 100, 65)
            st.progress(prog_val / 100)
            
            st.markdown("<br>", unsafe_allow_html=True)
            biaya_input = st.number_input("Input Biaya Operasional Tambahan Lapangan (Rp)", min_value=0, step=5000000)
            if st.button("Kirim Laporan Validasi Produksi"):
                total_baru = int(db["Biaya Konstruksi Terpakai"]) + biaya_input
                update_data_tunggal("Biaya Konstruksi Terpakai", total_baru)
                st.success("Database finansial produksi lapangan berhasil diperbarui.")
                st.rerun()
                
        # TAB 3: PEMBELIAN & LOGISTIK
        with tabs[2]:
            with st.form("form_logistik_new"):
                v_name = st.text_input("Mitra Pabrikan / Supplier Pelat Baja", value=db["Vendor Utama Logistik"])
                v_vol = st.number_input("Volume Pengadaan Logistik Komponen (Ton)", min_value=0, value=50)
                if st.form_submit_button("Ajukan Nota Permintaan Pembelian"):
                    update_data_tunggal("Vendor Utama Logistik", v_name)
                    st.warning(f"Permintaan diteruskan. Material seberat {v_vol} Ton menunggu verifikasi kelayakan uji mutu oleh divisi QA/QC.")
                    st.rerun()
                    
        # TAB 4: DEPARTEMEN QA/QC
        with tabs[3]:
            st.markdown(f"<div style='background:#1f293d; padding:12px; border-radius:6px; font-size:14px; margin-bottom:15px;'><b>Log Sertifikasi Mutu Terakhir:</b> {db['Status Inspeksi QA/QC']}</div>", unsafe_allow_html=True)
            status_qa = st.selectbox("Perbarui Kualifikasi Mutu Konstruksi & Pelat", [
                "Lolos Uji NDT Radiography Butt Joint Blok M1",
                "Sertifikasi Material Mill Certificate Pelat Baja Disetujui BKI",
                "Ditemukan Deformasi Pelat pada Area Blok Bow/Haluan (Butuh Perbaikan/Rework)"
            ])
            if st.button("Validasi Dokumen Mutu"):
                update_data_tunggal("Status Inspeksi QA/QC", status_qa)
                st.success("Status inspeksi kelayakan bangunan baru berhasil dipublikasikan.")
                st.rerun()
                
        # TAB 5: GUDANG MATERIAL
        with tabs[4]:
            st.markdown(f"<h5>Sisa Stok Bahan Baku Pelat Baja: <span style='color:#38bdf8;'>{db['Volume Stok Pelat Baja (Gudang)']} Ton</span></h5>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                tipe_mutasi = st.radio("Aksi Mutasi Inventaris", ["Material Masuk (Lolos Inspeksi)", "Pengambilan Barang untuk Bengkel Produksi"])
            with c2:
                vol_mutasi = st.number_input("Kuantitas Berat Material Baja (Ton)", min_value=1, value=15)
            if st.button("Eksekusi Mutasi Gudang"):
                stok_awal = int(db["Volume Stok Pelat Baja (Gudang)"])
                stok_akhir = stok_awal + vol_mutasi if tipe_mutasi == "Material Masuk (Lolos Inspeksi)" else stok_awal - vol_mutasi
                update_data_tunggal("Volume Stok Pelat Baja (Gudang)", stok_akhir)
                st.success("Pencatatan mutasi inventaris logistik berhasil direkam.")
                st.rerun()
                
        # TAB 6: DEPARTEMEN FASILITAS
        with tabs[5]:
            st.markdown(f"<p style='font-size:14px;'><b>Status Kelayakan Infrastruktur Alat Berat:</b> {db['Kelayakan Fasilitas Gantry Crane']}</p>", unsafe_allow_html=True)
            status_fasilitas = st.selectbox("Perbarui Log Kondisi Fasilitas Mekanis", [
                "Operasional Normal - Sertifikasi Aktif",
                "Gantry Crane Jalur Rel Selatan dalam Penjadwalan Kalibrasi Rutin",
                "Fasilitas Slipway Luncuran Kosong dan Siap Digunakan"
            ])
            if st.button("Update Log Fasilitas"):
                update_data_tunggal("Kelayakan Fasilitas Gantry Crane", status_fasilitas)
                st.success("Kondisi kelayakan aset produksi berhasil diperbarui.")
                st.rerun()
                
        # TAB 7: MANAJEMEN EKSEKUTIF
        with tabs[6]:
            st.markdown("<p style='font-size:13px; color:#94a3b8;'>Status Konsolidasi Parameter Riil (Hasil Integrasi Database Eksternal SQLite)</p>", unsafe_allow_html=True)
            df_tabel = pd.DataFrame(list(db.items()), columns=['Parameter Manufaktur Galangan', 'Status Valid Terkini'])
            st.dataframe(df_tabel, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif nav_selection == "Konfigurasi Sistem":
        st.markdown("<h2>Konfigurasi & Manajemen Pengguna</h2>", unsafe_allow_html=True)
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("Halaman khusus pengaturan hak akses database server, restrukturisasi skema sistem, dan konfigurasi port jaringan terintegrasi.")
        st.markdown('</div>', unsafe_allow_html=True)
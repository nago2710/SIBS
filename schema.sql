-- ============================================================
-- SIBS: Shipyard Integrated Business System
-- Database Schema for Supabase (PostgreSQL)
--
-- Sumber Data:
--   Skripsi: "Desain Integrasi Sistem Informasi Pembangunan
--            Kapal Pada Sebuah Galangan Kapal Kecil Indonesia"
--            oleh Ratih Laratasari Pagayang (Unhas, 2025)
--   Excel VBA: Sistem Informasi Galangan Kecil.xlsm
-- ============================================================

-- ===================== USERS =====================
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nama_lengkap VARCHAR(100),
    role VARCHAR(30) NOT NULL DEFAULT 'viewer',
    departemen VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== KAPAL (Ship Data) =====================
CREATE TABLE IF NOT EXISTS kapal (
    id BIGSERIAL PRIMARY KEY,
    id_project VARCHAR(50) UNIQUE NOT NULL,
    id_gambar VARCHAR(50),
    nama_gambar VARCHAR(100),
    type_kapal VARCHAR(50),
    nama_kapal VARCHAR(100) NOT NULL,
    kecepatan FLOAT,
    gt FLOAT,
    volume FLOAT,
    displacement FLOAT,
    loa FLOAT,
    lwl FLOAT,
    lbp FLOAT,
    b FLOAT,
    h FLOAT,
    t FLOAT,
    cb FLOAT,
    cm FLOAT,
    cw FLOAT,
    cp FLOAT,
    status VARCHAR(30) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== BLOK =====================
CREATE TABLE IF NOT EXISTS blok (
    id BIGSERIAL PRIMARY KEY,
    id_project VARCHAR(50) NOT NULL REFERENCES kapal(id_project) ON DELETE CASCADE,
    id_blok VARCHAR(50) NOT NULL,
    nama_blok VARCHAR(100),
    level VARCHAR(50),
    jumlah_sub_blok INT DEFAULT 0,
    total_berat FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(id_project, id_blok)
);

-- ===================== PWBS DETAIL =====================
CREATE TABLE IF NOT EXISTS pwbs_detail (
    id BIGSERIAL PRIMARY KEY,
    id_project VARCHAR(50) NOT NULL,
    id_blok VARCHAR(50) NOT NULL,
    id_material_ref VARCHAR(50),
    nama_material VARCHAR(100),
    jenis_material VARCHAR(50),
    nama_panel VARCHAR(100),
    kode VARCHAR(100),
    frame VARCHAR(50),
    posisi VARCHAR(50),
    panjang FLOAT DEFAULT 0,
    lebar FLOAT DEFAULT 0,
    tebal FLOAT DEFAULT 0,
    tinggi FLOAT DEFAULT 0,
    jumlah INT DEFAULT 1,
    luasan FLOAT DEFAULT 0,
    volume_mm3 FLOAT DEFAULT 0,
    berat FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== MATERIAL =====================
CREATE TABLE IF NOT EXISTS material (
    id BIGSERIAL PRIMARY KEY,
    id_material VARCHAR(50) UNIQUE NOT NULL,
    nama_material VARCHAR(100) NOT NULL,
    jenis_material VARCHAR(50),
    id_project VARCHAR(50),
    id_item VARCHAR(50),
    grade VARCHAR(30),
    jumlah INT DEFAULT 0,
    pressure VARCHAR(30),
    panjang FLOAT DEFAULT 0,
    lebar FLOAT DEFAULT 0,
    tebal FLOAT DEFAULT 0,
    diameter FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== PEKERJA =====================
CREATE TABLE IF NOT EXISTS pekerja (
    id BIGSERIAL PRIMARY KEY,
    id_pekerja VARCHAR(50) UNIQUE NOT NULL,
    nama_pekerjaan VARCHAR(100) NOT NULL,
    jenis_pekerjaan VARCHAR(50),
    id_project VARCHAR(50),
    id_item VARCHAR(50),
    id_material VARCHAR(50),
    id_fasilitas VARCHAR(50),
    level VARCHAR(50),
    posisi_kerja VARCHAR(50),
    jumlah INT DEFAULT 1,
    upah_per_hari FLOAT DEFAULT 0,
    total_upah FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== FASILITAS =====================
CREATE TABLE IF NOT EXISTS fasilitas (
    id BIGSERIAL PRIMARY KEY,
    id_fasilitas VARCHAR(50) UNIQUE NOT NULL,
    nama_fasilitas VARCHAR(100) NOT NULL,
    jenis_fasilitas VARCHAR(50),
    kapasitas FLOAT DEFAULT 0,
    jumlah INT DEFAULT 1,
    daya FLOAT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Operasional',
    sertifikasi_aktif BOOLEAN DEFAULT TRUE,
    biaya_harian FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fasilitas_maintenance (
    id BIGSERIAL PRIMARY KEY,
    id_fasilitas VARCHAR(50) NOT NULL REFERENCES fasilitas(id_fasilitas) ON DELETE CASCADE,
    tipe VARCHAR(30) NOT NULL,
    deskripsi TEXT,
    status VARCHAR(30) DEFAULT 'pending',
    tanggal_request TIMESTAMPTZ DEFAULT NOW(),
    tanggal_selesai TIMESTAMPTZ,
    requested_by VARCHAR(50),
    approved_by VARCHAR(50),
    catatan_selesai TEXT
);

CREATE TABLE IF NOT EXISTS fasilitas_usage (
    id BIGSERIAL PRIMARY KEY,
    id_fasilitas VARCHAR(50) NOT NULL REFERENCES fasilitas(id_fasilitas) ON DELETE CASCADE,
    id_project VARCHAR(50),
    tanggal_mulai DATE NOT NULL,
    tanggal_selesai DATE,
    durasi_jam FLOAT DEFAULT 0,
    biaya FLOAT DEFAULT 0,
    keterangan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== SCHEDULE DETAIL =====================
CREATE TABLE IF NOT EXISTS schedule_detail (
    id BIGSERIAL PRIMARY KEY,
    id_project VARCHAR(50) NOT NULL,
    no_urut VARCHAR(20) NOT NULL,
    nama_pekerjaan VARCHAR(200) NOT NULL,
    tanggal_mulai DATE,
    tanggal_selesai DATE,
    parent_no VARCHAR(20),
    progress FLOAT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== PRODUKSI DATA =====================
CREATE TABLE IF NOT EXISTS produksi_data (
    id BIGSERIAL PRIMARY KEY,
    id_project VARCHAR(50) NOT NULL,
    id_item VARCHAR(100) NOT NULL,
    kode_part VARCHAR(100),
    nama_part VARCHAR(200),
    berat_part FLOAT DEFAULT 0,
    berat_las FLOAT DEFAULT 0,
    tanggal DATE,
    status VARCHAR(30) DEFAULT 'planned',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== GUDANG BARANG =====================
CREATE TABLE IF NOT EXISTS gudang_barang (
    id BIGSERIAL PRIMARY KEY,
    id_barang VARCHAR(50) UNIQUE NOT NULL,
    nama_barang VARCHAR(100) NOT NULL,
    jenis VARCHAR(50),
    satuan VARCHAR(30) DEFAULT 'unit',
    stok_current FLOAT DEFAULT 0,
    stok_minimum FLOAT DEFAULT 0,
    lokasi_rak VARCHAR(50),
    jenis_gudang VARCHAR(30) DEFAULT 'tertutup',
    spesifikasi TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gudang_mutasi (
    id BIGSERIAL PRIMARY KEY,
    id_barang VARCHAR(50) NOT NULL REFERENCES gudang_barang(id_barang) ON DELETE CASCADE,
    tipe VARCHAR(20) NOT NULL CHECK (tipe IN ('masuk', 'keluar')),
    jumlah FLOAT NOT NULL CHECK (jumlah > 0),
    id_project VARCHAR(50),
    supplier VARCHAR(100),
    keterangan TEXT,
    tanggal TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- ===================== INSPEKSI QA/QC =====================
CREATE TABLE IF NOT EXISTS inspeksi_qc (
    id BIGSERIAL PRIMARY KEY,
    id_project VARCHAR(50) NOT NULL,
    id_blok VARCHAR(50),
    kategori VARCHAR(100) NOT NULL,
    sub_kategori VARCHAR(100),
    item_inspeksi VARCHAR(200),
    status VARCHAR(30) DEFAULT 'pending',
    hasil TEXT,
    catatan TEXT,
    inspector VARCHAR(50),
    tanggal_inspeksi TIMESTAMPTZ DEFAULT NOW(),
    approved_by VARCHAR(50),
    tanggal_approval TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== SUPPLIER =====================
CREATE TABLE IF NOT EXISTS supplier (
    id BIGSERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    alamat TEXT,
    telepon VARCHAR(30),
    email VARCHAR(100),
    jenis_supply VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== PURCHASE ORDER =====================
CREATE TABLE IF NOT EXISTS purchase_order (
    id BIGSERIAL PRIMARY KEY,
    no_po VARCHAR(50) UNIQUE NOT NULL,
    id_supplier BIGINT REFERENCES supplier(id),
    id_project VARCHAR(50),
    tanggal_order DATE NOT NULL,
    tanggal_target DATE,
    status VARCHAR(30) DEFAULT 'draft',
    total_harga FLOAT DEFAULT 0,
    catatan TEXT,
    created_by VARCHAR(50),
    approved_by VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS purchase_order_item (
    id BIGSERIAL PRIMARY KEY,
    id_po BIGINT NOT NULL REFERENCES purchase_order(id) ON DELETE CASCADE,
    nama_barang VARCHAR(100) NOT NULL,
    spesifikasi VARCHAR(200),
    jumlah FLOAT NOT NULL,
    satuan VARCHAR(30) DEFAULT 'unit',
    harga_satuan FLOAT DEFAULT 0,
    subtotal FLOAT DEFAULT 0
);

-- ===================== PERMINTAAN MATERIAL (Produksi → Gudang) =====================
CREATE TABLE IF NOT EXISTS permintaan_material (
    id BIGSERIAL PRIMARY KEY,
    id_project VARCHAR(50) NOT NULL,
    id_barang VARCHAR(50),
    nama_barang VARCHAR(100) NOT NULL,
    jumlah FLOAT NOT NULL,
    satuan VARCHAR(30) DEFAULT 'unit',
    keperluan TEXT,
    status VARCHAR(30) DEFAULT 'pending',
    requested_by VARCHAR(50),
    approved_by VARCHAR(50),
    tanggal_request TIMESTAMPTZ DEFAULT NOW(),
    tanggal_approval TIMESTAMPTZ
);

-- ===================== AUDIT LOG =====================
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50),
    action VARCHAR(50) NOT NULL,
    target_table VARCHAR(50),
    target_id TEXT,
    old_value JSONB,
    new_value JSONB,
    keterangan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===================== INDEXES =====================
CREATE INDEX IF NOT EXISTS idx_kapal_status ON kapal(status);
CREATE INDEX IF NOT EXISTS idx_blok_project ON blok(id_project);
CREATE INDEX IF NOT EXISTS idx_pwbs_project_blok ON pwbs_detail(id_project, id_blok);
CREATE INDEX IF NOT EXISTS idx_material_project ON material(id_project);
CREATE INDEX IF NOT EXISTS idx_pekerja_project ON pekerja(id_project);
CREATE INDEX IF NOT EXISTS idx_schedule_project ON schedule_detail(id_project);
CREATE INDEX IF NOT EXISTS idx_produksi_project ON produksi_data(id_project);
CREATE INDEX IF NOT EXISTS idx_gudang_mutasi_barang ON gudang_mutasi(id_barang);
CREATE INDEX IF NOT EXISTS idx_gudang_mutasi_tanggal ON gudang_mutasi(tanggal);
CREATE INDEX IF NOT EXISTS idx_inspeksi_project ON inspeksi_qc(id_project);
CREATE INDEX IF NOT EXISTS idx_inspeksi_kategori ON inspeksi_qc(kategori);
CREATE INDEX IF NOT EXISTS idx_po_project ON purchase_order(id_project);
CREATE INDEX IF NOT EXISTS idx_po_status ON purchase_order(status);
CREATE INDEX IF NOT EXISTS idx_permintaan_project ON permintaan_material(id_project);
CREATE INDEX IF NOT EXISTS idx_permintaan_status ON permintaan_material(status);
CREATE INDEX IF NOT EXISTS idx_audit_username ON audit_log(username);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);
CREATE INDEX IF NOT EXISTS idx_fas_maintenance_fas ON fasilitas_maintenance(id_fasilitas);
CREATE INDEX IF NOT EXISTS idx_fas_usage_fas ON fasilitas_usage(id_fasilitas);

# SIBS: Shipyard Integrated Business System

**Sistem Integrasi Bisnis & Operasional Galangan Kapal**  
*Enterprise Clean White Edition — Powered by Supabase (PostgreSQL)*

Berdasarkan riset ilmiah:
1. Skripsi **Ratih Laratasari Pagayang** (*"Desain Integrasi Sistem Informasi Pembangunan Kapal Pada Sebuah Galangan Kapal Kecil Indonesia"*, Universitas Hasanuddin, 2025)
2. Sistem Informasi Galangan Kecil Excel VBA Workbook (*230+ sheet*)

---

## 📋 Daftar Isi
- [Fitur Utama](#-fitur-utama)
- [Struktur Proyek](#-struktur-proyek)
- [Panduan Setup Supabase](#-panduan-setup-supabase)
- [Instalasi & Menjalankan Aplikasi](#-instalasi--menjalankan-aplikasi)
- [Akun Pengguna Bawaan](#-akun-pengguna-bawaan)
- [7 Modul Departemen](#-7-modul-departemen)
- [Data Riil & Seed Data](#-data-riil--seed-data)

---

## ✨ Fitur Utama

- 🚢 **7 Departemen Terintegrasi Penuh**:
  - **Perencanaan**: Dimensi utama kapal (LOA, LBP, B, H, T, GT, Vs, Cb, Cm, Cw, Cp), blok lambung (HS-04, HS-06), PWBS level 1-4, dan Drawing Register.
  - **Produksi Lapangan**: Jadwal perakitan 7 tahapan riil, update progres fisik per sub-pekerjaan, log fabrikasi (cutting & welding per frame), dan formulir requisition material ke gudang.
  - **Pembelian & Logistik**: Database supplier galangan, penerbitan Purchase Order (PO), approval status pesanan (draft -> submitted -> approved -> delivered).
  - **Quality Control (QA/QC)**: 39 standar uji klasifikasi BKI (NDT, visual, tightness, hydrostatic), status persetujuan, dan tracking defect/remedial work.
  - **Material & Gudang**: Master stok material pelat & profil baja, consumable pengelasan, cat marine, peringatan stok menipis (low-stock alert), transaksi mutasi masuk/keluar, dan approval pengeluaran barang.
  - **Manajemen Fasilitas**: Kesiapan alat berat (gantry crane, plasma cutting, drydock), jadwal & penanganan maintenance, serta pencatatan utilisasi biaya harian.
  - **Manajemen Eksekutif & BAP**: Dashboard lintas departemen, Kurva S rencana vs realisasi, analisis biaya proyek, dan generator Berita Acara Pemeriksaan (BAP) siap cetak langsung dari browser (`Ctrl + P`).

- 🔒 **Keamanan & Standar Enterprise**:
  - Hashing kata sandi berbasis standar industri **PBKDF2-SHA256** dengan dynamic salt.
  - Throttling percobaan login untuk mencegah brute-force.
  - Pencatatan jejak audit (Audit Trail) otomatis untuk setiap aksi login, mutasi, dan perubahan data.
  - Role-based access control (RBAC) dengan pemisahan wewenang tiap departemen.

- 🗄️ **Database Cloud Supabase (PostgreSQL)**:
  - 16+ tabel relasional ternormalisasi dengan foreign keys dan indexes performa tinggi.

---

## 📁 Struktur Proyek

```
SIBS/
├── app.py                      # Router utama aplikasi Streamlit
├── config.py                   # Konfigurasi Supabase, App, dan Security
├── database.py                 # Wrapper CRUD client Supabase
├── auth.py                     # Otentikasi & hashing PBKDF2
├── utils.py                    # CSS korporat putih, format helper, KPI card, print styling
├── schema.sql                  # Skrip DDL PostgreSQL untuk Supabase
├── seed_data.py                # Skrip injeksi data awal riil dari Excel/Skripsi
├── requirements.txt            # Dependensi Python
├── .env.example                # Template kredensial Supabase
├── .env                        # Kredensial aktif Supabase (jangan dicommit)
├── departments/                # Paket modul 7 departemen
│   ├── __init__.py
│   ├── perencanaan.py          # Desain & PWBS
│   ├── produksi.py             # Jadwal & Fabrikasi Lapangan
│   ├── pembelian.py            # Supplier & Purchase Order
│   ├── qaqc.py                 # 39 Kategori Inspeksi BKI
│   ├── gudang.py               # Stok, Mutasi & Approval Requisition
│   ├── fasilitas.py            # Alat Berat, Maintenance & Utilisasi
│   └── eksekutif.py            # Kurva S, Biaya & Cetak Lembar BAP
└── asset/                      # File aset gambar
```

---

## 🚀 Panduan Setup Supabase

Aplikasi SIBS menggunakan database PostgreSQL berbasis cloud di **Supabase**. Ikuti langkah-langkah mudah berikut untuk mengonfigurasikannya:

### 1. Buat Proyek Baru di Supabase
1. Kunjungi [supabase.com](https://supabase.com) dan masuk (atau daftar akun gratis).
2. Klik tombol **"New project"**.
3. Masukkan nama proyek (misal: `SIBS-Galangan`) dan buat **Database Password** yang kuat.
4. Pilih region terdekat (misal: `Singapore (ap-southeast-1)`).
5. Tunggu 1-2 menit hingga proyek selesai disiapkan.

### 2. Jalankan Skema Database (`schema.sql`)
1. Di dashboard Supabase Anda, buka menu **SQL Editor** pada sidebar kiri (ikon `>_`).
2. Buka file `schema.sql` yang ada di proyek SIBS, salin (copy) seluruh kodenya.
3. Tempelkan (paste) ke SQL Editor di Supabase.
4. Klik tombol **"Run"** (atau tekan `Ctrl + Enter`).
5. Seluruh tabel relasional, enum, dan indeks akan otomatis terbuat.

### 3. Salin API URL & Anon Key ke File `.env`
1. Di dashboard Supabase, buka menu **Project Settings** (ikon gerigi di kiri bawah) → **API**.
2. Salin nilai **Project URL** (contoh: `https://xyzcompany.supabase.co`).
3. Salin nilai **Project API Keys** bagian `anon` / `public`.
4. Buka file `.env` di folder proyek SIBS, lalu isi nilainya:
   ```env
   SUPABASE_URL=https://xyzcompany.supabase.co
   SUPABASE_KEY=eyJh......
   ```

---

## 💻 Instalasi & Menjalankan Aplikasi

### 1. Aktifkan Virtual Environment & Pasang Dependensi
Pastikan virtual environment Python aktif, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 2. Isi Data Awal Riil Galangan Kapal (Seed Data)
Setelah Supabase siap dan terhubung di `.env`, jalankan skrip berikut satu kali untuk mengisi data kapal KM. Nusantara, blok HS-06, jadwal 7 tahap, material, alat berat, dan akun pengguna:
```bash
python seed_data.py
```

### 3. Jalankan Aplikasi Web
```bash
streamlit run app.py
```
Aplikasi akan terbuka otomatis di peramban Anda pada alamat: `http://localhost:8501`.

---

## 👥 Akun Pengguna Bawaan

| Role | Username | Password | Wewenang Akses |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Akses penuh ke seluruh departemen, manajemen user, dan log audit |
| **Perencanaan** | `perencanaan` | `super123` | Desain kapal, data blok lambung, dan hierarki PWBS |
| **Produksi** | `produksi` | `super123` | Jadwal perakitan, data pemotongan/las, dan permintaan material |
| **Pembelian** | `pembelian` | `super123` | Rekanan supplier dan penerbitan Purchase Order |
| **QA / QC** | `qaqc` | `super123` | 39 standar inspeksi mutu BKI dan approval pengujian |
| **Gudang** | `gudang` | `super123` | Stok inventaris, transaksi mutasi, dan pengeluaran material |
| **Fasilitas** | `fasilitas` | `super123` | Monitoring alat berat, jadwal maintenance, dan utilisasi |
| **Eksekutif** | `eksekutif` | `super123` | Dashboard pimpinan, Kurva S, analisis biaya, dan cetak BAP |

---

## 🚢 Data Riil Kapal & Proyek (Berdasarkan Sumber Riset)

- **Identitas Proyek Kapal**: KM. NUSANTARA (`NB-002`) / KM. LAKAAN (`NB-001`)
- **Tipe Kapal**: Ferry Ro-Ro (Penumpang & Kendaraan)
- **Ukuran**: 750 Gross Tonnage (GT)
- **Dimensi Utama**:
  - Length Overall (LOA): 70.00 m
  - Length on Waterline (LWL): 68.00 m
  - Length Between Perpendiculars (LBP): 65.00 m
  - Breadth / Lebar (B): 14.00 m
  - Depth / Tinggi (H): 4.80 m
  - Draught / Sarat Air (T): 3.20 m
  - Service Speed (Vs): 15.00 knot
  - Koefisien Bentuk: Cb = 0.70, Cm = 0.80, Cw = 0.80, Cp = 0.70
- **Tahapan Perakitan Blok HS-06 (Jan - Mar 2025)**:
  1. Pembangunan Panel Deck (Durasi: 12 hari, Bobot: 15%)
  2. Pembangunan Panel Bottom (Durasi: 18 hari, Bobot: 20%)
  3. Pembangunan Panel Sisi SB (Durasi: 21 hari, Bobot: 15%)
  4. Pembangunan Panel Sisi PS (Durasi: 21 hari, Bobot: 15%)
  5. Assembly Bottom + Sisi (Durasi: 15 hari, Bobot: 20%)
  6. Assembly Deck Panel (Durasi: 12 hari, Bobot: 10%)
  7. Finishing, Blasting Sa 2.5 & Painting (Durasi: 13 hari, Bobot: 5%)

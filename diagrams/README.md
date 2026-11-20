# 📊 DOKUMENTASI DIAGRAM ALIR & PERANCANGAN SISTEM (BAB IV)
## Shipyard Integrated Business System (SIBS)

Dokumen ini disusun khusus sebagai bahan lampiran dan isi utama **BAB IV (Hasil dan Pembahasan / Perancangan Sistem)** pada laporan Skripsi/Tugas Akhir.

---

### 📑 Daftar File Diagram

| No. File | Nama Diagram | Deskripsi untuk Laporan Skripsi |
| :--- | :--- | :--- |
| `01_arsitektur_sistem_global.md` | **Arsitektur Sistem Terintegrasi SIBS** | Menggambarkan hubungan arsitektur antara UI Streamlit, Modul 7 Departemen, Security PBKDF2, dan Database Supabase Cloud PostgreSQL. |
| `02_flowchart_perencanaan.md` | **Flowchart Dept. Perencanaan & Desain** | Alur penentuan dimensi utama kapal, pembagian blok lambung, hierarki PWBS level 1-4, dan verifikasi drawing register. |
| `03_flowchart_produksi.md` | **Flowchart Dept. Produksi Lapangan** | Alur penjadwalan WBS perakitan blok, pencatatan cutting/welding frame, pengajuan requisition material, dan update progres. |
| `04_flowchart_pembelian.md` | **Flowchart Dept. Pembelian & Logistik** | Alur penerimaan kebutuhan material, database supplier, penerbitan Purchase Order (PO), approval, dan tracking pengiriman. |
| `05_flowchart_qaqc.md` | **Flowchart Dept. QA/QC (Pengendalian Mutu)** | Alur pengujian mutu berbasis 39 kategori standar BKI, inspeksi NDT las, evaluasi approve/reject, dan tindakan perbaikan (remedial work). |
| `06_flowchart_gudang.md` | **Flowchart Dept. Material & Gudang** | Alur penerimaan barang dari vendor, penempatan rak/yard, persetujuan pengeluaran permintaan produksi, mutasi stok, dan peringatan batas minimum. |
| `07_flowchart_fasilitas.md` | **Flowchart Dept. Manajemen Fasilitas** | Alur monitoring kesiapan crane & drydock, permintaan servis/maintenance, pencatatan utilisasi alat berat, dan alokasi biaya harian proyek. |
| `08_flowchart_eksekutif_bap.md` | **Flowchart Dept. Eksekutif & BAP** | Alur agregasi metrik lintas departemen, plotting Kurva S rencana vs realisasi, analisis biaya, dan penerbitan Berita Acara Pemeriksaan (BAP). |
| `09_cross_functional_swimlane.md` | **Cross-Functional / Swimlane Diagram** | Menggambarkan interaksi proses bisnis dan perpindahan data antar 7 departemen secara horizontal dari awal hingga akhir. |
| `10_dfd_konteks_level_0.md` | **Data Flow Diagram (DFD) Level 0 / Konteks** | Diagram konteks sistem yang memperlihatkan entitas luar (7 Departemen, BKI, Owner Surveyor) dan arus data masuk/keluar ke SIBS. |
| `11_dfd_level_1.md` | **Data Flow Diagram (DFD) Level 1** | Dekomposisi 7 proses utama sistem dan keterhubungannya dengan data store Supabase. |
| `12_erd_database.md` | **Entity Relationship Diagram (ERD)** | Relasi relasional antar 16+ tabel database (kapal, blok, pwbs, schedule, gudang, po, inspeksi, fasilitas, dsb.). |
| `viewer.html` | **Interactive Diagram Viewer** | File HTML yang bisa dibuka di browser apa saja untuk melihat seluruh diagram dalam visual rapi dan mengekspornya ke PNG/SVG. |

---

### 💡 Cara Memasukkan ke Dokumen Word / Skripsi

1. **Buka file `viewer.html` di Google Chrome / Edge**:
   - Klik kanan file `viewer.html` → *Open with Google Chrome*.
   - Semua diagram akan ter-render otomatis dalam bentuk gambar grafis yang sangat jernih.
   - Anda dapat menekan tombol **"Download PNG"** atau melakukan *screenshot* / *copy image* dan menempelkannya (*paste*) langsung ke Microsoft Word.
2. **Alternatif via Mermaid Live Editor**:
   - Buka situs [mermaid.live](https://mermaid.live).
   - Salin blok kode ```mermaid dari file `.md` yang Anda inginkan.
   - Unduh gambar dalam resolusi tinggi (PNG / SVG).
3. **Format Caption Gambar Akademis**:
   - Gunakan format standar Unhas:
     > **Gambar 4.x** Diagram Alir Proses Produksi Pembangunan Blok Lambung (Sumber: Hasil Perancangan SIBS, 2026)

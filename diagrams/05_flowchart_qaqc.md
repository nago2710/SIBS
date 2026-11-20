# Diagram 4.5: Flowchart Departemen Quality Assurance & Quality Control (QA/QC)

### Deskripsi untuk Bab 4:
> **Gambar 4.5 Diagram Alir Pengendalian Mutu Konstruksi Kapal Berbasis 39 Standar Uji BKI**  
> Menggambarkan mekanisme pengawasan mutu terstruktur sesuai klasifikasi Biro Klasifikasi Indonesia (BKI) dan supervisi Owner Surveyor. Meliputi permohonan inspeksi komponen blok, pengujian tanpa merusak (*Non-Destructive Testing / NDT*), verifikasi standar hasil uji, penerbitan status persetujuan (*Approved / Pending / Rejected*), hingga pengelolaan tindakan korektif (*Remedial Work*).

```mermaid
flowchart TD
    Start(["Mulai Proses Inspeksi Mutu QA/QC"]) --> NotifProduksi["Terima Permintaan Inspeksi dari Produksi atau Agenda Rutin Blok"]
    NotifProduksi --> PilihKategori["Pilih Kategori Standar dari 39 Katalog Standar BKI (Tabel 'QC_CATEGORIES')"]
    
    PilihKategori --> TentukanMetode["Tentukan Metode Pengujian Sesuai Komponen (Visual VT, Ultrasonic UT, Radiography RT, Magnetic MT, Vacuum Box, atau Hydrostatic)"]
    TentukanMetode --> EksekusiInspeksi["Lakukan Pengujian Fisik Bersama Inspektur Galangan / Surveyor BKI"]

    EksekusiInspeksi --> CatatHasil["Input Data Temuan Teknis ke Formulir Inspeksi Baru (Tabel 'inspeksi_qc')"]
    CatatHasil --> EvaluasiHasil{"Apakah Hasil Uji Memenuhi Kriteria Standar Klasifikasi?"}

    EvaluasiHasil -- "Tidak Memenuhi (Cacat / Defect)" --> SetRejected["Tetapkan Status: 'Rejected'"]
    SetRejected --> CatatDefect["Dokumentasikan Lokasi, Jenis Cacat (Undercut/Porosity/Crack), dan Foto Temuan"]
    CatatDefect --> MasukLogRemedial["Masukkan Komponen ke Daftar Rekapitulasi 'Defect & Remedial Work'"]
    MasukLogRemedial --> TerbitkanNCR["Terbitkan Catatan Ketidaksesuaian ke Departemen Produksi"]
    TerbitkanNCR --> PerbaikanProduksi["Produksi Melakukan Gouging, Pengelasan Ulang, atau Perbaikan Sambungan"]
    PerbaikanProduksi --> EksekusiInspeksi

    EvaluasiHasil -- "Masih Perlu Kajian / Data Kurang" --> SetPending["Tetapkan Status: 'Pending' (Menunggu Hasil Uji Laboratorium / Approval Lanjutan)"]
    SetPending --> SelesaiPending(["Menunggu Dokumen Pendukung Lengkap"])

    EvaluasiHasil -- "Memenuhi Standar BKI" --> SetApproved["Tetapkan Status: 'Approved'"]
    SetApproved --> SignApproval["Perekaman Identitas Verifikator, Tanggal Approval, dan Catatan Kesesuaian"]
    SignApproval --> UpdateStatistik["Pembaruan Otomatis Statistik Kepatuhan Mutu (% Lolos) pada Dashboard Eksekutif"]
    UpdateStatistik --> Selesai(["Komponen Dinyatakan Lolos & Siap Erection"])
```

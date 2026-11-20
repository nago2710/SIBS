# Diagram 4.8: Flowchart Departemen Manajemen Eksekutif & Penerbitan BAP

### Deskripsi untuk Bab 4:
> **Gambar 4.8 Diagram Alir Dashboard Eksekutif, Kurva S, dan Penerbitan Berita Acara Pemeriksaan (BAP)**  
> Mengilustrasikan fungsi pengendalian strategis tingkat manajemen puncak (*Executive Level*). Meliputi agregasi data real-time dari 6 departemen operasional, pembentukan Kurva S kemajuan fisik (*Planned vs Actual S-Curve*), monitoring deviasi anggaran proyek, hingga penerbitan dan pencetakan dokumen resmi Berita Acara Pemeriksaan (BAP) kemajuan pekerjaan yang siap cetak format A4.

```mermaid
flowchart TD
    Start(["Mulai Akses Manajemen Eksekutif"]) --> TarikDataLengkap["Sistem Menjalankan Fungsi 'get_dashboard_stats(active_project)'"]
    
    TarikDataLengkap --> AgregasiMetrics["Agregasi Data Multi-Departemen Secara Real-Time dari Supabase:
    1. Progres Fisik Rata-Rata WBS (Tabel 'schedule_detail')
    2. Tingkat Kelulusan Mutu QA/QC (Tabel 'inspeksi_qc')
    3. Status Defisit Inventaris Material (Tabel 'gudang_barang')
    4. Antrean Purchase Order & Permintaan Material"]

    AgregasiMetrics --> TampilkanOverview["Tampilkan Ringkasan Kartu KPI Eksekutif & Profil Kapal Aktif"]

    TampilkanOverview --> PilihFitur{"Pilih Analisis Manajemen Eksekutif"}

    %% FITUR 1: KURVA S
    PilihFitur -- "Analisis Kurva S Kemajuan Fisik" --> KalkulasiKumulatif["Hitung Bobot Kumulatif Jadwal Rencana vs Realisasi Progres Lapangan"]
    KalkulasiKumulatif --> PlottingSCurve["Visualisasikan Grafik Kurva S (Garis Rencana Biru vs Garis Realisasi Hijau)"]
    PlottingSCurve --> EvaluasiDeviasi{"Apakah Realisasi Progres >= Jadwal Rencana?"}
    EvaluasiDeviasi -- "Ya" --> StatusOnTrack["Tampilkan Status: 'Proyek Tepat Waktu / Lebih Cepat (+%)'"]
    EvaluasiDeviasi -- "Tidak" --> StatusDelayed["Tampilkan Peringatan: 'Proyek Mengalami Deviasi Keterlambatan (-%)'"]
    StatusOnTrack --> TinjauLanjut
    StatusDelayed --> TinjauLanjut["Lakukan Tindakan Mitigasi Jadwal"]

    %% FITUR 2: BIAYA
    PilihFitur -- "Analisis Biaya & Anggaran" --> RekapBiaya["Rekapitulasi Anggaran Proyek vs Realisasi Serapan Biaya (Material, Upah, Fasilitas, NDT)"]
    RekapBiaya --> HitungVarians["Hitung Selisih / Deviasi Anggaran per Kategori Biaya"]
    HitungVarians --> TinjauLanjut

    %% FITUR 3: PENERBITAN BAP
    PilihFitur -- "Penerbitan Berita Acara Pemeriksaan (BAP)" --> FormBAP["Buka Formulir Konfigurasi Dokumen Berita Acara (BAP)"]
    FormBAP --> InputBAP["Input Nomor BAP Otomatis, Tanggal Pemeriksaan, Pihak Pertama (Galangan), Pihak Kedua (Owner/BKI), dan Catatan Evaluasi"]
    InputBAP --> GenerateLembarBAP["Sistem Membentuk Lembar BAP Resmi dengan Standar Kop, Klausul Hukum, dan Kolom Tanda Tangan"]
    GenerateLembarBAP --> PratinjauCetak["Tampilkan Pratinjau Lembar BAP di Antarmuka Web"]
    PratinjauCetak --> CetakDokumen["Pengguna Menekan 'Ctrl + P' / Cetak Browser (CSS Khusus @media print Aktif Otomatis Mengisolasi Lembar BAP)"]
    CetakDokumen --> DokumenFisik(["Dokumen BAP Tercetak Resmi / Disimpan sebagai File PDF A4"])
```

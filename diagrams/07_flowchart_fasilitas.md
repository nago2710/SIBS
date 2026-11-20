# Diagram 4.7: Flowchart Departemen Manajemen Fasilitas & Peralatan

### Deskripsi untuk Bab 4:
> **Gambar 4.7 Diagram Alir Manajemen Fasilitas, Pemeliharaan, dan Utilisasi Alat Berat**  
> Menggambarkan tata kelola kesiapan fasilitas perkapalan (*shipyard heavy equipment & dock facilities*). Meliputi pemantauan status operasional dan masa berlaku sertifikasi K3, alur pengajuan dan penanganan perawatan (*Preventive / Corrective Maintenance*), pencatatan jam/hari pemakaian alat (*facility utilization*), serta pembebanan biaya harian fasilitas ke pos anggaran pembangunan kapal.

```mermaid
flowchart TD
    Start(["Mulai Manajemen Fasilitas"]) --> TinjauFasilitas["Buka Master Fasilitas Galangan (Tabel 'fasilitas')"]
    TinjauFasilitas --> MonitoringKondisi["Monitoring Status Kesiapan (Operasional / Ready / Rusak) dan Sertifikasi K3"]

    MonitoringKondisi --> IdentifikasiKebutuhan{"Pilih Alur Operasional Fasilitas"}

    %% CABANG 1: PERAWATAN & MAINTENANCE
    IdentifikasiKebutuhan -- "Pengajuan Pemeliharaan (Maintenance)" --> FormReqMaint["Buka Formulir Pengajuan Perawatan Fasilitas"]
    FormReqMaint --> InputDataMaint["Pilih Fasilitas (ID), Jenis Perawatan (Preventive/Repair/Overhaul), Estimasi Biaya, dan Deskripsi Keluhan"]
    InputDataMaint --> SimpanReqMaint["Simpan Permintaan Perawatan (Tabel 'fasilitas_maintenance', Status: 'diajukan')"]
    
    SimpanReqMaint --> PelaksanaanPerbaikan["Teknisi Melaksanakan Perbaikan & Kalibrasi Alat Berat"]
    PelaksanaanPerbaikan --> UpdateStatusPekerjaan["Ubah Status Maintenance: 'disetujui' -> 'sedang_dikerjakan' -> 'selesai'"]
    UpdateStatusPekerjaan --> UpdateStatusFasilitas["Kembalikan Status Fasilitas menjadi 'Operasional' (Tabel 'fasilitas')"]
    UpdateStatusFasilitas --> SelesaiMaint(["Fasilitas Siap Digunakan Kembali"])

    %% CABANG 2: PENCATATAN PENGGUNAAN & BIAYA
    IdentifikasiKebutuhan -- "Pencatatan Utilisasi Alat untuk Proyek" --> FormUtilisasi["Buka Formulir Pencatatan Penggunaan Fasilitas"]
    FormUtilisasi --> InputUtilisasi["Pilih Fasilitas, Proyek Aktif (NB-002), Tanggal Mulai-Selesai, dan Durasi Jam/Hari"]
    InputUtilisasi --> HitungBiaya["Hitung Pembebanan Biaya: Total Biaya = Durasi x Biaya Sewa Harian Fasilitas"]
    
    HitungBiaya --> SimpanUtilisasi["Simpan Data Pemakaian (Tabel 'fasilitas_usage')"]
    SimpanUtilisasi --> AgregasiBiaya["Integrasikan Biaya Fasilitas ke Modul Biaya Eksekutif"]
    AgregasiBiaya --> SelesaiUtilisasi(["Biaya Fasilitas Terbebankan ke Proyek"])
```

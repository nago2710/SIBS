# Diagram 4.2: Flowchart Departemen Desain & Perencanaan Produksi

### Deskripsi untuk Bab 4:
> **Gambar 4.2 Diagram Alir Proses Perencanaan Desain, Blok Lambung, dan PWBS**  
> Menggambarkan tahapan teknis departemen perencanaan dimulai dari input spesifikasi dimensi utama kapal, verifikasi koefisien bentuk badan kapal (*hydrostatic & form coefficients*), pembagian blok lambung (*block division*), perincian struktur hierarki PWBS (*Product Work Breakdown Structure*), serta pengendalian status persetujuan gambar kerja (*Drawing Register*).

```mermaid
flowchart TD
    Start(["Mulai Proses Perencanaan"]) --> InputDimensi["Input Spesifikasi & Dimensi Utama Kapal (LOA, LBP, B, H, T, GT, Vs)"]
    InputDimensi --> InputCoeff["Input Koefisien Bentuk Lambung (Cb, Cm, Cw, Cp)"]
    InputCoeff --> SimpanKapal["Simpan / Update Master Data Kapal ke Database (Tabel 'kapal')"]
    
    SimpanKapal --> DefinisikanBlok["Definisikan Pembagian Blok Konstruksi Lambung (Contoh: HS-04, HS-06)"]
    DefinisikanBlok --> InputBlok["Input Estimasi Berat (Ton), Status Blok, dan Lokasi Erection"]
    InputBlok --> SimpanBlok["Simpan Data Blok ke Database (Tabel 'blok')"]

    SimpanBlok --> BreakdownPWBS["Lakukan Breakdown Hirarki PWBS (Product Work Breakdown Structure)"]
    BreakdownPWBS --> LevelPWBS["Tentukan Level Kodifikasi (Level 1: Kapal, Level 2: Blok, Level 3: Sub-Blok, Level 4: Part/Piece)"]
    LevelPWBS --> InputPWBSItem["Input Detail Kode PWBS, Deskripsi Komponen, Estimasi Kuantitas & Satuan"]
    InputPWBSItem --> SimpanPWBS["Simpan Elemen PWBS ke Database (Tabel 'pwbs_detail')"]

    SimpanPWBS --> DrawingCheck["Review Drawing Register & Status Gambar Kerja"]
    DrawingCheck --> EvaluasiGambar{"Apakah Gambar Disetujui BKI & Owner?"}
    
    EvaluasiGambar -- "Tidak (Perlu Revisi)" --> RevisiGambar["Lakukan Revisi Teknis Desain Gambar Kerja (R1/R2)"]
    RevisiGambar --> DrawingCheck

    EvaluasiGambar -- "Ya (Approved)" --> RilisProduksi["Rilis Dokumen Desain & Struktur Blok ke Departemen Produksi"]
    RilisProduksi --> Selesai(["Selesai / Terintegrasi ke Jadwal Produksi"])
```

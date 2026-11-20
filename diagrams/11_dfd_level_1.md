# Diagram 4.11: Data Flow Diagram (DFD) Level 1 Dekomposisi Sistem

### Deskripsi untuk Bab 4:
> **Gambar 4.11 Data Flow Diagram (DFD) Level 1 Dekomposisi Proses SIBS**  
> Menguraikan proses utama pada DFD Level 0 menjadi 7 sub-proses modular fungsional, serta memperlihatkan interaksi aliran data dua arah dengan tabel data store di Supabase PostgreSQL.

```mermaid
flowchart TD
    %% SUB-PROSES
    P1(("1.0 Pengelolaan Desain & PWBS"))
    P2(("2.0 Pelaksanaan & Pengendalian Produksi"))
    P3(("3.0 Pengadaan & Purchase Order"))
    P4(("4.0 Pengendalian Mutu QA/QC"))
    P5(("5.0 Manajemen Inventori Gudang"))
    P6(("6.0 Manajemen Fasilitas & Pemeliharaan"))
    P7(("7.0 Agregasi Eksekutif & Penerbitan BAP"))

    %% DATA STORES
    DS_Kapal[("DS-1: kapal & blok")]
    DS_PWBS[("DS-2: pwbs_detail")]
    DS_Jadwal[("DS-3: schedule_detail")]
    DS_Produksi[("DS-4: produksi_data")]
    DS_Vendor[("DS-5: supplier & po")]
    DS_Gudang[("DS-6: gudang_barang & mutasi")]
    DS_Req[("DS-7: permintaan_material")]
    DS_QC[("DS-8: inspeksi_qc")]
    DS_Fasilitas[("DS-9: fasilitas & usage")]

    %% ALIRAN DATA P1
    P1 <--> DS_Kapal
    P1 <--> DS_PWBS
    P1 --> DS_Jadwal

    %% ALIRAN DATA P2
    P2 <--> DS_Jadwal
    P2 --> DS_Produksi
    P2 --> DS_Req

    %% ALIRAN DATA P3
    P3 <--> DS_Vendor
    P3 --> DS_Gudang

    %% ALIRAN DATA P4
    P4 <--> DS_QC
    P4 --> DS_Produksi

    %% ALIRAN DATA P5
    P5 <--> DS_Gudang
    P5 <--> DS_Req

    %% ALIRAN DATA P6
    P6 <--> DS_Fasilitas

    %% ALIRAN DATA P7
    DS_Kapal --> P7
    DS_Jadwal --> P7
    DS_QC --> P7
    DS_Gudang --> P7
    DS_Fasilitas --> P7
    DS_Vendor --> P7
```

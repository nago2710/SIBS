# Diagram 4.9: Cross-Functional Flowchart (Swimlane Diagram) Integrasi 7 Departemen

### Deskripsi untuk Bab 4:
> **Gambar 4.9 Diagram Alir Lintas Departemen (Cross-Functional Swimlane Diagram)**  
> Menggambarkan keterkaitan koordinasi proses bisnis secara horizontal antara ke-7 unit kerja galangan kapal (Perencanaan, Pembelian, Gudang, Produksi, Fasilitas, QA/QC, dan Eksekutif) dalam satu siklus pembangunan blok lambung kapal dari penetapan desain hingga penerbitan Berita Acara Pemeriksaan (BAP).

```mermaid
flowchart LR
    subgraph PERENCANAAN["1. PERENCANAAN & DESAIN"]
        p1["Input Dimensi Kapal & PWBS Blok"] --> p2["Rilis Gambar Kerja & Jadwal WBS"]
    end

    subgraph PEMBELIAN["2. PEMBELIAN & LOGISTIK"]
        b1["Terima Rencana Material / Alert Stok"] --> b2["Terbitkan Purchase Order ke Rekanan"]
        b2 --> b3["Kirim Material ke Galangan"]
    end

    subgraph GUDANG["3. MATERIAL & GUDANG"]
        w1["Terima & Catat Material Masuk (Mutasi In)"]
        w2{"Verifikasi Permintaan Material Produksi"}
        w3["Keluarkan Material & Kurangi Stok (Mutasi Out)"]
    end

    subgraph FASILITAS["4. MANAJEMEN FASILITAS"]
        f1["Siapkan Crane & Mesin Plasma Cutting"]
        f2["Catat Utilisasi & Biaya Fasilitas Proyek"]
    end

    subgraph PRODUKSI["5. PRODUKSI LAPANGAN"]
        pr1["Ajukan Requisition Material ke Gudang"]
        pr2["Lakukan Pemotongan Pelat & Pengelasan Frame"]
        pr3["Ajukan Permohonan Uji NDT / Visual"]
        pr4["Update Persentase Progres Fisik (%)"]
    end

    subgraph QAQC["6. QUALITY CONTROL (QA/QC)"]
        q1["Uji Berdasarkan 39 Standar BKI"]
        q2{"Evaluasi Hasil Uji"}
        q3["Approve & Dokumentasikan Mutu"]
        q4["Reject (Perintah Remedial Work)"]
    end

    subgraph EKSEKUTIF["7. MANAJEMEN EKSEKUTIF"]
        e1["Pantau Kurva S & Rekapitulasi Biaya"]
        e2["Verifikasi Lapangan Bersama Owner / BKI"]
        e3["Penerbitan & Cetak Berita Acara (BAP)"]
    end

    %% ALUR RELASI ANTAR DEPARTEMEN (HORIZONTAL FLOW)
    p2 --> b1
    p2 --> pr1
    b3 --> w1
    pr1 --> w2
    w2 -- "Disetujui" --> w3
    w3 --> pr2
    f1 --> pr2
    pr2 --> f2
    pr2 --> pr3
    pr3 --> q1
    q1 --> q2
    q2 -- "Memenuhi Syarat" --> q3
    q2 -- "Tidak Memenuhi" --> q4
    q4 --> pr2
    q3 --> pr4
    pr4 --> e1
    f2 --> e1
    e1 --> e2
    e2 --> e3
```

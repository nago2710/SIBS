# Diagram 4.12: Entity Relationship Diagram (ERD) Database Supabase

### Deskripsi untuk Bab 4:
> **Gambar 4.12 Entity Relationship Diagram (ERD) Basis Data SIBS**  
> Memperlihatkan struktur tabel relasional, atribut kunci (*Primary Key & Foreign Key*), tipe data, dan derajat relasi (*cardinality*) antar entitas pada basis data Supabase PostgreSQL.

```mermaid
erDiagram
    users {
        int id PK
        varchar username UK
        text password_hash
        varchar nama_lengkap
        varchar role
        varchar departemen
        boolean is_active
        timestamp created_at
    }

    kapal {
        varchar id_project PK
        varchar nama_kapal
        varchar tipe_kapal
        varchar pemilik
        varchar galangan
        varchar kelas
        numeric gt
        numeric loa
        numeric lwl
        numeric lbp
        numeric b
        numeric h
        numeric t
        numeric vs
        numeric cb
        numeric cm
        numeric cw
        numeric cp
    }

    blok {
        int id PK
        varchar id_project FK
        varchar id_blok
        varchar nama_blok
        numeric berat_ton
        varchar status
        varchar lokasi_erection
    }

    pwbs_detail {
        int id PK
        varchar id_project FK
        varchar id_blok FK
        varchar kode_pwbs
        text deskripsi
        int level
        varchar parent_kode
        numeric estimasi_qty
        varchar satuan
    }

    schedule_detail {
        int id PK
        varchar id_project FK
        varchar no_urut
        varchar pekerjaan
        date tanggal_mulai
        date tanggal_selesai
        int durasi_hari
        numeric bobot_persen
        numeric progress
    }

    produksi_data {
        int id PK
        varchar id_project FK
        varchar item_kode
        varchar frame_no
        varchar jenis_pekerjaan
        numeric berat_kg
        numeric panjang_las_m
        varchar mesin_alat
        varchar operator
        varchar status
        date tanggal
    }

    gudang_barang {
        varchar id_barang PK
        varchar nama_barang
        varchar kategori
        varchar jenis_gudang
        varchar lokasi_rak
        numeric stok_current
        numeric stok_minimum
        varchar satuan
        numeric harga_satuan
    }

    gudang_mutasi {
        int id PK
        varchar id_barang FK
        varchar tipe
        numeric jumlah
        varchar referensi
        text keterangan
        varchar created_by
        timestamp tanggal
    }

    permintaan_material {
        int id PK
        varchar id_project FK
        varchar id_barang FK
        varchar id_blok
        numeric jumlah
        varchar prioritas
        varchar status
        varchar requested_by
        varchar approved_by
        timestamp tanggal_request
    }

    inspeksi_qc {
        int id PK
        varchar id_project FK
        varchar kategori
        varchar id_blok
        varchar komponen
        varchar metode_uji
        varchar status
        varchar inspektur
        date tanggal_inspeksi
        varchar approved_by
    }

    supplier {
        int id PK
        varchar nama
        varchar kategori
        varchar kontak
        varchar telepon
        varchar email
        text alamat
        boolean is_active
    }

    purchase_order {
        int id PK
        varchar no_po UK
        varchar id_project FK
        varchar supplier
        numeric total_nilai
        varchar status
        date tanggal
        date target_kedatangan
        varchar created_by
        varchar approved_by
    }

    fasilitas {
        varchar id_fasilitas PK
        varchar nama_fasilitas
        varchar kategori
        varchar kapasitas
        varchar daya_listrik
        varchar lokasi
        numeric biaya_harian
        varchar status
        varchar status_sertifikasi
    }

    fasilitas_maintenance {
        int id PK
        varchar id_fasilitas FK
        varchar jenis_perawatan
        text deskripsi
        numeric estimasi_biaya
        varchar status
        date tanggal_request
        varchar requested_by
    }

    fasilitas_usage {
        int id PK
        varchar id_project FK
        varchar id_fasilitas FK
        date tanggal_mulai
        date tanggal_selesai
        numeric durasi
        numeric total_biaya
        varchar operator
    }

    audit_log {
        int id PK
        varchar username
        varchar action
        varchar target_table
        varchar target_id
        text keterangan
        timestamp created_at
    }

    %% RELATIONSHIPS
    kapal ||--o{ blok : "memiliki"
    kapal ||--o{ schedule_detail : "dijadwalkan"
    kapal ||--o{ produksi_data : "dikerjakan"
    kapal ||--o{ permintaan_material : "meminta"
    kapal ||--o{ inspeksi_qc : "diinspeksi"
    kapal ||--o{ purchase_order : "didanai"
    kapal ||--o{ fasilitas_usage : "menggunakan"

    blok ||--o{ pwbs_detail : "dibagi_menjadi"
    gudang_barang ||--o{ gudang_mutasi : "bermutasi"
    gudang_barang ||--o{ permintaan_material : "dikeluarkan_untuk"
    fasilitas ||--o{ fasilitas_maintenance : "diservis"
    fasilitas ||--o{ fasilitas_usage : "dipakai_pada"
```

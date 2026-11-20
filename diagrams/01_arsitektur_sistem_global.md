# Diagram 4.1: Arsitektur Global Sistem Terintegrasi Galangan Kapal (SIBS)

### Deskripsi untuk Bab 4:
> **Gambar 4.1 Arsitektur Sistem Terintegrasi SIBS (Shipyard Integrated Business System)**  
> Mengilustrasikan arsitektur sistem berlapis (*layered architecture*) yang menghubungkan antarmuka pengguna (*Frontend Presentation Layer*), modul logika bisnis 7 departemen (*Application & Business Logic Layer*), lapisan keamanan dan otentikasi (*Security & RBAC Layer*), serta lapisan basis data terpusat berbasis cloud (*Cloud Database Layer*) menggunakan Supabase PostgreSQL.

```mermaid
flowchart TD
    subgraph UI["1. LAPISAN PRESENTASI (STREAMLIT USER INTERFACE)"]
        Landing["Halaman Muka (Landing Page) & Portal Informasi"]
        Login["Portal Otentikasi & Validasi Kredensial Multi-Role"]
        Sidebar["Sidebar Navigasi & Pemilih Proyek Kapal Aktif"]
        PrintView["Modul Cetak Dokumen Resmi BAP (Print-Ready CSS)"]
    end

    subgraph Security["2. LAPISAN KEAMANAN & OTENTIKASI (AUTH & RBAC)"]
        PBKDF2["Enkripsi Password PBKDF2-SHA256 (100k Iterasi + Salt)"]
        Throttling["Anti-Brute Force Login Throttling"]
        RBAC["Role-Based Access Control (7 Hak Akses Departemen)"]
        Audit["Audit Logging (Pencatatan Jejak Aktivitas Sistem)"]
    end

    subgraph Business["3. LAPISAN LOGIKA BISNIS 7 DEPARTEMEN (SIBS DEPARTMENTS)"]
        D1["Perencanaan & Desain (Dimensi, Blok, PWBS, Drawing)"]
        D2["Produksi Lapangan (Jadwal WBS, Cutting, Welding, Requisition)"]
        D3["Pembelian & Logistik (Supplier, Purchase Order, PO Tracking)"]
        D4["QA / QC (39 Standar BKI, NDT, Approval, Remedial Work)"]
        D5["Gudang & Material (Master Stok, Mutasi Masuk/Keluar, Alert)"]
        D6["Fasilitas Galangan (Alat Berat, Maintenance, Utilisasi Biaya)"]
        D7["Eksekutif & BAP (Dashboard KPI, Kurva S, Rekap Biaya, BAP)"]
    end

    subgraph DB["4. LAPISAN BASIS DATA CLOUD (SUPABASE POSTGRESQL)"]
        T_Users[("users & audit_log")]
        T_Ship[("kapal, blok, pwbs_detail")]
        T_Prod[("schedule_detail, produksi_data, pekerja")]
        T_Logistik[("supplier, purchase_order, purchase_order_item")]
        T_Warehouse[("gudang_barang, gudang_mutasi, permintaan_material")]
        T_Quality[("inspeksi_qc (39 Kategori BKI)")]
        T_Facility[("fasilitas, fasilitas_maintenance, fasilitas_usage")]
    end

    UI --> Security
    Security --> Business
    Business <--> DB

    D1 <--> T_Ship
    D2 <--> T_Prod
    D2 <--> T_Warehouse
    D3 <--> T_Logistik
    D4 <--> T_Quality
    D5 <--> T_Warehouse
    D6 <--> T_Facility
    D7 <--> T_Ship
    D7 <--> T_Prod
    D7 <--> T_Warehouse
    D7 <--> T_Quality
    Security <--> T_Users
```

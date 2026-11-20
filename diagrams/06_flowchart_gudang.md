# Diagram 4.6: Flowchart Departemen Material & Gudang

### Deskripsi untuk Bab 4:
> **Gambar 4.6 Diagram Alir Pengelolaan Inventaris Material dan Mutasi Stok Gudang**  
> Mengilustrasikan pengelolaan siklus hidup material konstruksi kapal di gudang galangan (gudang terbuka/tertutup). Meliputi penerimaan barang masuk dari rekanan logistik, penempatan rak/yard, pemantauan saldo stok terkini secara dinamis, verifikasi dan pengeluaran fisik berdasarkan permintaan produksi, serta otomatisasi pemicu peringatan stok minimum (*Low-Stock Alert*).

```mermaid
flowchart TD
    Start(["Mulai Pengelolaan Material & Gudang"]) --> IdentifikasiAktivitas{"Pilih Jenis Aktivitas Gudang"}

    %% CABANG 1: PENERIMAAN MATERIAL MASUK
    IdentifikasiAktivitas -- "Penerimaan Material Masuk (PO/Vendor)" --> CekSuratJalan["Periksa Surat Jalan, Faktur, dan Fisik Material dari Logistik"]
    CekSuratJalan --> CekMasterBarang{"Apakah Barang Sudah Ada di Master Stok?"}
    
    CekMasterBarang -- "Belum Ada" --> InputMaster["Input Kode Barang (SKU), Nama, Kategori, Jenis Gudang, Rak, dan Satuan"]
    InputMaster --> SimpanMaster["Simpan ke Master Inventaris (Tabel 'gudang_barang')"]
    SimpanMaster --> FormMutasiMasuk
    
    CekMasterBarang -- "Sudah Ada" --> FormMutasiMasuk["Buka Formulir Mutasi Barang Masuk"]

    FormMutasiMasuk --> InputMutasiMasuk["Input ID Barang, Kuantitas Masuk, Nomor Referensi (PO/SJ), dan Lokasi Rak"]
    InputMutasiMasuk --> EksekusiMutasiMasuk["Proses Mutasi Masuk (Tabel 'gudang_mutasi', Tipe: 'masuk')"]
    EksekusiMutasiMasuk --> UpdateStokTambah["Sistem Otomatis Menambah Stok: stok_current = stok_current + jumlah"]
    UpdateStokTambah --> SelesaiMasuk(["Material Resmi Tersimpan di Gudang"])

    %% CABANG 2: PENGELUARAN UNTUK PRODUKSI
    IdentifikasiAktivitas -- "Pengeluaran Material (Permintaan Produksi)" --> CekPermintaanPending["Buka Tab 'Persetujuan Permintaan Produksi' (Tabel 'permintaan_material', Status: 'pending')"]
    CekPermintaanPending --> ReviewKebutuhan["Verifikasi ID Barang, Jumlah yang Diminta, Blok Tujuan, dan Prioritas"]
    
    ReviewKebutuhan --> CekKetersediaan{"Apakah Stok Fisik di Gudang Mencukupi?"}
    
    CekKetersediaan -- "Tidak Cukup" --> TolakReq["Klik 'Tolak Permintaan' dengan Catatan: Stok Tidak Mencukupi"]
    TolakReq --> NotifLogistik["Kirim Peringatan ke Departemen Pembelian untuk Pengadaan Baru"]
    NotifLogistik --> SelesaiTolak(["Permintaan Ditolak"])

    CekKetersediaan -- "Cukup" --> SetujuiReq["Klik 'Setujui & Keluarkan Barang'"]
    SetujuiReq --> EksekusiMutasiKeluar["Proses Mutasi Keluar Otomatis (Tabel 'gudang_mutasi', Tipe: 'keluar')"]
    EksekusiMutasiKeluar --> UpdateStokKurang["Sistem Otomatis Mengurangi Stok: stok_current = stok_current - jumlah"]
    UpdateStokKurang --> UpdateReqStatus["Ubah Status Permintaan Material menjadi 'Approved'"]
    UpdateReqStatus --> SerahkanBarang["Fisik Material Diserahkan ke Tim Fabrikasi Lapangan"]

    %% CEK PERINGATAN STOK MINIMUM
    UpdateStokKurang --> CekBatasMinimum{"Apakah stok_current <= stok_minimum?"}
    CekBatasMinimum -- "Ya (Stok Kritis)" --> TriggerAlert["Aktifkan Indikator Low-Stock Alert Merah di Dashboard Gudang & Eksekutif"]
    CekBatasMinimum -- "Tidak (Aman)" --> SelesaiKeluar(["Selesai / Stok Terupdate"])
    TriggerAlert --> SelesaiKeluar
```

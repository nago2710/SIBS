"""
SIBS: Shipyard Integrated Business System
Seed Data Script — Sesuai Skema Tabel Supabase (schema.sql)
"""

import os
import sys
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()

from config import supabase_config, DEFAULT_USERS, QC_CATEGORIES
from auth import hash_password
from database import db_manager


def seed_all():
    print("=" * 60)
    print("SIBS — PENGISIAN DATA AWAL (SEED DATA)")
    print("=" * 60)

    if not db_manager.is_connected:
        print("❌ Supabase belum terhubung!")
        return False

    # 1. USERS
    print("\n1. Mengisi data Pengguna (Users)...")
    for u in DEFAULT_USERS:
        username, raw_pw, nama, role, dept = u
        existing = db_manager.get_user_by_username(username)
        if not existing:
            user_data = {
                "username": username,
                "password_hash": hash_password(raw_pw),
                "nama_lengkap": nama,
                "role": role,
                "departemen": dept,
                "is_active": True,
            }
            ok = db_manager.create_user(user_data)
            print(f"   [+] User '{username}' ({role}) created: {ok}")
        else:
            print(f"   [i] User '{username}' sudah ada.")

    # 2. KAPAL
    print("\n2. Mengisi data Kapal...")
    ships = [
        {
            "id_project": "NB-002",
            "nama_kapal": "KM. NUSANTARA",
            "type_kapal": "Ferry Ro-Ro",
            "kecepatan": 15.0,
            "gt": 750.0,
            "loa": 70.0,
            "lwl": 68.0,
            "lbp": 65.0,
            "b": 14.0,
            "h": 4.8,
            "t": 3.2,
            "cb": 0.70,
            "cm": 0.80,
            "cw": 0.80,
            "cp": 0.70,
            "status": "active",
        },
        {
            "id_project": "NB-001",
            "nama_kapal": "KM. LAKAAN",
            "type_kapal": "Ferry Ro-Ro",
            "kecepatan": 14.0,
            "gt": 750.0,
            "loa": 65.0,
            "lwl": 62.0,
            "lbp": 60.0,
            "b": 12.0,
            "h": 4.5,
            "t": 3.0,
            "cb": 0.68,
            "cm": 0.78,
            "cw": 0.78,
            "cp": 0.68,
            "status": "active",
        }
    ]
    for s in ships:
        try:
            db_manager.client.table("kapal").upsert(s, on_conflict="id_project").execute()
            print(f"   [+] Kapal '{s['nama_kapal']}': Berhasil")
        except Exception as e:
            print(f"   [-] Kapal '{s['nama_kapal']}' error: {e}")

    # 3. BLOK
    print("\n3. Mengisi data Blok Lambung...")
    blocks = [
        {"id_project": "NB-002", "id_blok": "HS-04", "nama_blok": "Hull Structure Block 04", "level": "Sub-Assembly", "jumlah_sub_blok": 5, "total_berat": 45.5},
        {"id_project": "NB-002", "id_blok": "HS-06", "nama_blok": "Hull Structure Block 06", "level": "Sub-Assembly", "jumlah_sub_blok": 5, "total_berat": 52.8},
    ]
    for b in blocks:
        try:
            db_manager.client.table("blok").upsert(b, on_conflict="id_project,id_blok").execute()
            print(f"   [+] Blok '{b['id_blok']}': Berhasil")
        except Exception as e:
            print(f"   [-] Blok '{b['id_blok']}' error: {e}")

    # 4. PWBS DETAIL
    print("\n4. Mengisi data PWBS...")
    pwbs_items = [
        {"id_project": "NB-002", "id_blok": "HS-06", "kode": "HS-06-PL-01", "nama_panel": "Bottom Panel", "nama_material": "Pelat Baja Grade A 10mm", "jenis_material": "Pelat", "jumlah": 6, "berat": 12.5},
        {"id_project": "NB-002", "id_blok": "HS-06", "kode": "HS-06-PL-02", "nama_panel": "Side Shell Starboard", "nama_material": "Pelat Baja Grade A 10mm", "jenis_material": "Pelat", "jumlah": 4, "berat": 8.5},
        {"id_project": "NB-002", "id_blok": "HS-06", "kode": "HS-06-PL-03", "nama_panel": "Side Shell Portside", "nama_material": "Pelat Baja Grade A 10mm", "jenis_material": "Pelat", "jumlah": 4, "berat": 8.5},
        {"id_project": "NB-002", "id_blok": "HS-06", "kode": "HS-06-DK-01", "nama_panel": "Vehicle Deck Panel", "nama_material": "Pelat Baja Grade A 12mm", "jenis_material": "Pelat", "jumlah": 8, "berat": 16.0},
        {"id_project": "NB-002", "id_blok": "HS-06", "kode": "HS-06-FR-01", "nama_panel": "Floor & Web Frame", "nama_material": "Profil Siku L 100x100x10", "jenis_material": "Profil", "jumlah": 18, "berat": 7.3},
    ]
    for p in pwbs_items:
        try:
            db_manager.client.table("pwbs_detail").insert(p).execute()
            print(f"   [+] PWBS '{p['kode']}': Berhasil")
        except Exception as e:
            print(f"   [-] PWBS '{p['kode']}' error: {e}")

    # 5. JADWAL PERAKITAN / SCHEDULE
    print("\n5. Mengisi data Jadwal Perakitan...")
    schedules = [
        {"id_project": "NB-002", "no_urut": "1", "nama_pekerjaan": "Pembangunan Panel Deck", "tanggal_mulai": "2025-01-10", "tanggal_selesai": "2025-01-22", "progress": 100.0},
        {"id_project": "NB-002", "no_urut": "2", "nama_pekerjaan": "Pembangunan Panel Bottom", "tanggal_mulai": "2025-01-15", "tanggal_selesai": "2025-02-02", "progress": 90.0},
        {"id_project": "NB-002", "no_urut": "3", "nama_pekerjaan": "Pembangunan Panel Sisi SB (Starboard)", "tanggal_mulai": "2025-01-22", "tanggal_selesai": "2025-02-12", "progress": 75.0},
        {"id_project": "NB-002", "no_urut": "4", "nama_pekerjaan": "Pembangunan Panel Sisi PS (Portside)", "tanggal_mulai": "2025-01-24", "tanggal_selesai": "2025-02-14", "progress": 70.0},
        {"id_project": "NB-002", "no_urut": "5", "nama_pekerjaan": "Assembly Bottom + Sisi", "tanggal_mulai": "2025-02-15", "tanggal_selesai": "2025-03-02", "progress": 40.0},
        {"id_project": "NB-002", "no_urut": "6", "nama_pekerjaan": "Assembly Deck Panel", "tanggal_mulai": "2025-02-28", "tanggal_selesai": "2025-03-12", "progress": 15.0},
        {"id_project": "NB-002", "no_urut": "7", "nama_pekerjaan": "Finishing, Blasting Sa 2.5 & Painting", "tanggal_mulai": "2025-03-05", "tanggal_selesai": "2025-03-18", "progress": 0.0},
    ]
    for sc in schedules:
        try:
            db_manager.client.table("schedule_detail").insert(sc).execute()
            print(f"   [+] Schedule #{sc['no_urut']} ({sc['nama_pekerjaan']}): Berhasil")
        except Exception as e:
            print(f"   [-] Schedule error: {e}")

    # 6. GUDANG BARANG (Master Stok)
    print("\n6. Mengisi Master Data Stok Gudang...")
    items = [
        {"id_barang": "MAT-PL-10", "nama_barang": "Pelat Baja BKI Grade A 10mm", "jenis": "Pelat Baja", "satuan": "LEMBAR", "stok_current": 42.0, "stok_minimum": 15.0, "lokasi_rak": "Yard Plate Area A", "jenis_gudang": "terbuka", "spesifikasi": "6000x1500x10mm"},
        {"id_barang": "MAT-PL-12", "nama_barang": "Pelat Baja BKI Grade A 12mm", "jenis": "Pelat Baja", "satuan": "LEMBAR", "stok_current": 28.0, "stok_minimum": 10.0, "lokasi_rak": "Yard Plate Area A", "jenis_gudang": "terbuka", "spesifikasi": "6000x1500x12mm"},
        {"id_barang": "MAT-PR-01", "nama_barang": "Profil Siku L 100x100x10mm", "jenis": "Profil", "satuan": "BATANG", "stok_current": 65.0, "stok_minimum": 20.0, "lokasi_rak": "Yard Profile Area B", "jenis_gudang": "terbuka", "spesifikasi": "L=6m BKI Grade A"},
        {"id_barang": "MAT-LAS-01", "nama_barang": "Kawat Las E7018 Dia 3.2mm", "jenis": "Pengelasan", "satuan": "DUS", "stok_current": 18.0, "stok_minimum": 25.0, "lokasi_rak": "Rak W-02 Consumables", "jenis_gudang": "tertutup", "spesifikasi": "Dus 20kg E7018 Low Hydrogen"},
        {"id_barang": "MAT-LAS-02", "nama_barang": "Kawat Las SAW Dia 4.0mm", "jenis": "Pengelasan", "satuan": "SPOOL", "stok_current": 12.0, "stok_minimum": 8.0, "lokasi_rak": "Rak W-03 Consumables", "jenis_gudang": "tertutup", "spesifikasi": "Spool 25kg SAW Submerged"},
        {"id_barang": "MAT-CAT-01", "nama_barang": "Epoxy Primer Marine Coating", "jenis": "Cat", "satuan": "PAIL", "stok_current": 35.0, "stok_minimum": 15.0, "lokasi_rak": "Rak Paint-01", "jenis_gudang": "tertutup", "spesifikasi": "Pail 20L Anti-Corrosion Primer"},
        {"id_barang": "MAT-CAT-02", "nama_barang": "Polyurethane Finish Top Coat", "jenis": "Cat", "satuan": "PAIL", "stok_current": 8.0, "stok_minimum": 10.0, "lokasi_rak": "Rak Paint-02", "jenis_gudang": "tertutup", "spesifikasi": "Pail 20L Finish Gloss Coat"},
        {"id_barang": "MAT-GAS-01", "nama_barang": "Gas Oksigen O2 Industri", "jenis": "Gas", "satuan": "TABUNG", "stok_current": 50.0, "stok_minimum": 15.0, "lokasi_rak": "Bunker Gas A", "jenis_gudang": "tertutup", "spesifikasi": "Tabung 6m3 150 Bar"},
        {"id_barang": "MAT-GAS-02", "nama_barang": "Gas Acetylene", "jenis": "Gas", "satuan": "TABUNG", "stok_current": 25.0, "stok_minimum": 10.0, "lokasi_rak": "Bunker Gas B", "jenis_gudang": "tertutup", "spesifikasi": "Tabung 40L Dissolved Acetylene"},
    ]
    for it in items:
        try:
            db_manager.client.table("gudang_barang").upsert(it, on_conflict="id_barang").execute()
            print(f"   [+] Barang '{it['nama_barang']}': Berhasil")
        except Exception as e:
            print(f"   [-] Barang error: {e}")

    # 7. SUPPLIER
    print("\n7. Mengisi Master Data Supplier...")
    suppliers = [
        {"nama": "PT Krakatau Steel (Persero) Tbk", "jenis_supply": "Pelat & Profil Baja", "telepon": "0254-391150", "email": "sales@krakatausteel.com", "alamat": "Jl. Industri No. 5, Cilegon, Banten", "is_active": True},
        {"nama": "PT Nippon Paint Indonesia", "jenis_supply": "Cat & Protective Coating", "telepon": "021-6900540", "email": "marine.sales@nipponpaint.co.id", "alamat": "Kawasan Industri Ancol, Jakarta Utara", "is_active": True},
        {"nama": "PT Lincoln Electric Indonesia", "jenis_supply": "Peralatan & Kawat Las", "telepon": "021-8983000", "email": "info@lincolnelectric.co.id", "alamat": "Delta Silicon Industrial Park, Cikarang", "is_active": True},
        {"nama": "PT Samator Gas Industri Tbk", "jenis_supply": "Gas Industri", "telepon": "0411-510200", "email": "makassar@samator.com", "alamat": "Kawasan Industri Makassar (KIMA) Kav. 10", "is_active": True},
        {"nama": "PT Cahaya Samudera Perkasa", "jenis_supply": "Pipa & Outfitting", "telepon": "031-7492200", "email": "sales@cahayasamudera.com", "alamat": "Kawasan Industri Gresik, Jawa Timur", "is_active": True},
    ]
    for sp in suppliers:
        try:
            db_manager.client.table("supplier").insert(sp).execute()
            print(f"   [+] Supplier '{sp['nama']}': Berhasil")
        except Exception as e:
            print(f"   [-] Supplier error: {e}")

    # 8. FASILITAS
    print("\n8. Mengisi Master Data Fasilitas Galangan...")
    facilities = [
        {"id_fasilitas": "FAS-CR-01", "nama_fasilitas": "Gantry Crane 50T", "jenis_fasilitas": "Lifting", "kapasitas": 50.0, "daya": 120.0, "status": "Operasional", "sertifikasi_aktif": True, "biaya_harian": 1500000.0},
        {"id_fasilitas": "FAS-CR-02", "nama_fasilitas": "Overhead Crane 15T", "jenis_fasilitas": "Lifting", "kapasitas": 15.0, "daya": 45.0, "status": "Operasional", "sertifikasi_aktif": True, "biaya_harian": 750000.0},
        {"id_fasilitas": "FAS-CUT-01", "nama_fasilitas": "CNC Plasma Cutting Koike", "jenis_fasilitas": "Cutting", "kapasitas": 32.0, "daya": 30.0, "status": "Operasional", "sertifikasi_aktif": True, "biaya_harian": 600000.0},
        {"id_fasilitas": "FAS-LAS-01", "nama_fasilitas": "Submerged Arc Welding (SAW)", "jenis_fasilitas": "Welding", "kapasitas": 1000.0, "daya": 50.0, "status": "Operasional", "sertifikasi_aktif": True, "biaya_harian": 450000.0},
        {"id_fasilitas": "FAS-CMP-01", "nama_fasilitas": "Air Compressor 250 CFM", "jenis_fasilitas": "Blasting", "kapasitas": 250.0, "daya": 55.0, "status": "Operasional", "sertifikasi_aktif": True, "biaya_harian": 350000.0},
        {"id_fasilitas": "FAS-DCK-01", "nama_fasilitas": "Graving Drydock 5000 DWT", "jenis_fasilitas": "Drydock", "kapasitas": 5000.0, "daya": 250.0, "status": "Operasional", "sertifikasi_aktif": True, "biaya_harian": 5000000.0},
    ]
    for fc in facilities:
        try:
            db_manager.client.table("fasilitas").upsert(fc, on_conflict="id_fasilitas").execute()
            print(f"   [+] Fasilitas '{fc['nama_fasilitas']}': Berhasil")
        except Exception as e:
            print(f"   [-] Fasilitas error: {e}")

    # 9. INSPEKSI QA/QC AWAL
    print("\n9. Mengisi Contoh Data Inspeksi QA/QC...")
    sample_qc = [
        {"id_project": "NB-002", "id_blok": "HS-06", "kategori": "Surface Preparation & Machine Cutting", "item_inspeksi": "Bottom Plate Nesting FR 14-22", "status": "approved", "hasil": "Kualitas bevel cutting Sa 2.5, toleransi +/- 1mm.", "inspector": "Ir. Hendra (BKI Surveyor)", "tanggal_inspeksi": "2025-01-16T08:00:00Z"},
        {"id_project": "NB-002", "id_blok": "HS-06", "kategori": "Welding Qualification", "item_inspeksi": "WPS HS-06 Butt Joint Panel", "status": "approved", "hasil": "WPS approved sesuai standar BKI Rules Part 1.", "inspector": "Rudi Hartono (QC Galangan)", "tanggal_inspeksi": "2025-01-18T08:00:00Z"},
        {"id_project": "NB-002", "id_blok": "HS-06", "kategori": "Structural Testing", "item_inspeksi": "Butt Joint Bottom Plate FR 18", "status": "approved", "hasil": "100% UT lolos, tidak ditemukan lack of fusion atau crack.", "inspector": "Bambang Sutrisno (NDT Level II)", "tanggal_inspeksi": "2025-01-25T08:00:00Z"},
        {"id_project": "NB-002", "id_blok": "HS-06", "kategori": "Welding Surfaces", "item_inspeksi": "Side Shell SB Longitudinal Seam", "status": "rejected", "hasil": "Ditemukan undercut sepanjang 15cm pada frame 19 (Remedial Work).", "inspector": "Rudi Hartono (QC Galangan)", "tanggal_inspeksi": "2025-02-01T08:00:00Z"},
        {"id_project": "NB-002", "id_blok": "HS-06", "kategori": "Tightness Testing", "item_inspeksi": "Double Bottom Tank Top Panel", "status": "pending", "hasil": "Jadwal pengujian vacuum box direncanakan minggu depan.", "inspector": "Ir. Hendra (BKI Surveyor)", "tanggal_inspeksi": "2025-02-15T08:00:00Z"},
    ]
    for qc in sample_qc:
        try:
            db_manager.client.table("inspeksi_qc").insert(qc).execute()
            print(f"   [+] Inspeksi '{qc['kategori']}': Berhasil")
        except Exception as e:
            print(f"   [-] Inspeksi error: {e}")

    print("\n" + "=" * 60)
    print("✅ PENGISIAN SEED DATA SELESAI DENGAN SUKSES!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    seed_all()

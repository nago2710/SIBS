"""
SIBS: Shipyard Integrated Business System
Departemen: Material & Penyimpanan / Gudang (gudang.py)

Tanggung Jawab:
- Pengelolaan master data stok barang gudang (terbuka & tertutup)
- Pencatatan transaksi mutasi masuk (penerimaan PO) dan keluar (alokasi produksi)
- Monitoring batas stok minimum & peringatan stok menipis (low-stock alert)
- Persetujuan dan pengeluaran barang atas permintaan tim produksi
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import db_manager
from utils import (
    render_page_header, render_kpi, status_pill,
    format_currency, format_percentage, format_date,
    show_success, show_error, show_warning, show_info
)


def render(user_info: dict, active_project: str):
    """Render interface Departemen Material & Gudang."""
    render_page_header(
        title="Material & Penyimpanan (Gudang)",
        subtitle="Manajemen Stok Inventaris, Mutasi Masuk/Keluar, dan Persetujuan Pengeluaran Material",
        badge="DEPARTEMEN GUDANG"
    )

    if not db_manager.is_connected:
        st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

    all_barang = db_manager.get_all_barang()
    low_stock = db_manager.get_barang_low_stock()

    # KPI summary
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("TOTAL JENIS MATERIAL", str(len(all_barang)), "SKU terdaftar", "#1E3A8A")
    with c2:
        total_stok = sum(float(b.get("stok_current", 0)) for b in all_barang)
        render_kpi("TOTAL FISIK STOK", f"{int(total_stok):,} Unit", "Akumulasi saldo fisik", "#16A34A")
    with c3:
        render_kpi("PERINGATAN STOK MENIPIS", str(len(low_stock)), "Di bawah batas minimum", "#DC2626" if low_stock else "#16A34A", "#DC2626" if low_stock else "")
    with c4:
        pending_req = db_manager.get_permintaan_material(active_project, status="pending") if active_project else []
        render_kpi("PERMINTAAN PRODUKSI", str(len(pending_req)), "Menunggu pengeluaran", "#D97706")

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    tab_stok, tab_approval, tab_mutasi, tab_master = st.tabs([
        "Master Stok Inventaris",
        "Persetujuan Permintaan Produksi",
        "Mutasi Masuk / Keluar",
        "Tambah / Edit Data Barang"
    ])

    # =========================================================================
    # TAB 1: MASTER STOK INVENTARIS
    # =========================================================================
    with tab_stok:
        st.markdown("### Daftar Inventaris & Stok Material")

        if low_stock:
            st.error(f"[PERINGATAN DEFISIT] Terdapat {len(low_stock)} item material yang berada pada atau di bawah batas minimum!")
            df_low = pd.DataFrame(low_stock)
            cols_l = [c for c in ["id_barang", "nama_barang", "stok_current", "stok_minimum", "satuan", "lokasi_rak"] if c in df_low.columns]
            st.dataframe(df_low[cols_l], use_container_width=True, hide_index=True)

        if all_barang:
            df_b = pd.DataFrame(all_barang)
            cols_show = [c for c in ["id_barang", "nama_barang", "jenis", "jenis_gudang", "lokasi_rak", "stok_current", "stok_minimum", "satuan", "spesifikasi"] if c in df_b.columns]
            st.dataframe(df_b[cols_show], use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data barang di inventaris gudang.")

    # =========================================================================
    # TAB 2: PERSETUJUAN PERMINTAAN PRODUKSI
    # =========================================================================
    with tab_approval:
        st.markdown("### Pengeluaran Material Berdasarkan Permintaan Produksi")
        st.caption("Persetujuan dan pengeluaran fisik barang dari rak gudang ke lapangan perakitan.")

        pending_req = db_manager.get_permintaan_material(active_project, status="pending") if active_project else []

        if pending_req:
            st.markdown("#### Permintaan Menunggu Persetujuan")
            for req in pending_req:
                with st.expander(f"Permintaan #{req.get('id')}: {req.get('id_barang')} ({req.get('jumlah')} {req.get('satuan', 'UNIT')})"):
                    c_a, c_b = st.columns(2)
                    with c_a:
                        st.write(f"**Pemohon:** {req.get('requested_by')}")
                        st.write(f"**Tanggal Request:** {format_date(req.get('tanggal_request'))}")
                    with c_b:
                        st.write(f"**Keperluan:** {req.get('keperluan', '-')}")

                    btn_c1, btn_c2 = st.columns(2)
                    with btn_c1:
                        if st.button(f"Setujui & Keluarkan #{req.get('id')}", key=f"app_{req.get('id')}"):
                            mutasi_ok = db_manager.create_mutasi(
                                id_barang=req.get("id_barang"),
                                tipe="keluar",
                                jumlah=float(req.get("jumlah")),
                                created_by=user_info.get("username", "gudang"),
                                referensi=f"REQ-PROD-#{req.get('id')}",
                                keterangan=f"Pengeluaran material: {req.get('keperluan')}"
                            )
                            if mutasi_ok:
                                db_manager.update_permintaan_status(req["id"], "approved", approved_by=user_info.get("username"))
                                show_success(f"Permintaan #{req.get('id')} disetujui dan stok barang telah dikurangi.")
                                st.rerun()
                            else:
                                show_error("Gagal memproses mutasi stok (mungkin stok fisik tidak mencukupi).")
                    with btn_c2:
                        if st.button(f"Tolak Permintaan #{req.get('id')}", key=f"rej_{req.get('id')}"):
                            db_manager.update_permintaan_status(req["id"], "rejected", approved_by=user_info.get("username"))
                            show_warning(f"Permintaan #{req.get('id')} ditolak.")
                            st.rerun()
        else:
            st.info("[STATUS NORMAL] Tidak ada permintaan material yang menunggu persetujuan.")

    # =========================================================================
    # TAB 3: MUTASI MASUK / KELUAR
    # =========================================================================
    with tab_mutasi:
        st.markdown("### Pencatatan Mutasi Barang Masuk & Keluar")

        with st.form("form_mutasi_manual"):
            c1, c2, c3 = st.columns(3)
            with c1:
                b_opts = {f"{b['id_barang']} - {b['nama_barang']} (Stok: {b.get('stok_current', 0)})": b["id_barang"] for b in all_barang} if all_barang else {}
                if b_opts:
                    sel_b_label = st.selectbox("Pilih Material *:", list(b_opts.keys()))
                    m_id_barang = b_opts[sel_b_label]
                else:
                    m_id_barang = st.text_input("ID Barang *", value="MAT-PL-10")
                
                m_tipe = st.selectbox("Tipe Mutasi *:", ["masuk", "keluar"])
            with c2:
                m_qty = st.number_input("Jumlah Kuantitas *", min_value=0.1, value=10.0, step=1.0)
                m_ref = st.text_input("No. Referensi (PO / Surat Jalan)", value="SJ-2025-001")
            with c3:
                m_ket = st.text_area("Keterangan Mutasi", value="Penerimaan dari rekanan supplier")

            submit_mut = st.form_submit_button("Proses Mutasi Stok")
            if submit_mut:
                ok = db_manager.create_mutasi(
                    id_barang=m_id_barang,
                    tipe=m_tipe,
                    jumlah=m_qty,
                    created_by=user_info.get("username", "gudang"),
                    referensi=m_ref.strip(),
                    keterangan=m_ket.strip()
                )
                if ok:
                    db_manager.log_action(user_info.get("username", "user"), "MUTASI_STOK", "gudang_mutasi", m_id_barang, keterangan=f"Mutasi {m_tipe} {m_qty}")
                    show_success(f"Mutasi {m_tipe} sebanyak {m_qty} berhasil dicatat.")
                    st.rerun()
                else:
                    show_error("Gagal mencatat mutasi stok (periksa ketersediaan stok jika mutasi keluar).")

        st.markdown("---")
        st.markdown("#### Riwayat Transaksi Mutasi Terakhir")
        hist = db_manager.get_mutasi_history(limit=50)
        if hist:
            df_hist = pd.DataFrame(hist)
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada riwayat transaksi mutasi.")

    # =========================================================================
    # TAB 4: TAMBAH / EDIT DATA BARANG
    # =========================================================================
    with tab_master:
        st.markdown("### Master Data Barang & Material")

        with st.form("form_master_barang"):
            c1, c2, c3 = st.columns(3)
            with c1:
                b_code = st.text_input("Kode Barang / SKU * (Contoh: MAT-PL-10)")
                b_nama = st.text_input("Nama Barang * (Contoh: Pelat Baja Marine Grade A 10mm)")
                b_kat = st.selectbox("Jenis Material", ["Pelat Baja", "Profil", "Pengelasan", "Cat", "Gas", "Pipa & Outfitting"])
            with c2:
                b_jenis = st.selectbox("Jenis Gudang", ["terbuka", "tertutup"])
                b_rak = st.text_input("Lokasi Rak / Yard", value="Yard Area A")
                b_satuan = st.text_input("Satuan Pengukuran", value="LEMBAR")
            with c3:
                b_stok_cur = st.number_input("Stok Awal", min_value=0.0, value=50.0, step=1.0)
                b_stok_min = st.number_input("Batas Stok Minimum", min_value=0.0, value=10.0, step=1.0)
                b_spek = st.text_input("Spesifikasi Teknis", value="6000x1500x10mm BKI Grade A")

            submit_b = st.form_submit_button("Simpan Master Data Barang")
            if submit_b:
                if not b_code or not b_nama:
                    show_error("Kode Barang dan Nama Barang wajib diisi.")
                else:
                    payload = {
                        "id_barang": b_code.strip(),
                        "nama_barang": b_nama.strip(),
                        "jenis": b_kat,
                        "jenis_gudang": b_jenis,
                        "lokasi_rak": b_rak.strip(),
                        "satuan": b_satuan.strip(),
                        "stok_current": b_stok_cur,
                        "stok_minimum": b_stok_min,
                        "spesifikasi": b_spek.strip()
                    }
                    ok = db_manager.upsert_barang(payload)
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "UPSERT_BARANG", "gudang_barang", b_code, keterangan=f"Master item {b_nama}")
                        show_success(f"Barang '{b_nama}' ({b_code}) berhasil disimpan.")
                        st.rerun()
                    else:
                        show_error("Gagal menyimpan data barang.")

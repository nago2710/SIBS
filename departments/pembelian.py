"""
SIBS: Shipyard Integrated Business System
Departemen: Pembelian & Logistik (pembelian.py)

Tanggung Jawab:
- Pengelolaan master supplier / vendor perlengkapan galangan
- Pembuatan dan pemantauan Purchase Order (PO)
- Validasi status pesanan (draft, submitted, approved, delivered)
- Koordinasi logistik pengiriman material ke galangan
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
    """Render interface Departemen Pembelian & Logistik."""
    render_page_header(
        title="Pembelian & Logistik",
        subtitle="Manajemen Rekanan Supplier, Pengadaan Material Proyek, dan Purchase Order (PO)",
        badge="DEPARTEMEN PEMBELIAN"
    )

    if not db_manager.is_connected:
        st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

    tab_po, tab_buat_po, tab_supplier = st.tabs([
        "Daftar Purchase Order (PO)",
        "Buat Purchase Order Baru",
        "Master Vendor & Supplier"
    ])

    # =========================================================================
    # TAB 1: DAFTAR PURCHASE ORDER (PO)
    # =========================================================================
    with tab_po:
        st.markdown("### Daftar Pesanan Pembelian (Purchase Orders)")
        
        c_filter1, c_filter2 = st.columns(2)
        with c_filter1:
            filter_status = st.selectbox("Filter Status PO:", ["Semua Status", "draft", "submitted", "approved", "delivered", "cancelled"])
        with c_filter2:
            st.markdown("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)

        status_param = None if filter_status == "Semua Status" else filter_status
        po_list = db_manager.get_purchase_orders(active_project, status=status_param) if active_project else []

        if po_list:
            total_nilai = sum(float(p.get("total_harga", 0)) for p in po_list)
            c1, c2, c3 = st.columns(3)
            with c1:
                render_kpi("TOTAL NILAI PO", format_currency(total_nilai), f"{len(po_list)} Pesanan", "#1E3A8A")
            with c2:
                po_app = sum(1 for p in po_list if p.get("status") in ["approved", "delivered"])
                render_kpi("PO DISETUJUI / TERKIRIM", f"{po_app} / {len(po_list)}", "Status aktif", "#16A34A")
            with c3:
                po_draft = sum(1 for p in po_list if p.get("status") == "draft")
                render_kpi("PO MENUNGGU PERSETUJUAN", str(po_draft), "Perlu tindakan", "#D97706")

            st.markdown("#### Tabel Pesanan")
            df_po = pd.DataFrame(po_list)
            st.dataframe(df_po, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Update Status Purchase Order")
            with st.form("form_update_po"):
                po_options = {f"{p.get('no_po', p.get('id'))} - Rp {float(p.get('total_harga', 0)):,.0f} ({p.get('status')})": p["id"] for p in po_list}
                sel_po_label = st.selectbox("Pilih PO untuk Diubah:", list(po_options.keys()))
                target_po_id = po_options[sel_po_label]

                new_status = st.selectbox("Status Baru:", ["submitted", "approved", "delivered", "cancelled"])
                submit_update = st.form_submit_button("Perbarui Status PO")

                if submit_update:
                    ok = db_manager.update_po_status(target_po_id, new_status, approved_by=user_info.get("username"))
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "UPDATE_PO_STATUS", "purchase_order", str(target_po_id), keterangan=f"Ubah status PO ke {new_status}")
                        show_success(f"Status PO berhasil diubah menjadi '{new_status}'.")
                        st.rerun()
                    else:
                        show_error("Gagal memperbarui status PO.")
        else:
            st.info("Belum ada data Purchase Order untuk proyek ini.")

    # =========================================================================
    # TAB 2: BUAT PURCHASE ORDER BARU
    # =========================================================================
    with tab_buat_po:
        st.markdown("### Penerbitan Purchase Order Baru")
        
        suppliers = db_manager.get_all_supplier()
        sup_dict = {f"{s['nama']} ({s.get('jenis_supply', '')})": s for s in suppliers} if suppliers else {}

        with st.form("form_create_po"):
            c1, c2 = st.columns(2)
            with c1:
                no_po = st.text_input("Nomor PO * (Contoh: PO-2025-NB002-01)")
                if sup_dict:
                    sel_sup_label = st.selectbox("Pilih Supplier / Vendor *:", list(sup_dict.keys()))
                    sel_sup_obj = sup_dict[sel_sup_label]
                    sup_id = sel_sup_obj["id"]
                    sup_nama = sel_sup_obj["nama"]
                else:
                    sup_id = None
                    sup_nama = st.text_input("Nama Supplier *", value="PT Krakatau Steel (Persero) Tbk")
                tgl_po = st.date_input("Tanggal PO", value=date.today())
            with c2:
                total_val = st.number_input("Estimasi Total Nilai (Rp) *", min_value=100000.0, value=25000000.0, step=1000000.0)
                tgl_target = st.date_input("Target Tanggal Kedatangan", value=date.today())
                po_catatan = st.text_area("Syarat & Keterangan Pengiriman", value="FOB Galangan Makassar. Term of Payment: Net 30 hari.")

            submit_create = st.form_submit_button("Terbitkan Purchase Order")
            if submit_create:
                if not no_po:
                    show_error("Nomor PO wajib diisi.")
                else:
                    po_payload = {
                        "no_po": no_po.strip(),
                        "id_supplier": sup_id,
                        "id_project": active_project,
                        "total_harga": total_val,
                        "status": "draft",
                        "tanggal_order": tgl_po.isoformat(),
                        "tanggal_target": tgl_target.isoformat(),
                        "catatan": po_catatan.strip(),
                        "created_by": user_info.get("username", "pembelian")
                    }
                    ok = db_manager.create_purchase_order(po_payload)
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "CREATE_PO", "purchase_order", no_po, keterangan=f"Penerbitan PO {no_po}")
                        show_success(f"Purchase Order {no_po} berhasil diterbitkan dengan status Draft.")
                        st.rerun()
                    else:
                        show_error("Gagal menerbitkan Purchase Order.")

    # =========================================================================
    # TAB 3: MASTER VENDOR & SUPPLIER
    # =========================================================================
    with tab_supplier:
        st.markdown("### Database Supplier Rekanan Galangan")

        suppliers = db_manager.get_all_supplier()
        if suppliers:
            df_sup = pd.DataFrame(suppliers)
            cols = [c for c in ["id", "nama", "jenis_supply", "telepon", "email", "alamat", "is_active"] if c in df_sup.columns]
            st.dataframe(df_sup[cols], use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data supplier terdaftar di database.")

        st.markdown("---")
        st.markdown("#### Tambah Data Supplier Baru")
        with st.form("form_supplier"):
            c1, c2, c3 = st.columns(3)
            with c1:
                s_nama = st.text_input("Nama Perusahaan Supplier *")
                s_kat = st.selectbox("Jenis Pasokan", ["Pelat & Profil Baja", "Cat & Protective Coating", "Peralatan & Kawat Las", "Pipa & Outfitting", "Gas Industri", "Mesin & Fasilitas"])
            with c2:
                s_telp = st.text_input("No. Telepon Perusahaan")
                s_email = st.text_input("Email Resmi")
            with c3:
                s_alamat = st.text_area("Alamat Lengkap Kantor / Gudang", rows=1)

            submit_s = st.form_submit_button("Simpan Data Supplier")
            if submit_s:
                if not s_nama:
                    show_error("Nama perusahaan supplier wajib diisi.")
                else:
                    sup_data = {
                        "nama": s_nama.strip(),
                        "jenis_supply": s_kat,
                        "telepon": s_telp.strip(),
                        "email": s_email.strip(),
                        "alamat": s_alamat.strip(),
                        "is_active": True
                    }
                    ok = db_manager.upsert_supplier(sup_data)
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "UPSERT_SUPPLIER", "supplier", s_nama, keterangan="Update data supplier")
                        show_success(f"Data supplier '{s_nama}' berhasil disimpan.")
                        st.rerun()
                    else:
                        show_error("Gagal menyimpan data supplier.")

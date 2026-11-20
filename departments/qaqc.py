"""
SIBS: Shipyard Integrated Business System
Departemen: Quality Control / Quality Assurance (qaqc.py)

Tanggung Jawab:
- Pelaksanaan inspeksi konstruksi kapal berbasis 39 kategori standar BKI & Owner
- Verifikasi hasil uji las (NDT, visual, mechanical test)
- Manajemen status inspeksi (approved, rejected, pending)
- Pemantauan cacat/reject dan tindakan perbaikan (remedial work)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import db_manager
from config import QC_CATEGORIES
from utils import (
    render_page_header, render_kpi, status_pill,
    format_percentage, format_date,
    show_success, show_error, show_warning, show_info
)


def render(user_info: dict, active_project: str):
    """Render interface Departemen Quality Assurance & Quality Control (QA/QC)."""
    render_page_header(
        title="Quality Control & Assurance (QA/QC)",
        subtitle="Verifikasi Standar Mutu Pembangunan Kapal, Inspeksi Pengelasan, dan Pengujian Struktur",
        badge="DEPARTEMEN QA/QC"
    )

    if not db_manager.is_connected:
        st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

    summary = db_manager.get_inspeksi_summary(active_project) if active_project else {"total": 0, "approved": 0, "rejected": 0, "pending": 0}

    # Summary KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("TOTAL INSPEKSI", str(summary.get("total", 0)), "Seluruh kategori", "#1E3A8A")
    with col2:
        render_kpi("LOLOS / APPROVED", str(summary.get("approved", 0)), "Memenuhi standar BKI", "#16A34A")
    with col3:
        render_kpi("REJECT / DEFECT", str(summary.get("rejected", 0)), "Butuh remedial work", "#DC2626")
    with col4:
        render_kpi("MENUNGGU VERIFIKASI", str(summary.get("pending", 0)), "Belum diapprove", "#D97706")

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    tab_inspeksi, tab_input, tab_reject, tab_kategori = st.tabs([
        "Riwayat Hasil Inspeksi",
        "Catat Inspeksi Baru",
        "Defect & Remedial Work",
        "Katalog 39 Standar Uji BKI"
    ])

    # =========================================================================
    # TAB 1: RIWAYAT HASIL INSPEKSI
    # =========================================================================
    with tab_inspeksi:
        st.markdown("### Daftar Hasil Inspeksi Mutu Proyek")
        
        c_kat, c_stat = st.columns(2)
        with c_kat:
            kat_list = ["Semua Kategori"] + [c["nama"] for c in QC_CATEGORIES]
            sel_kat = st.selectbox("Filter Kategori Uji:", kat_list)
        with c_stat:
            sel_stat = st.selectbox("Filter Status:", ["Semua Status", "approved", "rejected", "pending"])

        kat_param = None if sel_kat == "Semua Kategori" else sel_kat
        inspections = db_manager.get_inspeksi_by_project(active_project, kategori=kat_param) if active_project else []

        if sel_stat != "Semua Status":
            inspections = [i for i in inspections if i.get("status") == sel_stat]

        if inspections:
            df_i = pd.DataFrame(inspections)
            cols_show = [c for c in ["id", "kategori", "id_blok", "item_inspeksi", "hasil", "status", "inspector", "tanggal_inspeksi", "approved_by"] if c in df_i.columns]
            st.dataframe(df_i[cols_show], use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Tindakan Approval Inspeksi")
            with st.form("form_approve_qc"):
                pending_opts = {f"#{i['id']} - {i.get('kategori')} ({i.get('item_inspeksi', '')}) - [{i.get('status')}]": i["id"] for i in inspections}
                sel_item_lbl = st.selectbox("Pilih Record Inspeksi:", list(pending_opts.keys()))
                target_qc_id = pending_opts[sel_item_lbl]

                qc_act = st.selectbox("Ubah Status:", ["approved", "rejected", "pending"])
                submit_qc_act = st.form_submit_button("Simpan Status Inspeksi")

                if submit_qc_act:
                    ok = db_manager.update_inspeksi_status(target_qc_id, qc_act, approved_by=user_info.get("username"))
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "UPDATE_QC_STATUS", "inspeksi_qc", str(target_qc_id), keterangan=f"Ubah status inspeksi ke {qc_act}")
                        show_success(f"Status inspeksi #{target_qc_id} diubah menjadi {qc_act}.")
                        st.rerun()
                    else:
                        show_error("Gagal mengubah status inspeksi.")
        else:
            st.info("Tidak ada data inspeksi yang sesuai dengan filter.")

    # =========================================================================
    # TAB 2: CATAT INSPEKSI BARU
    # =========================================================================
    with tab_input:
        st.markdown("### Formulir Pencatatan Inspeksi QA/QC Baru")

        with st.form("form_new_inspection"):
            c1, c2 = st.columns(2)
            with c1:
                kat_opts = [f"{c['nama']} ({c['grup']})" for c in QC_CATEGORIES]
                sel_cat_full = st.selectbox("Kategori Standar Uji *:", kat_opts)
                cat_nama_clean = sel_cat_full.split(" (")[0]

                bloks = db_manager.get_blok_by_project(active_project) if active_project else []
                b_opts = [b["id_blok"] for b in bloks] if bloks else ["HS-04", "HS-06"]
                target_b = st.selectbox("Blok yang Diinspeksi *:", b_opts)

                komponen = st.text_input("Item / Lokasi Sambungan *", value="Deck Panel Seam FR 20-22")
            with c2:
                hasil_status = st.selectbox("Hasil Evaluasi *:", ["approved", "pending", "rejected"])
                inspektur = st.text_input("Nama Inspektur / Surveyor", value=user_info.get("nama_lengkap", "QC Inspector"))
                tgl_insp = st.date_input("Tanggal Pemeriksaan", value=date.today())
                hasil_text = st.text_area("Deskripsi Hasil & Catatan Teknis", value="Sambungan las rapi, penetrasi penuh, tidak ditemukan cacat porosity atau undercut.")

            submit_new_i = st.form_submit_button("Catat Laporan Inspeksi")
            if submit_new_i:
                if not komponen:
                    show_error("Nama item / lokasi sambungan wajib diisi.")
                else:
                    insp_payload = {
                        "id_project": active_project,
                        "kategori": cat_nama_clean,
                        "id_blok": target_b,
                        "item_inspeksi": komponen.strip(),
                        "status": hasil_status,
                        "hasil": hasil_text.strip(),
                        "inspector": inspektur.strip(),
                        "tanggal_inspeksi": tgl_insp.isoformat() + "T08:00:00Z",
                        "approved_by": user_info.get("username") if hasil_status == "approved" else None
                    }
                    ok = db_manager.create_inspeksi(insp_payload)
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "CREATE_INSPECTION", "inspeksi_qc", cat_nama_clean, keterangan=f"Inspeksi {komponen}: {hasil_status}")
                        show_success("Laporan inspeksi berhasil disimpan.")
                        st.rerun()
                    else:
                        show_error("Gagal menyimpan laporan inspeksi.")

    # =========================================================================
    # TAB 3: DEFECT & REMEDIAL WORK
    # =========================================================================
    with tab_reject:
        st.markdown("### Daftar Defect / Cacat & Tindakan Perbaikan (Remedial Work)")
        all_insp = db_manager.get_inspeksi_by_project(active_project) if active_project else []
        rejects = [i for i in all_insp if i.get("status") == "rejected"]

        if rejects:
            st.warning(f"[CATATAN] Ditemukan {len(rejects)} temuan yang dinyatakan REJECT dan membutuhkan tindakan perbaikan.")
            df_rej = pd.DataFrame(rejects)
            st.dataframe(df_rej, use_container_width=True, hide_index=True)
        else:
            st.info("[STATUS NORMAL] Tidak ada temuan reject aktif. Mutu konstruksi memenuhi standar.")

    # =========================================================================
    # TAB 4: KATALOG 39 STANDAR UJI
    # =========================================================================
    with tab_kategori:
        st.markdown("### Katalog 39 Standar Inspeksi (Biro Klasifikasi Indonesia)")
        st.caption("Standar lengkap pemeriksaan mutu konstruksi kapal dari pemotongan baja hingga peluncuran.")

        df_cat = pd.DataFrame(QC_CATEGORIES)
        st.dataframe(df_cat, use_container_width=True, hide_index=True)

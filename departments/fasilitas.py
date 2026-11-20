"""
SIBS: Shipyard Integrated Business System
Departemen: Manajemen Fasilitas (fasilitas.py)

Tanggung Jawab:
- Master data fasilitas berat galangan (crane, plasma cutting, drydock, mesin las)
- Monitoring status operasional, kesiapan, dan sertifikasi alat
- Pengajuan dan pelacakan permintaan perawatan (maintenance & repair)
- Pencatatan utilisasi fasilitas dan pembebanan biaya harian ke proyek
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
    """Render interface Departemen Fasilitas."""
    render_page_header(
        title="Manajemen Fasilitas & Peralatan",
        subtitle="Pemantauan Kesiapan Operasional, Jadwal Perawatan (Maintenance), dan Utilisasi Alat Galangan",
        badge="DEPARTEMEN FASILITAS"
    )

    if not db_manager.is_connected:
        st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

    all_fasilitas = db_manager.get_all_fasilitas()

    # KPI summary
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("TOTAL FASILITAS", str(len(all_fasilitas)), "Unit terdaftar", "#1E3A8A")
    with c2:
        op_count = sum(1 for f in all_fasilitas if str(f.get("status", "")).lower() in ["operasional", "ready", "active"])
        render_kpi("FASILITAS OPERASIONAL", f"{op_count} / {len(all_fasilitas)}", f"{format_percentage((op_count/len(all_fasilitas))*100) if all_fasilitas else '0%'} Kesiapan", "#16A34A")
    with c3:
        maint_count = sum(1 for f in all_fasilitas if str(f.get("status", "")).lower() in ["maintenance", "rusak", "perbaikan"])
        render_kpi("DALAM PERAWATAN", str(maint_count), "Unit tidak beroperasi", "#DC2626" if maint_count else "#16A34A")
    with c4:
        req_maint = db_manager.get_maintenance_requests()
        pend_maint = sum(1 for m in req_maint if str(m.get("status", "")).lower() in ["diajukan", "pending"])
        render_kpi("REQUEST MAINTENANCE", str(pend_maint), "Menunggu penanganan", "#D97706")

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    tab_daftar, tab_maint, tab_utilisasi, tab_tambah = st.tabs([
        "Status Fasilitas & Kesiapan",
        "Jadwal & Request Perawatan",
        "Pencatatan Utilisasi Alat",
        "Tambah / Perbarui Fasilitas"
    ])

    # =========================================================================
    # TAB 1: STATUS FASILITAS & SERTIFIKASI
    # =========================================================================
    with tab_daftar:
        st.markdown("### Daftar Kesiapan Alat & Fasilitas Galangan")

        if all_fasilitas:
            df_f = pd.DataFrame(all_fasilitas)
            cols_show = [c for c in ["id_fasilitas", "nama_fasilitas", "jenis_fasilitas", "kapasitas", "daya", "status", "sertifikasi_aktif", "biaya_harian"] if c in df_f.columns]
            st.dataframe(df_f[cols_show], use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data fasilitas terdaftar.")

    # =========================================================================
    # TAB 2: JADWAL & REQUEST PERAWATAN
    # =========================================================================
    with tab_maint:
        st.markdown("### Pengajuan & Pelacakan Pemeliharaan (Maintenance)")

        with st.form("form_req_maint"):
            c1, c2, c3 = st.columns(3)
            with c1:
                f_opts = {f"{f['id_fasilitas']} - {f['nama_fasilitas']}": f["id_fasilitas"] for f in all_fasilitas} if all_fasilitas else {}
                if f_opts:
                    sel_f_lbl = st.selectbox("Pilih Fasilitas *:", list(f_opts.keys()))
                    m_id_fas = f_opts[sel_f_lbl]
                else:
                    m_id_fas = st.text_input("ID Fasilitas *", value="FAS-CR-01")
                
                m_jenis = st.selectbox("Jenis Perawatan *:", ["Preventive", "Corrective / Repair", "Overhaul", "Kalibrasi / Uji K3"])
            with c2:
                m_tgl = st.date_input("Tanggal Pelaporan", value=date.today())
            with c3:
                m_keluhan = st.text_area("Deskripsi Keluhan / Komponen yang Diservis *", value="Pengecekan kabel hoist dan pelumasan bearing berkala.")

            submit_m = st.form_submit_button("Ajukan Permintaan Perawatan")
            if submit_m:
                payload = {
                    "id_fasilitas": m_id_fas,
                    "tipe": m_jenis,
                    "deskripsi": m_keluhan.strip(),
                    "tanggal_request": m_tgl.isoformat() + "T08:00:00Z",
                    "status": "pending",
                    "requested_by": user_info.get("username", "fasilitas")
                }
                ok = db_manager.create_maintenance_request(payload)
                if ok:
                    db_manager.log_action(user_info.get("username", "user"), "CREATE_MAINTENANCE", "fasilitas_maintenance", m_id_fas, keterangan=f"Request {m_jenis} untuk {m_id_fas}")
                    show_success(f"Permintaan pemeliharaan untuk {m_id_fas} berhasil dicatat.")
                    st.rerun()
                else:
                    show_error("Gagal mencatat permintaan pemeliharaan.")

        st.markdown("---")
        st.markdown("#### Riwayat Permintaan Perawatan")
        m_list = db_manager.get_maintenance_requests()
        if m_list:
            df_m = pd.DataFrame(m_list)
            st.dataframe(df_m, use_container_width=True, hide_index=True)

            st.markdown("##### Update Status Penanganan")
            with st.form("form_up_maint"):
                m_options = {f"#{m['id']} - {m.get('id_fasilitas')} ({m.get('tipe')}) - Status: {m.get('status')}": m["id"] for m in m_list}
                sel_m_lbl = st.selectbox("Pilih Record Maintenance:", list(m_options.keys()))
                target_m_id = m_options[sel_m_lbl]

                m_status_new = st.selectbox("Status Baru:", ["disetujui", "sedang_dikerjakan", "selesai", "dibatalkan"])
                submit_up_m = st.form_submit_button("Perbarui Status Maintenance")
                if submit_up_m:
                    ok = db_manager.update_maintenance_status(target_m_id, m_status_new)
                    if ok:
                        show_success("Status maintenance berhasil diperbarui.")
                        st.rerun()
                    else:
                        show_error("Gagal memperbarui status maintenance.")
        else:
            st.info("Belum ada riwayat permintaan perawatan.")

    # =========================================================================
    # TAB 3: PENCATATAN UTILISASI ALAT
    # =========================================================================
    with tab_utilisasi:
        st.markdown("### Pencatatan Penggunaan Fasilitas (Alokasi Proyek)")

        with st.form("form_utilisasi"):
            c1, c2, c3 = st.columns(3)
            with c1:
                f_opts = {f"{f['nama_fasilitas']} ({f['id_fasilitas']})": f["id_fasilitas"] for f in all_fasilitas} if all_fasilitas else {}
                if f_opts:
                    sel_u_lbl = st.selectbox("Fasilitas yang Digunakan *:", list(f_opts.keys()))
                    u_id_fas = f_opts[sel_u_lbl]
                else:
                    u_id_fas = st.text_input("ID Fasilitas *", value="FAS-CR-01")
            with c2:
                u_mulai = st.date_input("Tanggal Mulai", value=date.today())
                u_selesai = st.date_input("Tanggal Selesai", value=date.today())
            with c3:
                u_durasi = st.number_input("Durasi Penggunaan (Jam)", min_value=1.0, value=8.0, step=1.0)
                u_biaya = st.number_input("Total Biaya Penggunaan (Rp)", min_value=0.0, value=1500000.0, step=100000.0)

            submit_u = st.form_submit_button("Catat Utilisasi Fasilitas")
            if submit_u:
                payload = {
                    "id_project": active_project,
                    "id_fasilitas": u_id_fas,
                    "tanggal_mulai": u_mulai.isoformat(),
                    "tanggal_selesai": u_selesai.isoformat(),
                    "durasi_jam": u_durasi,
                    "biaya": u_biaya,
                    "keterangan": f"Operator: {user_info.get('nama_lengkap', 'Operator')}"
                }
                ok = db_manager.create_fasilitas_usage(payload)
                if ok:
                    show_success("Pencatatan utilisasi alat berhasil disimpan.")
                    st.rerun()
                else:
                    show_error("Gagal mencatat utilisasi alat.")

        u_history = db_manager.get_fasilitas_usage()
        if u_history:
            st.markdown("#### Riwayat Penggunaan Fasilitas")
            st.dataframe(pd.DataFrame(u_history), use_container_width=True, hide_index=True)

    # =========================================================================
    # TAB 4: TAMBAH / PERBARUI FASILITAS
    # =========================================================================
    with tab_tambah:
        st.markdown("### Master Data Fasilitas")

        with st.form("form_master_fasilitas"):
            c1, c2, c3 = st.columns(3)
            with c1:
                f_id = st.text_input("ID Fasilitas * (Contoh: FAS-CR-01)")
                f_nama = st.text_input("Nama Alat / Fasilitas * (Contoh: Gantry Crane 50T)")
                f_kat = st.selectbox("Jenis Fasilitas", ["Lifting", "Cutting", "Welding", "Drydock", "Blasting", "Transport"])
            with c2:
                f_kap = st.number_input("Kapasitas Teknis (Ton / CFM / Ampere)", min_value=0.0, value=50.0, step=5.0)
                f_daya = st.number_input("Daya Listrik (kW)", min_value=0.0, value=120.0, step=10.0)
            with c3:
                f_biaya = st.number_input("Biaya Sewa / Operasional Harian (Rp)", min_value=0.0, value=1500000.0, step=50000.0)
                f_status = st.selectbox("Status Kesiapan", ["Operasional", "Maintenance", "Rusak", "Standby"])

            submit_f = st.form_submit_button("Simpan Data Fasilitas")
            if submit_f:
                if not f_id or not f_nama:
                    show_error("ID dan Nama Fasilitas wajib diisi.")
                else:
                    f_payload = {
                        "id_fasilitas": f_id.strip(),
                        "nama_fasilitas": f_nama.strip(),
                        "jenis_fasilitas": f_kat,
                        "kapasitas": f_kap,
                        "daya": f_daya,
                        "biaya_harian": f_biaya,
                        "status": f_status,
                        "sertifikasi_aktif": True
                    }
                    ok = db_manager.upsert_fasilitas(f_payload)
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "UPSERT_FASILITAS", "fasilitas", f_id, keterangan=f"Master fasilitas {f_nama}")
                        show_success(f"Fasilitas '{f_nama}' ({f_id}) berhasil disimpan.")
                        st.rerun()
                    else:
                        show_error("Gagal menyimpan data fasilitas.")

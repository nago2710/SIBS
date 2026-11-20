"""
SIBS: Shipyard Integrated Business System
Departemen: Produksi Lapangan (produksi.py)

Tanggung Jawab:
- Monitoring jadwal perakitan blok & update kemajuan fisik per sub-pekerjaan
- Pencatatan data fabrikasi harian (cutting, welding, fit-up, assembly)
- Pengajuan permintaan material ke gudang
- Monitoring alokasi tenaga kerja dan biaya produksi
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import db_manager
from utils import (
    render_page_header, render_kpi, status_pill,
    format_currency, format_percentage, format_date,
    show_success, show_error, show_warning, show_info
)


def render(user_info: dict, active_project: str):
    """Render interface Departemen Produksi Lapangan."""
    render_page_header(
        title="Produksi Lapangan",
        subtitle="Pengendalian Jadwal Perakitan Blok, Fabrikasi Komponen, dan Permintaan Material",
        badge="DEPARTEMEN PRODUKSI"
    )

    if not db_manager.is_connected:
        st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

    tab_jadwal, tab_fabrikasi, tab_permintaan, tab_pekerja = st.tabs([
        "Jadwal & Kemajuan Perakitan",
        "Data Fabrikasi (Cutting/Welding)",
        "Permintaan Material ke Gudang",
        "Alokasi Tenaga Kerja"
    ])

    # =========================================================================
    # TAB 1: JADWAL & KEMAJUAN PERAKITAN
    # =========================================================================
    with tab_jadwal:
        st.markdown("### Jadwal Perakitan Blok & Update Progres Fisik")
        st.caption("Monitoring tahapan perakitan berdasarkan urutan pekerjaan struktural HS-06.")

        schedules = db_manager.get_schedule_by_project(active_project) if active_project else []

        if schedules:
            avg_prog = sum(float(s.get("progress", 0)) for s in schedules) / len(schedules)

            c1, c2, c3 = st.columns(3)
            with c1:
                render_kpi("KEMAJUAN FISIK KESELURUHAN", format_percentage(avg_prog), "Rata-rata tahapan WBS", "#16A34A")
            with c2:
                render_kpi("TOTAL ITEM PEKERJAAN", str(len(schedules)), "Item dalam WBS jadwal", "#1E3A8A")
            with c3:
                selesai_count = sum(1 for s in schedules if float(s.get("progress", 0)) >= 100.0)
                render_kpi("PEKERJAAN SELESAI", f"{selesai_count} / {len(schedules)}", f"{format_percentage((selesai_count/len(schedules))*100)} rampung", "#0284C7")

            st.markdown("#### Tabel Jadwal & Progres")
            df_sch = pd.DataFrame(schedules)
            cols_show = [c for c in ["id", "no_urut", "nama_pekerjaan", "tanggal_mulai", "tanggal_selesai", "progress"] if c in df_sch.columns]
            st.dataframe(df_sch[cols_show], use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Update Progres Sub-Pekerjaan")
            with st.form("form_update_progress"):
                options_dict = {f"{s.get('no_urut')} - {s.get('nama_pekerjaan')} (Saat ini: {s.get('progress', 0)}%)": s["id"] for s in schedules}
                sel_label = st.selectbox("Pilih Pekerjaan untuk Diperbarui:", list(options_dict.keys()))
                sel_id = options_dict[sel_label]

                curr_prog = next((float(s.get("progress", 0)) for s in schedules if s["id"] == sel_id), 0.0)
                new_prog = st.slider("Persentase Selesai Baru (%)", min_value=0.0, max_value=100.0, value=curr_prog, step=1.0)

                submit_prog = st.form_submit_button("Perbarui Progres Pekerjaan")
                if submit_prog:
                    ok = db_manager.update_schedule_progress(sel_id, new_prog)
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "UPDATE_PROGRESS", "schedule_detail", str(sel_id), keterangan=f"Update progress ke {new_prog}%")
                        show_success("Progres pekerjaan berhasil diperbarui.")
                        st.rerun()
                    else:
                        show_error("Gagal memperbarui progres.")
        else:
            st.info("Belum ada data jadwal perakitan untuk proyek ini.")

    # =========================================================================
    # TAB 2: DATA FABRIKASI (CUTTING/WELDING)
    # =========================================================================
    with tab_fabrikasi:
        st.markdown("### Log Produksi Fabrikasi Komponen")
        st.caption("Pencatatan pemotongan pelat, perakitan panel, dan pengelasan komponen per frame.")

        prod_data = db_manager.get_produksi_by_project(active_project) if active_project else []

        if prod_data:
            df_p = pd.DataFrame(prod_data)
            st.dataframe(df_p, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada catatan fabrikasi untuk proyek ini.")

        st.markdown("---")
        st.markdown("#### Catat Aktivitas Fabrikasi Baru")
        with st.form("form_tambah_fabrikasi"):
            c1, c2, c3 = st.columns(3)
            with c1:
                p_item = st.text_input("ID Item * (Contoh: PROD-HS06-01)")
                p_kode_part = st.text_input("Kode Part * (Contoh: P-HS06-012)")
                p_nama_part = st.text_input("Nama Part * (Contoh: Bottom Plate Seam FR 18-20)")
            with c2:
                p_berat = st.number_input("Berat Part (kg)", min_value=0.0, value=120.0, step=10.0)
                p_berat_las = st.number_input("Estimasi Berat Lasan (kg)", min_value=0.0, value=4.5, step=0.5)
            with c3:
                p_status = st.selectbox("Status Hasil", ["planned", "in_progress", "completed", "rework"])
                p_tanggal = st.date_input("Tanggal Pelaksanaan", value=datetime.today())

            submit_fab = st.form_submit_button("Simpan Catatan Fabrikasi")
            if submit_fab:
                if not p_item or not p_kode_part:
                    show_error("ID Item dan Kode Part wajib diisi.")
                else:
                    new_item = {
                        "id_project": active_project,
                        "id_item": p_item.strip(),
                        "kode_part": p_kode_part.strip(),
                        "nama_part": p_nama_part.strip(),
                        "berat_part": p_berat,
                        "berat_las": p_berat_las,
                        "status": p_status,
                        "tanggal": p_tanggal.isoformat()
                    }
                    ok = db_manager.insert_produksi(new_item)
                    if ok:
                        show_success(f"Aktivitas {p_kode_part} berhasil dicatat.")
                        st.rerun()
                    else:
                        show_error("Gagal mencatat aktivitas fabrikasi.")

    # =========================================================================
    # TAB 3: PERMINTAAN MATERIAL KE GUDANG
    # =========================================================================
    with tab_permintaan:
        st.markdown("### Pengajuan Permintaan Material ke Gudang (Material Requisition)")
        st.caption("Bagian produksi mengajukan pengeluaran material fisik ke bagian gudang.")

        with st.form("form_req_material"):
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                all_barang = db_manager.get_all_barang()
                b_opts = {f"{b['id_barang']} - {b['nama_barang']} (Stok: {b.get('stok_current', 0)} {b.get('satuan', '')})": b for b in all_barang} if all_barang else {}
                if b_opts:
                    sel_b_label = st.selectbox("Pilih Material di Gudang *:", list(b_opts.keys()))
                    sel_b_obj = b_opts[sel_b_label]
                    sel_id_barang = sel_b_obj["id_barang"]
                    sel_nama_barang = sel_b_obj["nama_barang"]
                    sel_satuan = sel_b_obj.get("satuan", "unit")
                else:
                    sel_id_barang = st.text_input("ID Barang *", value="MAT-PL-10")
                    sel_nama_barang = st.text_input("Nama Barang", value="Pelat Baja Grade A 10mm")
                    sel_satuan = "LEMBAR"
                
                req_qty = st.number_input("Jumlah Diminta *", min_value=1.0, value=5.0, step=1.0)
            with col_m2:
                req_satuan = st.text_input("Satuan", value=sel_satuan)
                bloks = db_manager.get_blok_by_project(active_project) if active_project else []
                b_list = [b["id_blok"] for b in bloks] if bloks else ["HS-04", "HS-06"]
                req_blok = st.selectbox("Untuk Blok Target:", b_list)
            with col_m3:
                req_keperluan = st.text_area("Keperluan / Keterangan Penggunaan:", value="Kebutuhan Bottom Plate Frame 14-20")

            submit_req = st.form_submit_button("Kirim Permintaan Material")
            if submit_req:
                req_payload = {
                    "id_project": active_project,
                    "id_barang": sel_id_barang,
                    "nama_barang": sel_nama_barang,
                    "jumlah": req_qty,
                    "satuan": req_satuan,
                    "keperluan": f"[Blok {req_blok}] {req_keperluan.strip()}",
                    "requested_by": user_info.get("username", "produksi"),
                    "status": "pending"
                }
                ok = db_manager.create_permintaan_material(req_payload)
                if ok:
                    db_manager.log_action(user_info.get("username", "user"), "REQUEST_MATERIAL", "permintaan_material", sel_id_barang, keterangan=f"Permintaan {req_qty} {req_satuan} untuk {req_blok}")
                    show_success(f"Permintaan material {sel_id_barang} berhasil diajukan ke Gudang.")
                    st.rerun()
                else:
                    show_error("Gagal mengajukan permintaan material.")

        st.markdown("---")
        st.markdown("#### Riwayat Permintaan Material Proyek Ini")
        req_list = db_manager.get_permintaan_material(active_project) if active_project else []
        if req_list:
            df_req = pd.DataFrame(req_list)
            st.dataframe(df_req, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada riwayat permintaan material untuk proyek ini.")

    # =========================================================================
    # TAB 4: ALOKASI TENAGA KERJA
    # =========================================================================
    with tab_pekerja:
        st.markdown("### Daftar Tenaga Kerja & Alokasi Lapangan")
        pekerja_list = db_manager.get_pekerja_by_project(active_project) if active_project else []
        if not pekerja_list:
            pekerja_list = db_manager.get_all_pekerja()

        if pekerja_list:
            df_pek = pd.DataFrame(pekerja_list)
            st.dataframe(df_pek, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pekerja terdaftar.")

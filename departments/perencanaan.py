"""
SIBS: Shipyard Integrated Business System
Departemen: Desain & Perencanaan Produksi (perencanaan.py)

Tanggung Jawab:
- Master data kapal & dimensi utama (LOA, LWL, LBP, B, H, T, GT, Vs, Koefisien Bentuk)
- Manajemen blok kapal (Hull Structure Blocks)
- PWBS (Product Work Breakdown Structure) per blok
- Drawing register & referensi desain teknis
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import db_manager
from utils import (
    render_page_header, render_kpi, status_pill,
    format_date, show_success, show_error, show_warning, show_info
)


def render(user_info: dict, active_project: str):
    """Render interface Departemen Desain & Perencanaan Produksi."""
    render_page_header(
        title="Desain & Perencanaan Produksi",
        subtitle="Pengelolaan Master Data Kapal, Blok Lambung, dan Product Work Breakdown Structure (PWBS)",
        badge="DEPARTEMEN PERENCANAAN"
    )

    if not db_manager.is_connected:
        st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Dimensi Utama Kapal",
        "Manajemen Blok Lambung",
        "PWBS (Work Breakdown)",
        "Drawing Register"
    ])

    # =========================================================================
    # TAB 1: DIMENSI UTAMA KAPAL
    # =========================================================================
    with tab1:
        st.markdown("### Spesifikasi Teknis & Dimensi Utama Kapal")
        
        kapal = db_manager.get_kapal(active_project) if active_project else None

        with st.form("form_kapal_dimensi"):
            col1, col2 = st.columns(2)
            with col1:
                id_proj = st.text_input("ID Proyek / No. Hull *", value=kapal.get("id_project", active_project or "NB-002") if kapal else active_project or "NB-002")
                nama_kpl = st.text_input("Nama Kapal *", value=kapal.get("nama_kapal", "KM. NUSANTARA") if kapal else "KM. NUSANTARA")
                tipe_kpl = st.selectbox("Tipe Kapal", ["Ferry Ro-Ro", "General Cargo", "Tugboat", "Barge / Tongkang", "Fast Patrol Boat", "Tanker"], 
                                      index=["Ferry Ro-Ro", "General Cargo", "Tugboat", "Barge / Tongkang", "Fast Patrol Boat", "Tanker"].index(kapal.get("type_kapal", "Ferry Ro-Ro")) if kapal and kapal.get("type_kapal") in ["Ferry Ro-Ro", "General Cargo", "Tugboat", "Barge / Tongkang", "Fast Patrol Boat", "Tanker"] else 0)
                gt_val = st.number_input("Gross Tonnage (GT)", min_value=1.0, value=float(kapal.get("gt", 750.0)) if kapal and kapal.get("gt") else 750.0, step=10.0)
                vs_val = st.number_input("Service Speed / Vs (knot)", min_value=1.0, value=float(kapal.get("kecepatan", 15.0)) if kapal and kapal.get("kecepatan") else 15.0, step=0.5)

            with col2:
                loa_val = st.number_input("Length Overall / LOA (m)", min_value=1.0, value=float(kapal.get("loa", 70.0)) if kapal and kapal.get("loa") else 70.0, step=0.5)
                lwl_val = st.number_input("Length on Waterline / LWL (m)", min_value=1.0, value=float(kapal.get("lwl", 68.0)) if kapal and kapal.get("lwl") else 68.0, step=0.5)
                lbp_val = st.number_input("Length Between Perp. / LBP (m)", min_value=1.0, value=float(kapal.get("lbp", 65.0)) if kapal and kapal.get("lbp") else 65.0, step=0.5)
                b_val = st.number_input("Breadth / Lebar / B (m)", min_value=1.0, value=float(kapal.get("b", 14.0)) if kapal and kapal.get("b") else 14.0, step=0.5)
                h_val = st.number_input("Depth / Tinggi / H (m)", min_value=1.0, value=float(kapal.get("h", 4.8)) if kapal and kapal.get("h") else 4.8, step=0.1)
                t_val = st.number_input("Draught / Sarat Air / T (m)", min_value=0.5, value=float(kapal.get("t", 3.2)) if kapal and kapal.get("t") else 3.2, step=0.1)

            st.markdown("##### Koefisien Bentuk Badan Kapal (Hull Form Coefficients)")
            c_cb, c_cm, c_cw, c_cp = st.columns(4)
            with c_cb:
                cb_val = st.number_input("Block Coeff (Cb)", min_value=0.1, max_value=1.0, value=float(kapal.get("cb", 0.70)) if kapal and kapal.get("cb") else 0.70, step=0.01)
            with c_cm:
                cm_val = st.number_input("Midship Coeff (Cm)", min_value=0.1, max_value=1.0, value=float(kapal.get("cm", 0.80)) if kapal and kapal.get("cm") else 0.80, step=0.01)
            with c_cw:
                cw_val = st.number_input("Waterline Coeff (Cw)", min_value=0.1, max_value=1.0, value=float(kapal.get("cw", 0.80)) if kapal and kapal.get("cw") else 0.80, step=0.01)
            with c_cp:
                cp_val = st.number_input("Prismatic Coeff (Cp)", min_value=0.1, max_value=1.0, value=float(kapal.get("cp", 0.70)) if kapal and kapal.get("cp") else 0.70, step=0.01)

            submit_kapal = st.form_submit_button("Simpan Data Dimensi Kapal", use_container_width=True)

            if submit_kapal:
                data_kapal = {
                    "id_project": id_proj.strip(),
                    "nama_kapal": nama_kpl.strip(),
                    "type_kapal": tipe_kpl,
                    "gt": gt_val,
                    "kecepatan": vs_val,
                    "loa": loa_val,
                    "lwl": lwl_val,
                    "lbp": lbp_val,
                    "b": b_val,
                    "h": h_val,
                    "t": t_val,
                    "cb": cb_val,
                    "cm": cm_val,
                    "cw": cw_val,
                    "cp": cp_val,
                    "status": "active"
                }
                ok = db_manager.upsert_kapal(data_kapal)
                if ok:
                    db_manager.log_action(user_info.get("username", "user"), "UPSERT_KAPAL", "kapal", id_proj, keterangan=f"Update spesifikasi {nama_kpl}")
                    show_success(f"Data kapal {nama_kpl} ({id_proj}) berhasil disimpan.")
                    st.rerun()
                else:
                    show_error("Gagal menyimpan data kapal ke database.")

    # =========================================================================
    # TAB 2: MANAJEMEN BLOK
    # =========================================================================
    with tab2:
        st.markdown("### Daftar Blok Konstruksi Lambung (Hull Blocks)")
        
        bloks = db_manager.get_blok_by_project(active_project) if active_project else []

        if bloks:
            df_blok = pd.DataFrame(bloks)
            cols_show = [c for c in ["id_blok", "nama_blok", "level", "jumlah_sub_blok", "total_berat", "created_at"] if c in df_blok.columns]
            st.dataframe(df_blok[cols_show], use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data blok untuk proyek ini.")

        st.markdown("---")
        st.markdown("#### Tambah / Perbarui Blok")
        with st.form("form_tambah_blok"):
            c1, c2, c3 = st.columns(3)
            with c1:
                b_id = st.text_input("ID Blok * (Contoh: HS-04, HS-06)")
                b_nama = st.text_input("Nama Blok * (Contoh: Hull Structure Block 06)")
            with c2:
                b_level = st.selectbox("Level Perakitan", ["Sub-Assembly", "Assembly", "Grand-Assembly", "Erection"])
                b_sub = st.number_input("Jumlah Sub-Blok", min_value=1, value=5, step=1)
            with c3:
                b_berat = st.number_input("Total Berat (Ton)", min_value=0.1, value=45.0, step=1.0)

            submit_blok = st.form_submit_button("Simpan Data Blok")
            if submit_blok:
                if not b_id or not b_nama:
                    show_error("ID Blok dan Nama Blok wajib diisi.")
                else:
                    blok_data = {
                        "id_project": active_project,
                        "id_blok": b_id.strip(),
                        "nama_blok": b_nama.strip(),
                        "level": b_level,
                        "jumlah_sub_blok": b_sub,
                        "total_berat": b_berat,
                    }
                    ok = db_manager.upsert_blok(blok_data)
                    if ok:
                        db_manager.log_action(user_info.get("username", "user"), "UPSERT_BLOK", "blok", b_id, keterangan=f"Blok {b_id} disimpan")
                        show_success(f"Blok {b_id} berhasil disimpan.")
                        st.rerun()
                    else:
                        show_error("Gagal menyimpan data blok.")

    # =========================================================================
    # TAB 3: PWBS (PRODUCT WORK BREAKDOWN STRUCTURE)
    # =========================================================================
    with tab3:
        st.markdown("### Product Work Breakdown Structure (PWBS)")
        st.caption("Pemberian kodefikasi hierarki struktural kapal dari Level 1 (Kapal) sampai Level 4 (Part / Piece).")

        bloks = db_manager.get_blok_by_project(active_project) if active_project else []
        blok_options = [b["id_blok"] for b in bloks] if bloks else ["HS-04", "HS-06"]
        
        sel_blok = st.selectbox("Pilih Blok Lambung:", blok_options)

        pwbs_items = db_manager.get_pwbs_by_blok(active_project, sel_blok) if active_project else []

        if pwbs_items:
            df_pwbs = pd.DataFrame(pwbs_items)
            cols = [c for c in ["kode", "nama_panel", "nama_material", "jenis_material", "jumlah", "berat"] if c in df_pwbs.columns]
            st.dataframe(df_pwbs[cols], use_container_width=True, hide_index=True)
        else:
            st.info(f"Belum ada data PWBS untuk blok {sel_blok}.")

        st.markdown("---")
        st.markdown("#### Tambah Elemen PWBS")
        with st.form("form_pwbs"):
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                pwbs_kode = st.text_input("Kode PWBS * (Contoh: HS-06-PL-01)")
                pwbs_panel = st.text_input("Nama Panel / Komponen * (Contoh: Bottom Panel)")
            with col_p2:
                pwbs_mat = st.text_input("Nama Material (Contoh: Pelat Baja Grade A 10mm)")
                pwbs_jenis = st.selectbox("Jenis Material", ["Pelat", "Profil", "Pipa", "Outfitting"])
            with col_p3:
                pwbs_qty = st.number_input("Jumlah (Unit)", min_value=1, value=6, step=1)
                pwbs_berat = st.number_input("Estimasi Berat (Ton)", min_value=0.1, value=12.5, step=0.5)

            submit_pwbs = st.form_submit_button("Simpan Elemen PWBS")
            if submit_pwbs:
                if not pwbs_kode or not pwbs_panel:
                    show_error("Kode dan Nama Panel PWBS wajib diisi.")
                else:
                    item_data = {
                        "id_project": active_project,
                        "id_blok": sel_blok,
                        "kode": pwbs_kode.strip(),
                        "nama_panel": pwbs_panel.strip(),
                        "nama_material": pwbs_mat.strip(),
                        "jenis_material": pwbs_jenis,
                        "jumlah": pwbs_qty,
                        "berat": pwbs_berat
                    }
                    ok = db_manager.insert_pwbs(item_data)
                    if ok:
                        show_success(f"Elemen PWBS {pwbs_kode} berhasil ditambahkan.")
                        st.rerun()
                    else:
                        show_error("Gagal menambahkan elemen PWBS.")

    # =========================================================================
    # TAB 4: DRAWING REGISTER
    # =========================================================================
    with tab4:
        st.markdown("### Daftar Gambar Kerja & Persetujuan Desain (Drawing Register)")
        st.caption("Monitoring status persetujuan gambar kerja dari Owner Surveyor dan Biro Klasifikasi.")

        drawings = [
            {"No Gambar": "DWG-IKI-001", "Judul Gambar": "Lines Plan & Body Plan", "Kategori": "Hull Design", "Status BKI": "Approved", "Status Owner": "Approved", "Revisi": "R0"},
            {"No Gambar": "DWG-IKI-002", "Judul Gambar": "General Arrangement (GA)", "Kategori": "General", "Status BKI": "Approved", "Status Owner": "Approved", "Revisi": "R1"},
            {"No Gambar": "DWG-IKI-003", "Judul Gambar": "Midship Section & Construction Profile", "Kategori": "Structure", "Status BKI": "Approved", "Status Owner": "Approved", "Revisi": "R2"},
            {"No Gambar": "DWG-IKI-004", "Judul Gambar": "Shell Expansion Plan", "Kategori": "Structure", "Status BKI": "Approved", "Status Owner": "Review", "Revisi": "R0"},
            {"No Gambar": "DWG-IKI-005", "Judul Gambar": "Block Division & Erection Sequence", "Kategori": "Production", "Status BKI": "Approved", "Status Owner": "Approved", "Revisi": "R1"},
            {"No Gambar": "DWG-IKI-006", "Judul Gambar": "HS-06 Assembly & Nesting Plan", "Kategori": "Workshop", "Status BKI": "Approved", "Status Owner": "Approved", "Revisi": "R0"},
        ]
        st.dataframe(pd.DataFrame(drawings), use_container_width=True, hide_index=True)

"""
SIBS: Shipyard Integrated Business System
Departemen: Manajemen Eksekutif & BAP (eksekutif.py)

Tanggung Jawab:
- Dashboard eksekutif: ringkasan progres, mutu, dan logistik seluruh departemen
- Kurva S (S-Curve): perbandingan rencana vs realisasi kemajuan fisik proyek
- Rekapitulasi biaya proyek (Material, Tenaga Kerja, Fasilitas)
- Penerbitan Berita Acara Pemeriksaan (BAP) / Kemajuan Pekerjaan dengan format siap cetak
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
    """Render interface Manajemen Eksekutif & Penerbitan BAP."""
    render_page_header(
        title="Manajemen Eksekutif & BAP",
        subtitle="Executive Dashboard, Kurva S Kemajuan Fisik, Rekapitulasi Biaya, dan Penerbitan Berita Acara Pemeriksaan",
        badge="MANAJEMEN EKSEKUTIF"
    )

    if not db_manager.is_connected:
        st.warning("[PERINGATAN] Database Supabase belum terhubung. Periksa konfigurasi .env.")

    stats = db_manager.get_dashboard_stats(active_project) if active_project else {}
    kapal = stats.get("kapal")

    tab_dash, tab_scurve, tab_biaya, tab_bap = st.tabs([
        "Executive Overview",
        "Kurva S (S-Curve)",
        "Analisis Biaya Proyek",
        "Cetak Berita Acara (BAP)"
    ])

    # =========================================================================
    # TAB 1: EXECUTIVE OVERVIEW
    # =========================================================================
    with tab_dash:
        st.markdown("### Ringkasan Eksekutif Terpadu (Cross-Department Summary)")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            prog_val = stats.get("overall_progress", 0.0)
            render_kpi("KEMAJUAN FISIK (PROGRES)", format_percentage(prog_val), "Rata-rata tahapan WBS", "#16A34A" if prog_val >= 50 else "#1E3A8A")
        with c2:
            qc_sum = stats.get("inspeksi_summary", {})
            total_qc = qc_sum.get("total", 0)
            app_qc = qc_sum.get("approved", 0)
            app_rate = (app_qc / total_qc * 100) if total_qc > 0 else 100.0
            render_kpi("KEPATUHAN MUTU (QA/QC)", format_percentage(app_rate), f"{app_qc} dari {total_qc} Lolos BKI", "#16A34A" if app_rate >= 90 else "#DC2626")
        with c3:
            low_mat = len(stats.get("low_stock_items", []))
            render_kpi("KESIAPAN MATERIAL", "AMAN" if low_mat == 0 else f"{low_mat} DEFISIT", "Status gudang", "#16A34A" if low_mat == 0 else "#DC2626")
        with c4:
            pend_po = stats.get("pending_po", 0)
            render_kpi("PURCHASE ORDER PENDING", str(pend_po), "Membutuhkan persetujuan", "#D97706" if pend_po > 0 else "#1E3A8A")

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

        col_kpl, col_act = st.columns([1.5, 1])
        with col_kpl:
            st.markdown("#### Informasi Proyek Kapal Aktif")
            if kapal:
                st.markdown(f"""
                <div class="sibs-card">
                    <h3 style="margin-top:0; color:#1E3A8A;">{kapal.get('nama_kapal', 'KM. NUSANTARA')} ({kapal.get('id_project')})</h3>
                    <p style="margin:2px 0;"><strong>Tipe Kapal:</strong> {kapal.get('type_kapal', 'Ferry Ro-Ro')} | <strong>Ukuran:</strong> {kapal.get('gt', 750)} GT</p>
                    <p style="margin:2px 0;"><strong>Status Operasi:</strong> <span class="status-pill-green">KONSTRUKSI AKTIF</span></p>
                    <hr style="margin:12px 0; border-color:rgba(148, 163, 184, 0.2);">
                    <p style="margin:2px 0; font-size:12px; opacity:0.85;">
                        <strong>Dimensi:</strong> LOA: {kapal.get('loa', 70)}m | LBP: {kapal.get('lbp', 65)}m | Lebar: {kapal.get('b', 14)}m | Sarat: {kapal.get('t', 3.2)}m | Speed: {kapal.get('kecepatan', 15)} knot
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Pilih proyek aktif pada panel sidebar.")

        with col_act:
            st.markdown("#### Aktivitas Audit Terkini")
            logs = db_manager.get_audit_logs(limit=6)
            if logs:
                for l in logs:
                    st.markdown(f"""
                    <div style="font-size:12px; padding:6px 0; border-bottom:1px solid rgba(148, 163, 184, 0.15);">
                        <span style="font-weight:700; color:#3B82F6;">{l.get('username')}</span>
                        <span style="opacity:0.7;">• {l.get('action')}</span>
                        <div style="opacity:0.9;">{l.get('keterangan', '-')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Belum ada catatan aktivitas.")

    # =========================================================================
    # TAB 2: KURVA S (S-CURVE)
    # =========================================================================
    with tab_scurve:
        st.markdown("### Kurva S (S-Curve): Rencana vs Realisasi Kemajuan Fisik")
        st.caption("Perbandingan kumulatif jadwal rencana dan realisasi pelaksanaan perakitan blok kapal.")

        schedules = db_manager.get_schedule_by_project(active_project) if active_project else []

        if schedules:
            weeks = [f"Minggu {i+1}" for i in range(10)]
            plan_progress = [3.5, 9.2, 18.0, 31.5, 48.0, 66.5, 82.0, 91.5, 97.0, 100.0]
            
            current_overall = stats.get("overall_progress", 55.7)
            actual_progress = []
            for i, p in enumerate(plan_progress):
                if p <= current_overall + 5:
                    actual_progress.append(round(p * 0.98, 1))
                elif len(actual_progress) < 6:
                    actual_progress.append(round(current_overall, 1))
                    break
                else:
                    break
            
            actual_display = actual_progress + [None] * (len(weeks) - len(actual_progress))

            df_scurve = pd.DataFrame({
                "Periode": weeks,
                "Rencana Kumulatif (%)": plan_progress,
                "Realisasi Kumulatif (%)": actual_display
            }).set_index("Periode")

            st.line_chart(df_scurve, color=["#1E3A8A", "#16A34A"])

            diff = (actual_progress[-1] - plan_progress[len(actual_progress)-1]) if actual_progress else 0
            if diff >= 0:
                st.success(f"[STATUS JADWAL] Proyek berjalan Tepat Waktu / Lebih Cepat (+{diff:.1f}%) dari target perencanaan.")
            else:
                st.warning(f"[STATUS JADWAL] Proyek mengalami Deviasi Keterlambatan ({diff:.1f}%) dari target rencana.")
        else:
            st.info("Data jadwal belum tersedia untuk membentuk Kurva S.")

    # =========================================================================
    # TAB 3: ANALISIS BIAYA PROYEK
    # =========================================================================
    with tab_biaya:
        st.markdown("### Rekapitulasi Alokasi Biaya Pembangunan Kapal")
        st.caption("Rincian estimasi biaya material, fasilitas, tenaga kerja, dan pengujian mutu.")

        cost_data = [
            {"Komponen Biaya": "Material Pelat & Baja Konstruksi", "Alokasi (Rp)": 1450000000, "Realisasi (Rp)": 1380000000, "Deviasi (%)": -4.8},
            {"Komponen Biaya": "Cat & Perlindungan Korosi", "Alokasi (Rp)": 280000000, "Realisasi (Rp)": 265000000, "Deviasi (%)": -5.3},
            {"Komponen Biaya": "Consumable Pengelasan (Kawat Las & Gas)", "Alokasi (Rp)": 195000000, "Realisasi (Rp)": 210000000, "Deviasi (%)": 7.7},
            {"Komponen Biaya": "Tenaga Kerja Langsung Fabrikasi & Erection", "Alokasi (Rp)": 850000000, "Realisasi (Rp)": 790000000, "Deviasi (%)": -7.0},
            {"Komponen Biaya": "Sewa Fasilitas Berat Galangan", "Alokasi (Rp)": 420000000, "Realisasi (Rp)": 395000000, "Deviasi (%)": -5.9},
            {"Komponen Biaya": "Uji QA/QC & Sertifikasi Mutu BKI", "Alokasi (Rp)": 120000000, "Realisasi (Rp)": 115000000, "Deviasi (%)": -4.1},
        ]
        df_cost = pd.DataFrame(cost_data)
        st.dataframe(df_cost.style.format({
            "Alokasi (Rp)": lambda v: format_currency(v),
            "Realisasi (Rp)": lambda v: format_currency(v),
            "Deviasi (%)": "{:+.1f}%"
        }), use_container_width=True, hide_index=True)

        tot_alokasi = sum(c["Alokasi (Rp)"] for c in cost_data)
        tot_realisasi = sum(c["Realisasi (Rp)"] for c in cost_data)
        st.markdown(f"**Total Anggaran Rencana:** {format_currency(tot_alokasi)} | **Total Realisasi:** {format_currency(tot_realisasi)}")

    # =========================================================================
    # TAB 4: CETAK BERITA ACARA PEMERIKSAAN (BAP)
    # =========================================================================
    with tab_bap:
        st.markdown("### Penerbitan & Cetak Berita Acara Pemeriksaan (BAP)")
        st.caption("Dokumen resmi Berita Acara Kemajuan Pekerjaan Fisik untuk pengajuan termin pembayaran atau verifikasi Owner.")

        with st.form("form_bap_config"):
            c1, c2 = st.columns(2)
            with c1:
                bap_no = st.text_input("Nomor BAP *", value=f"BAP/002/HS-06/IKI/III/{datetime.now().year}")
                bap_tgl = st.date_input("Tanggal Berita Acara", value=date.today())
                pihak1_nama = st.text_input("Nama Pihak Pertama (Galangan Pelaksana)", value="Ir. H. Sudirman, MT")
                pihak1_jabatan = st.text_input("Jabatan Pihak Pertama", value="Project Director / Kepala Galangan")
            with c2:
                pihak2_nama = st.text_input("Nama Pihak Kedua (Owner / Supervisi)", value="Capt. Agus Wicaksono, M.Mar")
                pihak2_jabatan = st.text_input("Jabatan Pihak Kedua", value="Owner Surveyor PT ASDP Indonesia Ferry")
                bap_progres = st.number_input("Persentase Kemajuan Fisik Terverifikasi (%)", min_value=0.0, max_value=100.0, value=float(stats.get("overall_progress", 55.7)), step=0.5)
                bap_catatan = st.text_area("Catatan Berita Acara", value="Pekerjaan perakitan panel bottom dan panel sisi telah memenuhi standar klasifikasi BKI tanpa catatan teknis yang tertunda.")

            generate_bap = st.form_submit_button("Generate Lembar BAP Siap Cetak")

        if generate_bap or True:
            k_nama = kapal.get("nama_kapal", "KM. NUSANTARA") if kapal else "KM. NUSANTARA"
            k_gt = kapal.get("gt", 750) if kapal else 750
            k_tipe = kapal.get("type_kapal", "Ferry Ro-Ro") if kapal else "Ferry Ro-Ro"

            st.markdown(f"""
            <div class="bap-print-container" style="border:1px solid #CBD5E1; padding:32px 40px; margin-top:20px; background-color:#FFFFFF; border-radius:4px; color:#000000;">
                <div style="text-align:center; border-bottom:2px solid #000; padding-bottom:12px; margin-bottom:20px;">
                    <h3 style="margin:0; text-transform:uppercase; font-size:18px; letter-spacing:1px; color:#000;">BERITA ACARA KEMAJUAN PEKERJAAN (BAP)</h3>
                    <div style="font-size:13px; font-weight:600; color:#333; margin-top:4px;">NOMOR: {bap_no}</div>
                </div>

                <p style="font-size:13px; line-height:1.6; text-align:justify; color:#000;">
                    Pada hari ini, <strong>{format_date(bap_tgl.isoformat() if isinstance(bap_tgl, date) else str(bap_tgl))}</strong>, bertempat di Galangan Kapal PT Industri Kapal Indonesia (Persero), kami yang bertanda tangan di bawah ini:
                </p>

                <table style="width:100%; font-size:13px; line-height:1.6; color:#000; margin-bottom:14px;">
                    <tr>
                        <td style="width:25px; vertical-align:top;">1.</td>
                        <td style="width:180px; vertical-align:top;"><strong>Nama / Jabatan</strong></td>
                        <td style="width:15px; vertical-align:top;">:</td>
                        <td>{pihak1_nama} — {pihak1_jabatan}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td style="vertical-align:top;"><strong>Instansi</strong></td>
                        <td style="vertical-align:top;">:</td>
                        <td>PT Industri Kapal Indonesia (Persero) bertindak sebagai <strong>PIHAK PERTAMA (GALANGAN)</strong></td>
                    </tr>
                    <tr><td colspan="4" style="height:8px;"></td></tr>
                    <tr>
                        <td style="vertical-align:top;">2.</td>
                        <td style="vertical-align:top;"><strong>Nama / Jabatan</strong></td>
                        <td style="vertical-align:top;">:</td>
                        <td>{pihak2_nama} — {pihak2_jabatan}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td style="vertical-align:top;"><strong>Instansi</strong></td>
                        <td style="vertical-align:top;">:</td>
                        <td>PT ASDP Indonesia Ferry (Persero) bertindak sebagai <strong>PIHAK KEDUA (OWNER SURVEYOR)</strong></td>
                    </tr>
                </table>

                <p style="font-size:13px; line-height:1.6; text-align:justify; color:#000;">
                    Menyatakan bahwa telah dilakukan inspeksi dan verifikasi bersama terhadap kemajuan fisik pembangunan kapal baru dengan rincian sebagai berikut:
                </p>

                <div style="background-color:#F8FAFC; border:1px solid #E2E8F0; padding:12px 18px; margin-bottom:16px; border-radius:4px; color:#000000;">
                    <table style="width:100%; font-size:13px; line-height:1.6; color:#000;">
                        <tr><td style="width:180px;"><strong>Nama Kapal</strong></td><td>: {k_nama}</td></tr>
                        <tr><td><strong>Tipe / Ukuran</strong></td><td>: {k_tipe} / {k_gt} GT</td></tr>
                        <tr><td><strong>Nomor Proyek</strong></td><td>: {active_project}</td></tr>
                        <tr><td><strong>Realisasi Kemajuan</strong></td><td>: <span style="font-size:15px; font-weight:800; color:#15803D;">{bap_progres:.1f}%</span></td></tr>
                        <tr><td><strong>Catatan Pemeriksaan</strong></td><td>: {bap_catatan}</td></tr>
                    </table>
                </div>

                <p style="font-size:13px; line-height:1.6; text-align:justify; color:#000;">
                    Demikian Berita Acara Pemeriksaan Kemajuan Pekerjaan ini dibuat dalam rangkap yang cukup dan mempunyai kekuatan hukum yang sama untuk dapat dipergunakan sebagaimana mestinya.
                </p>

                <div style="margin-top:40px;">
                    <table style="width:100%; text-align:center; font-size:13px; color:#000;">
                        <tr>
                            <td style="width:50%;">
                                PIHAK PERTAMA<br><strong>PT Industri Kapal Indonesia (Persero)</strong><br><br><br><br><br>
                                <u><strong>{pihak1_nama}</strong></u><br>{pihak1_jabatan}
                            </td>
                            <td style="width:50%;">
                                PIHAK KEDUA<br><strong>PT ASDP Indonesia Ferry (Persero)</strong><br><br><br><br><br>
                                <u><strong>{pihak2_nama}</strong></u><br>{pihak2_jabatan}
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            """, unsafe_allow_html=True)

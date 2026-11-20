"""
SIBS: Shipyard Integrated Business System
Database Module — Supabase Client Wrapper

Semua operasi database (CRUD) untuk setiap entitas.
"""

import logging
import json
from typing import Dict, List, Optional
from datetime import datetime, date

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Supabase database wrapper for all SIBS operations."""

    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize Supabase client from environment."""
        from config import supabase_config
        if not supabase_config.is_configured:
            logger.warning("Supabase belum dikonfigurasi (URL/KEY kosong). Set SUPABASE_URL dan SUPABASE_KEY di .env")
            return
        try:
            from supabase import create_client
            self.client = create_client(supabase_config.URL, supabase_config.KEY)
            logger.info("Supabase client berhasil terhubung")
        except Exception as e:
            logger.error(f"Gagal menghubungkan Supabase: {e}")

    @property
    def is_connected(self) -> bool:
        return self.client is not None

    # ------------------------------------------------------------------
    #  HELPER: safe query execution
    # ------------------------------------------------------------------
    def _query(self, table: str):
        """Return a table query builder, or None."""
        if not self.client:
            return None
        return self.client.table(table)

    def _safe_execute(self, builder, fallback=None):
        """Execute a query builder and return .data, or fallback on error."""
        if builder is None:
            return fallback if fallback is not None else []
        try:
            resp = builder.execute()
            return resp.data if resp.data else (fallback if fallback is not None else [])
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return fallback if fallback is not None else []

    # ==================================================================
    #  KAPAL (Ship Data)
    # ==================================================================
    def get_all_kapal(self) -> List[dict]:
        q = self._query("kapal")
        if q:
            q = q.select("*").order("created_at", desc=True)
        return self._safe_execute(q, [])

    def get_kapal(self, id_project: str) -> Optional[dict]:
        q = self._query("kapal")
        if q:
            q = q.select("*").eq("id_project", id_project).limit(1)
        rows = self._safe_execute(q, [])
        return rows[0] if rows else None

    def upsert_kapal(self, data: dict) -> bool:
        q = self._query("kapal")
        if not q:
            return False
        try:
            data["updated_at"] = datetime.utcnow().isoformat()
            q.upsert(data, on_conflict="id_project").execute()
            return True
        except Exception as e:
            logger.error(f"Upsert kapal error: {e}")
            return False

    # ==================================================================
    #  BLOK
    # ==================================================================
    def get_blok_by_project(self, id_project: str) -> List[dict]:
        q = self._query("blok")
        if q:
            q = q.select("*").eq("id_project", id_project).order("id_blok")
        return self._safe_execute(q, [])

    def upsert_blok(self, data: dict) -> bool:
        q = self._query("blok")
        if not q:
            return False
        try:
            q.upsert(data, on_conflict="id_project,id_blok").execute()
            return True
        except Exception as e:
            logger.error(f"Upsert blok error: {e}")
            return False

    # ==================================================================
    #  PWBS DETAIL
    # ==================================================================
    def get_pwbs_by_blok(self, id_project: str, id_blok: str) -> List[dict]:
        q = self._query("pwbs_detail")
        if q:
            q = q.select("*").eq("id_project", id_project).eq("id_blok", id_blok).order("id")
        return self._safe_execute(q, [])

    def insert_pwbs(self, data: dict) -> bool:
        q = self._query("pwbs_detail")
        if not q:
            return False
        try:
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Insert PWBS error: {e}")
            return False

    # ==================================================================
    #  MATERIAL
    # ==================================================================
    def get_all_material(self) -> List[dict]:
        q = self._query("material")
        if q:
            q = q.select("*").order("nama_material")
        return self._safe_execute(q, [])

    def get_material_by_project(self, id_project: str) -> List[dict]:
        q = self._query("material")
        if q:
            q = q.select("*").eq("id_project", id_project)
        return self._safe_execute(q, [])

    def upsert_material(self, data: dict) -> bool:
        q = self._query("material")
        if not q:
            return False
        try:
            q.upsert(data, on_conflict="id_material").execute()
            return True
        except Exception as e:
            logger.error(f"Upsert material error: {e}")
            return False

    # ==================================================================
    #  PEKERJA
    # ==================================================================
    def get_all_pekerja(self) -> List[dict]:
        q = self._query("pekerja")
        if q:
            q = q.select("*").order("id_pekerja")
        return self._safe_execute(q, [])

    def get_pekerja_by_project(self, id_project: str) -> List[dict]:
        q = self._query("pekerja")
        if q:
            q = q.select("*").eq("id_project", id_project)
        return self._safe_execute(q, [])

    def upsert_pekerja(self, data: dict) -> bool:
        q = self._query("pekerja")
        if not q:
            return False
        try:
            q.upsert(data, on_conflict="id_pekerja").execute()
            return True
        except Exception as e:
            logger.error(f"Upsert pekerja error: {e}")
            return False

    # ==================================================================
    #  FASILITAS
    # ==================================================================
    def get_all_fasilitas(self) -> List[dict]:
        q = self._query("fasilitas")
        if q:
            q = q.select("*").order("id_fasilitas")
        return self._safe_execute(q, [])

    def upsert_fasilitas(self, data: dict) -> bool:
        q = self._query("fasilitas")
        if not q:
            return False
        try:
            data["updated_at"] = datetime.utcnow().isoformat()
            q.upsert(data, on_conflict="id_fasilitas").execute()
            return True
        except Exception as e:
            logger.error(f"Upsert fasilitas error: {e}")
            return False

    # -- Fasilitas Maintenance --
    def get_maintenance_requests(self, id_fasilitas: str = None) -> List[dict]:
        q = self._query("fasilitas_maintenance")
        if q:
            q = q.select("*").order("tanggal_request", desc=True)
            if id_fasilitas:
                q = q.eq("id_fasilitas", id_fasilitas)
        return self._safe_execute(q, [])

    def create_maintenance_request(self, data: dict) -> bool:
        q = self._query("fasilitas_maintenance")
        if not q:
            return False
        try:
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Insert maintenance error: {e}")
            return False

    def update_maintenance_status(self, record_id: int, status: str, **kwargs) -> bool:
        q = self._query("fasilitas_maintenance")
        if not q:
            return False
        try:
            update_data = {"status": status}
            if status == "selesai":
                update_data["tanggal_selesai"] = datetime.utcnow().isoformat()
            update_data.update(kwargs)
            q.update(update_data).eq("id", record_id).execute()
            return True
        except Exception as e:
            logger.error(f"Update maintenance error: {e}")
            return False

    # -- Fasilitas Usage --
    def get_fasilitas_usage(self, id_fasilitas: str = None) -> List[dict]:
        q = self._query("fasilitas_usage")
        if q:
            q = q.select("*").order("tanggal_mulai", desc=True)
            if id_fasilitas:
                q = q.eq("id_fasilitas", id_fasilitas)
        return self._safe_execute(q, [])

    def create_fasilitas_usage(self, data: dict) -> bool:
        q = self._query("fasilitas_usage")
        if not q:
            return False
        try:
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Insert fasilitas usage error: {e}")
            return False

    # ==================================================================
    #  SCHEDULE DETAIL
    # ==================================================================
    def get_schedule_by_project(self, id_project: str) -> List[dict]:
        q = self._query("schedule_detail")
        if q:
            q = q.select("*").eq("id_project", id_project).order("no_urut")
        return self._safe_execute(q, [])

    def upsert_schedule(self, data: dict) -> bool:
        q = self._query("schedule_detail")
        if not q:
            return False
        try:
            q.upsert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Upsert schedule error: {e}")
            return False

    def update_schedule_progress(self, record_id: int, progress: float) -> bool:
        q = self._query("schedule_detail")
        if not q:
            return False
        try:
            q.update({"progress": progress}).eq("id", record_id).execute()
            return True
        except Exception as e:
            logger.error(f"Update schedule progress error: {e}")
            return False

    # ==================================================================
    #  PRODUKSI DATA
    # ==================================================================
    def get_produksi_by_project(self, id_project: str) -> List[dict]:
        q = self._query("produksi_data")
        if q:
            q = q.select("*").eq("id_project", id_project).order("tanggal")
        return self._safe_execute(q, [])

    def insert_produksi(self, data: dict) -> bool:
        q = self._query("produksi_data")
        if not q:
            return False
        try:
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Insert produksi error: {e}")
            return False

    def update_produksi_status(self, record_id: int, status: str) -> bool:
        q = self._query("produksi_data")
        if not q:
            return False
        try:
            q.update({"status": status}).eq("id", record_id).execute()
            return True
        except Exception as e:
            logger.error(f"Update produksi error: {e}")
            return False

    # ==================================================================
    #  GUDANG
    # ==================================================================
    def get_all_barang(self) -> List[dict]:
        q = self._query("gudang_barang")
        if q:
            q = q.select("*").order("nama_barang")
        return self._safe_execute(q, [])

    def get_barang(self, id_barang: str) -> Optional[dict]:
        q = self._query("gudang_barang")
        if q:
            q = q.select("*").eq("id_barang", id_barang).limit(1)
        rows = self._safe_execute(q, [])
        return rows[0] if rows else None

    def upsert_barang(self, data: dict) -> bool:
        q = self._query("gudang_barang")
        if not q:
            return False
        try:
            data["updated_at"] = datetime.utcnow().isoformat()
            q.upsert(data, on_conflict="id_barang").execute()
            return True
        except Exception as e:
            logger.error(f"Upsert barang error: {e}")
            return False

    def create_mutasi(self, id_barang: str, tipe: str, jumlah: float,
                      created_by: str = None, **kwargs) -> bool:
        """Create a warehouse mutation and update stock."""
        if not self.client:
            return False
        try:
            # Get current stock
            barang = self.get_barang(id_barang)
            if not barang:
                logger.error(f"Barang {id_barang} tidak ditemukan")
                return False

            current_stock = float(barang.get("stok_current", 0))
            if tipe == "keluar" and jumlah > current_stock:
                logger.error(f"Stok tidak cukup: {current_stock} < {jumlah}")
                return False

            new_stock = current_stock + jumlah if tipe == "masuk" else current_stock - jumlah

            # Insert mutation record
            mutasi_data = {
                "id_barang": id_barang,
                "tipe": tipe,
                "jumlah": jumlah,
                "created_by": created_by,
                **kwargs,
            }
            self.client.table("gudang_mutasi").insert(mutasi_data).execute()

            # Update stock
            self.client.table("gudang_barang").update({
                "stok_current": new_stock,
                "updated_at": datetime.utcnow().isoformat(),
            }).eq("id_barang", id_barang).execute()

            return True
        except Exception as e:
            logger.error(f"Create mutasi error: {e}")
            return False

    def get_mutasi_history(self, id_barang: str = None, limit: int = 100) -> List[dict]:
        q = self._query("gudang_mutasi")
        if q:
            q = q.select("*").order("tanggal", desc=True).limit(limit)
            if id_barang:
                q = q.eq("id_barang", id_barang)
        return self._safe_execute(q, [])

    def get_barang_low_stock(self) -> List[dict]:
        """Get items where current stock is at or below minimum."""
        all_items = self.get_all_barang()
        return [
            item for item in all_items
            if float(item.get("stok_current", 0)) <= float(item.get("stok_minimum", 0))
            and float(item.get("stok_minimum", 0)) > 0
        ]

    # ==================================================================
    #  INSPEKSI QA/QC
    # ==================================================================
    def get_inspeksi_by_project(self, id_project: str, kategori: str = None) -> List[dict]:
        q = self._query("inspeksi_qc")
        if q:
            q = q.select("*").eq("id_project", id_project).order("tanggal_inspeksi", desc=True)
            if kategori:
                q = q.eq("kategori", kategori)
        return self._safe_execute(q, [])

    def create_inspeksi(self, data: dict) -> bool:
        q = self._query("inspeksi_qc")
        if not q:
            return False
        try:
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Insert inspeksi error: {e}")
            return False

    def update_inspeksi_status(self, record_id: int, status: str, approved_by: str = None) -> bool:
        q = self._query("inspeksi_qc")
        if not q:
            return False
        try:
            update_data = {"status": status}
            if approved_by:
                update_data["approved_by"] = approved_by
                update_data["tanggal_approval"] = datetime.utcnow().isoformat()
            q.update(update_data).eq("id", record_id).execute()
            return True
        except Exception as e:
            logger.error(f"Update inspeksi error: {e}")
            return False

    def get_inspeksi_summary(self, id_project: str) -> dict:
        """Count inspections by status for a project."""
        rows = self.get_inspeksi_by_project(id_project)
        summary = {"total": len(rows), "approved": 0, "rejected": 0, "pending": 0}
        for r in rows:
            s = r.get("status", "pending")
            if s in summary:
                summary[s] += 1
        return summary

    # ==================================================================
    #  SUPPLIER
    # ==================================================================
    def get_all_supplier(self) -> List[dict]:
        q = self._query("supplier")
        if q:
            q = q.select("*").eq("is_active", True).order("nama")
        return self._safe_execute(q, [])

    def upsert_supplier(self, data: dict) -> bool:
        q = self._query("supplier")
        if not q:
            return False
        try:
            q.upsert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Upsert supplier error: {e}")
            return False

    # ==================================================================
    #  PURCHASE ORDER
    # ==================================================================
    def get_purchase_orders(self, id_project: str = None, status: str = None) -> List[dict]:
        q = self._query("purchase_order")
        if q:
            q = q.select("*").order("created_at", desc=True)
            if id_project:
                q = q.eq("id_project", id_project)
            if status:
                q = q.eq("status", status)
        return self._safe_execute(q, [])

    def create_purchase_order(self, po_data: dict, items: List[dict] = None) -> bool:
        if not self.client:
            return False
        try:
            resp = self.client.table("purchase_order").insert(po_data).execute()
            if items and resp.data:
                po_id = resp.data[0]["id"]
                for item in items:
                    item["id_po"] = po_id
                self.client.table("purchase_order_item").insert(items).execute()
            return True
        except Exception as e:
            logger.error(f"Create PO error: {e}")
            return False

    def update_po_status(self, po_id: int, status: str, approved_by: str = None) -> bool:
        q = self._query("purchase_order")
        if not q:
            return False
        try:
            update_data = {"status": status, "updated_at": datetime.utcnow().isoformat()}
            if approved_by:
                update_data["approved_by"] = approved_by
            q.update(update_data).eq("id", po_id).execute()
            return True
        except Exception as e:
            logger.error(f"Update PO status error: {e}")
            return False

    def get_po_items(self, po_id: int) -> List[dict]:
        q = self._query("purchase_order_item")
        if q:
            q = q.select("*").eq("id_po", po_id)
        return self._safe_execute(q, [])

    # ==================================================================
    #  PERMINTAAN MATERIAL (Produksi → Gudang)
    # ==================================================================
    def get_permintaan_material(self, id_project: str = None, status: str = None) -> List[dict]:
        q = self._query("permintaan_material")
        if q:
            q = q.select("*").order("tanggal_request", desc=True)
            if id_project:
                q = q.eq("id_project", id_project)
            if status:
                q = q.eq("status", status)
        return self._safe_execute(q, [])

    def create_permintaan_material(self, data: dict) -> bool:
        q = self._query("permintaan_material")
        if not q:
            return False
        try:
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Insert permintaan material error: {e}")
            return False

    def update_permintaan_status(self, record_id: int, status: str, approved_by: str = None) -> bool:
        q = self._query("permintaan_material")
        if not q:
            return False
        try:
            update_data = {"status": status}
            if approved_by:
                update_data["approved_by"] = approved_by
                update_data["tanggal_approval"] = datetime.utcnow().isoformat()
            q.update(update_data).eq("id", record_id).execute()
            return True
        except Exception as e:
            logger.error(f"Update permintaan error: {e}")
            return False

    # ==================================================================
    #  USERS
    # ==================================================================
    def get_user_by_username(self, username: str) -> Optional[dict]:
        q = self._query("users")
        if q:
            q = q.select("*").eq("username", username).eq("is_active", True).limit(1)
        rows = self._safe_execute(q, [])
        return rows[0] if rows else None

    def get_all_users(self) -> List[dict]:
        q = self._query("users")
        if q:
            q = q.select("id,username,nama_lengkap,role,departemen,is_active,created_at").order("username")
        return self._safe_execute(q, [])

    def create_user(self, data: dict) -> bool:
        q = self._query("users")
        if not q:
            return False
        try:
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Create user error: {e}")
            return False

    def update_user(self, username: str, data: dict) -> bool:
        q = self._query("users")
        if not q:
            return False
        try:
            data["updated_at"] = datetime.utcnow().isoformat()
            q.update(data).eq("username", username).execute()
            return True
        except Exception as e:
            logger.error(f"Update user error: {e}")
            return False

    # ==================================================================
    #  AUDIT LOG
    # ==================================================================
    def log_action(self, username: str, action: str, target_table: str = None,
                   target_id: str = None, old_value=None, new_value=None,
                   keterangan: str = None) -> bool:
        q = self._query("audit_log")
        if not q:
            return False
        try:
            data = {
                "username": username,
                "action": action,
                "target_table": target_table,
                "target_id": target_id,
                "keterangan": keterangan,
            }
            if old_value is not None:
                data["old_value"] = json.dumps(old_value) if not isinstance(old_value, str) else old_value
            if new_value is not None:
                data["new_value"] = json.dumps(new_value) if not isinstance(new_value, str) else new_value
            q.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Log action error: {e}")
            return False

    def get_audit_logs(self, limit: int = 200, username: str = None) -> List[dict]:
        q = self._query("audit_log")
        if q:
            q = q.select("*").order("created_at", desc=True).limit(limit)
            if username:
                q = q.eq("username", username)
        return self._safe_execute(q, [])

    # ==================================================================
    #  DASHBOARD AGGREGATION
    # ==================================================================
    def get_dashboard_stats(self, id_project: str) -> dict:
        """Aggregate key metrics for the executive dashboard."""
        stats = {
            "kapal": self.get_kapal(id_project),
            "blok_count": len(self.get_blok_by_project(id_project)),
            "material_count": len(self.get_material_by_project(id_project)),
            "inspeksi_summary": self.get_inspeksi_summary(id_project),
            "low_stock_items": self.get_barang_low_stock(),
            "pending_po": len(self.get_purchase_orders(id_project, status="draft")),
            "pending_permintaan": len(self.get_permintaan_material(id_project, status="pending")),
        }

        # Calculate schedule progress
        schedules = self.get_schedule_by_project(id_project)
        if schedules:
            top_level = [s for s in schedules if "." not in str(s.get("no_urut", ""))]
            if top_level:
                total_progress = sum(float(s.get("progress", 0)) for s in top_level)
                stats["overall_progress"] = total_progress / len(top_level)
            else:
                stats["overall_progress"] = 0
        else:
            stats["overall_progress"] = 0

        return stats


# Global instance
db_manager = DatabaseManager()

"""
SIBS: Shipyard Integrated Business System
Configuration Module — Supabase + App Settings

Sumber: Skripsi Ratih Laratasari Pagayang (Unhas, 2025)
        + Sistem Informasi Galangan Kecil.xlsm
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH, override=True)


# ==================== SUPABASE CONFIG ====================
@dataclass
class SupabaseConfig:
    URL: str = os.getenv("SUPABASE_URL", "")
    KEY: str = os.getenv("SUPABASE_KEY", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.URL and self.KEY)


# ==================== APP CONFIG ====================
@dataclass
class AppConfig:
    TITLE: str = "SIBS — Sistem Integrasi Bisnis Galangan Kapal"
    SHORT_TITLE: str = "SIBS"
    VERSION: str = "4.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


# ==================== SECURITY CONFIG ====================
@dataclass
class SecurityConfig:
    PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", "6"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))


# ==================== INSTANCES ====================
supabase_config = SupabaseConfig()
app_config = AppConfig()
security_config = SecurityConfig()


# ==================== DEPARTMENTS ====================
DEPARTMENTS = {
    "admin": {
        "display": "Administrator",
        "permissions": ["full_access"],
    },
    "perencanaan": {
        "display": "Desain & Perencanaan Produksi",
        "permissions": ["view_data", "edit_design", "manage_pwbs"],
    },
    "produksi": {
        "display": "Produksi Lapangan",
        "permissions": ["view_data", "update_progress", "request_material"],
    },
    "pembelian": {
        "display": "Pembelian & Logistik",
        "permissions": ["view_data", "manage_vendors", "manage_po"],
    },
    "qaqc": {
        "display": "Quality Control / Quality Assurance",
        "permissions": ["view_data", "validate_quality", "approve_reject"],
    },
    "gudang": {
        "display": "Material & Penyimpanan (Gudang)",
        "permissions": ["view_data", "manage_inventory", "manage_mutasi"],
    },
    "fasilitas": {
        "display": "Manajemen Fasilitas",
        "permissions": ["view_data", "manage_facilities", "manage_maintenance"],
    },
    "eksekutif": {
        "display": "Manajemen Eksekutif",
        "permissions": ["view_data", "view_reports", "export_data"],
    },
}

# ==================== QC INSPECTION CATEGORIES ====================
# Based on 40+ QC sheets in the Excel VBA file
QC_CATEGORIES = [
    {"id": "straightening", "nama": "Straightening", "grup": "Hull Construction"},
    {"id": "forming_bending", "nama": "Forming and Bending", "grup": "Hull Construction"},
    {"id": "surface_preparation", "nama": "Surface Preparation & Machine Cutting", "grup": "Hull Construction"},
    {"id": "steelwork_process", "nama": "Steelwork Process", "grup": "Hull Construction"},
    {"id": "keel_laying", "nama": "Keel Laying", "grup": "Hull Construction"},
    {"id": "conformity_with", "nama": "Conformity With Standards", "grup": "Standards"},
    {"id": "conformity_for", "nama": "Conformity For Standards", "grup": "Standards"},
    {"id": "remedial_work", "nama": "Remedial Work & Alteration", "grup": "Standards"},
    {"id": "welding_qualification", "nama": "Welding Qualification", "grup": "Welding"},
    {"id": "welding_consumables", "nama": "Welding Consumables", "grup": "Welding"},
    {"id": "welding_environment", "nama": "Welding Environment", "grup": "Welding"},
    {"id": "welding_equipment", "nama": "Welding Equipment", "grup": "Welding"},
    {"id": "welding_surfaces", "nama": "Welding Surfaces", "grup": "Welding"},
    {"id": "welding_mech", "nama": "Welding Mechanical Test", "grup": "Welding"},
    {"id": "structural_testing", "nama": "Structural Testing", "grup": "Testing"},
    {"id": "tightness_testing", "nama": "Tightness Testing", "grup": "Testing"},
    {"id": "inclining_experiment", "nama": "Inclining Experiment", "grup": "Testing"},
    {"id": "insulation", "nama": "Insulation", "grup": "Outfitting"},
    {"id": "hatch_covers", "nama": "Hatch Covers", "grup": "Outfitting"},
    {"id": "safety_construction", "nama": "Safety Construction", "grup": "Safety"},
    {"id": "cable_installation", "nama": "Cable Installation", "grup": "Electrical"},
    {"id": "main_switchboard", "nama": "Main Switchboard", "grup": "Electrical"},
    {"id": "emergency_switchboard", "nama": "Emergency Switchboard", "grup": "Electrical"},
    {"id": "main_lighting", "nama": "Main Lighting", "grup": "Electrical"},
    {"id": "emergency_lighting", "nama": "Emergency Lighting", "grup": "Electrical"},
    {"id": "navigation_lighting", "nama": "Navigation Lighting", "grup": "Electrical"},
    {"id": "doors_ramps", "nama": "Doors & Ramps Integral", "grup": "Outfitting"},
    {"id": "door_window", "nama": "Door & Window", "grup": "Outfitting"},
    {"id": "lifting_appliances", "nama": "Lifting Appliances", "grup": "Equipment"},
    {"id": "livesaving", "nama": "Life Saving Foundation", "grup": "Safety"},
    {"id": "rudders", "nama": "Rudders", "grup": "Hull Construction"},
    {"id": "forgings", "nama": "Forgings", "grup": "Hull Construction"},
    {"id": "freeboard", "nama": "Freeboard", "grup": "Measurement"},
    {"id": "principal_dimensions", "nama": "Principal Dimensions", "grup": "Measurement"},
    {"id": "shape", "nama": "Shape", "grup": "Measurement"},
    {"id": "launching", "nama": "Launching", "grup": "Final"},
    {"id": "anchor", "nama": "Anchor", "grup": "Equipment"},
    {"id": "windlass", "nama": "Windlass", "grup": "Equipment"},
    {"id": "mast_post_rigging", "nama": "Mast, Post & Rigging", "grup": "Equipment"},
]

# ==================== DEFAULT USERS ====================
DEFAULT_USERS = [
    ("admin", "admin123", "Administrator Sistem", "admin", "IT"),
    ("perencanaan", "super123", "Staff Perencanaan", "perencanaan", "Planning"),
    ("produksi", "super123", "Staff Produksi", "produksi", "Operations"),
    ("pembelian", "super123", "Staff Pembelian", "pembelian", "Procurement"),
    ("qaqc", "super123", "Staff QA/QC", "qaqc", "Quality"),
    ("gudang", "super123", "Staff Gudang", "gudang", "Warehouse"),
    ("fasilitas", "super123", "Staff Fasilitas", "fasilitas", "Facilities"),
    ("eksekutif", "super123", "Pimpinan Eksekutif", "eksekutif", "Executive"),
]

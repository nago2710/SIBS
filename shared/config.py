"""
Configuration module for NAV-MIS System
Handles all configuration, environment variables, and constants
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class DatabaseConfig:
    """Database configuration"""
    DB_FILE: str = os.getenv("DB_FILE", "database_galangan.db")
    BACKUP_ENABLED: bool = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
    BACKUP_INTERVAL: int = int(os.getenv("BACKUP_INTERVAL", "3600"))  # seconds


@dataclass
class SecurityConfig:
    """Security configuration"""
    PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", "6"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # seconds
    ENABLE_LOGGING: bool = os.getenv("ENABLE_LOGGING", "true").lower() == "true"


@dataclass
class AppConfig:
    """Application configuration"""
    APP_TITLE: str = "NAV-MIS: Integrated Shipyard System"
    APP_ICON: str = "⚓"
    LAYOUT: str = "wide"
    VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


@dataclass
class UIConfig:
    """UI/UX configuration"""
    PRIMARY_COLOR: str = "#2563eb"
    DARK_BG: str = "#0b0f19"
    CARD_BG: str = "#111827"
    BORDER_COLOR: str = "#1f293d"
    TEXT_PRIMARY: str = "#f1f5f9"
    TEXT_SECONDARY: str = "#94a3b8"
    SUCCESS_COLOR: str = "#4ade80"
    ERROR_COLOR: str = "#f87171"
    WARNING_COLOR: str = "#fbbf24"


# Initialize all configurations
db_config = DatabaseConfig()
security_config = SecurityConfig()
app_config = AppConfig()
ui_config = UIConfig()

# Department roles and permissions
DEPARTMENTS = {
    "admin": {
        "display": "Administrator",
        "permissions": ["full_access"]
    },
    "perencanaan": {
        "display": "Perencanaan & Desain",
        "permissions": ["view_data", "edit_design"]
    },
    "produksi": {
        "display": "Produksi Lapangan",
        "permissions": ["view_data", "update_progress"]
    },
    "pembelian": {
        "display": "Pembelian & Logistik",
        "permissions": ["view_data", "manage_vendors"]
    },
    "qaqa": {
        "display": "QA / QC",
        "permissions": ["view_data", "validate_quality"]
    },
    "gudang": {
        "display": "Gudang Material",
        "permissions": ["view_data", "manage_inventory"]
    },
    "fasilitas": {
        "display": "Manajemen Fasilitas",
        "permissions": ["view_data", "update_facilities"]
    },
    "eksekutif": {
        "display": "Eksekutif Pemantau",
        "permissions": ["view_data", "view_reports"]
    }
}

# Default project indicators
DEFAULT_PROJECT_DATA = [
    ("Nama Proyek Aktif", "Hull No. 284 - General Cargo Vessel 5000 DWT"),
    ("Master Schedule", "Tahap Erection Blok & Instalasi Pipa Lambung"),
    ("PWBS / Area Kerja", "Blok Midship M1 s/d M4"),
    ("Anggaran Alokasi Proyek", "18500000000"),
    ("Biaya Konstruksi Terpakai", "9240000000"),
    ("Volume Stok Pelat Baja (Gudang)", "342"),
    ("Status Inspeksi QA/QC", "Lolos Uji NDT Radiography Butt Joint Blok M1"),
    ("Kelayakan Fasilitas Gantry Crane", "Operasional Normal - Sertifikasi Aktif"),
    ("Target Waktu Peluncuran (Delivery)", "14 November 2026"),
    ("Vendor Utama Logistik", "PT Krakatau Steel Tbk")
]

# Default system users
DEFAULT_USERS = [
    ("ahmad.fauzi", "admin123", "admin", "IT"),
    ("budi.santoso", "super123", "produksi", "Operations"),
    ("siti.cahaya", "super123", "perencanaan", "Planning"),
    ("eka.wijaya", "super123", "pembelian", "Procurement"),
    ("rini.dewi", "super123", "qaqa", "Quality"),
    ("doni.kusuma", "super123", "gudang", "Warehouse"),
    ("yanti.santoso", "super123", "fasilitas", "Facilities"),
    ("bambang.wijaya", "super123", "eksekutif", "Executive")
]

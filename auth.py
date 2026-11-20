"""
SIBS: Shipyard Integrated Business System
Authentication Module — Password hashing, login, permissions
"""

import hashlib
import secrets
import logging
from typing import Dict, Tuple, Optional
from config import security_config, DEPARTMENTS

logger = logging.getLogger(__name__)


# ==================== PASSWORD HASHING (stdlib PBKDF2) ====================

def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256 with random salt."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}:{dk.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored PBKDF2 hash."""
    try:
        salt, expected = stored_hash.split(":", 1)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
        return dk.hex() == expected
    except Exception:
        return False


# ==================== AUTHENTICATION MANAGER ====================

class AuthenticationManager:
    """Handles login, permission checks, and user session management."""

    def __init__(self):
        self.login_attempts: Dict[str, int] = {}

    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[dict], str]:
        """
        Authenticate against Supabase users table.
        Returns (success, user_info_dict, message).
        """
        from database import db_manager

        if not db_manager.is_connected:
            return False, None, "Database belum terhubung. Periksa konfigurasi Supabase."

        # Input validation
        if not username or len(username) < 2:
            return False, None, "Username minimal 2 karakter."
        if not password or len(password) < security_config.PASSWORD_MIN_LENGTH:
            return False, None, f"Password minimal {security_config.PASSWORD_MIN_LENGTH} karakter."

        # Check login attempts
        attempts = self.login_attempts.get(username, 0)
        if attempts >= security_config.MAX_LOGIN_ATTEMPTS:
            return False, None, "Terlalu banyak percobaan login. Coba lagi nanti."

        # Fetch user from DB
        user = db_manager.get_user_by_username(username)
        if not user:
            self.login_attempts[username] = attempts + 1
            return False, None, "Username atau password salah."

        # Verify password
        if not verify_password(password, user.get("password_hash", "")):
            self.login_attempts[username] = attempts + 1
            return False, None, "Username atau password salah."

        # Success — reset attempts
        self.login_attempts[username] = 0
        role = user.get("role", "viewer")
        dept_info = DEPARTMENTS.get(role, {})

        user_info = {
            "username": user["username"],
            "nama_lengkap": user.get("nama_lengkap", user["username"]),
            "role": role,
            "departemen": user.get("departemen", ""),
            "department_display": dept_info.get("display", role),
            "permissions": dept_info.get("permissions", ["view_data"]),
        }

        # Audit log
        db_manager.log_action(username, "LOGIN", keterangan="Login berhasil")
        logger.info(f"User '{username}' berhasil login (role={role})")
        return True, user_info, "Login berhasil."

    # ------------------------------------------------------------------
    #  PERMISSION HELPERS
    # ------------------------------------------------------------------
    @staticmethod
    def has_permission(user_info: dict, required: str) -> bool:
        """Check if user has a specific permission."""
        if not user_info:
            return False
        perms = user_info.get("permissions", [])
        return "full_access" in perms or required in perms

    @staticmethod
    def can_access_department(user_info: dict, dept_key: str) -> bool:
        """Check if user can access a department tab."""
        if not user_info:
            return False
        role = user_info.get("role", "")
        if role == "admin":
            return True
        return role == dept_key

    @staticmethod
    def is_admin(user_info: dict) -> bool:
        return user_info.get("role") == "admin" if user_info else False


# Global instance
auth_manager = AuthenticationManager()

"""
Authentication and validation module for NAV-MIS System
Handles user authentication, input validation, and security checks
"""

import re
import logging
from typing import Dict, Tuple, Optional
from database import db_manager
from config import security_config, DEPARTMENTS

logger = logging.getLogger(__name__)


class AuthValidator:
    """Authentication and input validation class"""

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username format and length"""
        if not username or len(username) < 3:
            return False, "Username minimal 3 karakter"
        if len(username) > 50:
            return False, "Username maksimal 50 karakter"
        if not re.match(r"^[a-zA-Z0-9._-]+$", username):
            return False, "Username hanya boleh berisi alfanumerik, titik, underscore, dan dash"
        return True, ""

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if not password or len(password) < security_config.PASSWORD_MIN_LENGTH:
            return False, f"Password minimal {security_config.PASSWORD_MIN_LENGTH} karakter"
        if len(password) > 100:
            return False, "Password maksimal 100 karakter"
        return True, ""

    @staticmethod
    def validate_currency_input(value: str) -> Tuple[bool, float]:
        """Validate and convert currency input"""
        try:
            # Remove common currency formatting
            cleaned = value.replace("Rp", "").replace(".", "").replace(",", "").strip()
            num_value = float(cleaned)
            if num_value < 0:
                return False, 0
            return True, num_value
        except ValueError:
            return False, 0

    @staticmethod
    def validate_percentage(value: float) -> Tuple[bool, str]:
        """Validate percentage value"""
        if not 0 <= value <= 100:
            return False, "Persentase harus antara 0-100"
        return True, ""

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, email):
            return True, ""
        return False, "Format email tidak valid"

    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Validate date format DD-MM-YYYY"""
        pattern = r"^\d{2}-\d{2}-\d{4}$"
        if re.match(pattern, date_str):
            return True, ""
        return False, "Format tanggal harus DD-MM-YYYY"


class AuthenticationManager:
    """Authentication management class"""

    def __init__(self):
        """Initialize authentication manager"""
        self.login_attempts = {}
        self.validator = AuthValidator()

    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Authenticate user credentials
        Returns: (success, user_info, message)
        """
        # Validate inputs
        is_valid_user, user_msg = self.validator.validate_username(username)
        if not is_valid_user:
            return False, None, user_msg

        is_valid_pass, pass_msg = self.validator.validate_password(password)
        if not is_valid_pass:
            return False, None, pass_msg

        # Check login attempts
        if username in self.login_attempts:
            if self.login_attempts[username] >= security_config.MAX_LOGIN_ATTEMPTS:
                return False, None, f"Terlalu banyak percobaan login. Coba lagi nanti."

        # Authenticate against database
        user_data = db_manager.get_user(username, password)

        if user_data:
            # Reset login attempts
            self.login_attempts[username] = 0
            user_info = {
                "username": user_data['username'],
                "role": user_data['role'],
                "department": user_data['departemen'],
                "department_display": DEPARTMENTS.get(user_data['role'], {}).get('display', user_data['role']),
                "permissions": DEPARTMENTS.get(user_data['role'], {}).get('permissions', [])
            }
            logger.info(f"User {username} authenticated successfully")
            return True, user_info, "Login berhasil"
        else:
            # Increment login attempts
            self.login_attempts[username] = self.login_attempts.get(username, 0) + 1
            logger.warning(f"Failed login attempt for user {username}")
            return False, None, "Username atau password salah"

    def check_permission(self, user_info: Dict, required_permission: str) -> bool:
        """Check if user has required permission"""
        if not user_info:
            return False

        permissions = user_info.get("permissions", [])
        if "full_access" in permissions:
            return True

        return required_permission in permissions

    def can_edit_data(self, user_info: Dict) -> bool:
        """Check if user can edit project data"""
        return self.check_permission(user_info, "full_access") or self.check_permission(user_info, "edit_design")

    def can_update_progress(self, user_info: Dict) -> bool:
        """Check if user can update production progress"""
        return self.check_permission(user_info, "full_access") or self.check_permission(user_info, "update_progress")

    def can_manage_inventory(self, user_info: Dict) -> bool:
        """Check if user can manage inventory"""
        return self.check_permission(user_info, "full_access") or self.check_permission(user_info, "manage_inventory")

    def can_validate_quality(self, user_info: Dict) -> bool:
        """Check if user can validate quality"""
        return self.check_permission(user_info, "full_access") or self.check_permission(user_info, "validate_quality")


# Global authentication manager instance
auth_manager = AuthenticationManager()

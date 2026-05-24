"""
Database module for NAV-MIS System
Handles all database operations, queries, and data management
"""

import sqlite3
import logging
from typing import Dict, List, Tuple, Optional
from contextlib import contextmanager
from config import db_config, DEFAULT_PROJECT_DATA, DEFAULT_USERS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database management class with context manager support"""

    def __init__(self, db_file: str = None):
        """Initialize database manager"""
        self.db_file = db_file or db_config.DB_FILE

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def initialize_database(self) -> bool:
        """Initialize database with tables and default data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        departemen TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                """)

                # Create project data table with metadata
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS proyek_data (
                        indikator TEXT PRIMARY KEY,
                        nilai TEXT NOT NULL,
                        kategori TEXT,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_by TEXT
                    )
                """)

                # Create audit log table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS audit_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT NOT NULL,
                        action TEXT NOT NULL,
                        target TEXT,
                        old_value TEXT,
                        new_value TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Check and populate default data
                cursor.execute("SELECT COUNT(*) FROM proyek_data")
                if cursor.fetchone()[0] == 0:
                    cursor.executemany(
                        "INSERT INTO proyek_data (indikator, nilai) VALUES (?, ?)",
                        DEFAULT_PROJECT_DATA
                    )
                    logger.info("Default project data inserted")

                # Check and populate default users
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    cursor.executemany(
                        "INSERT OR IGNORE INTO users (username, password, role, departemen) VALUES (?, ?, ?, ?)",
                        DEFAULT_USERS
                    )
                    logger.info("Default users inserted")

                conn.commit()
                logger.info("Database initialized successfully")
                return True

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            return False

    def get_all_project_data(self) -> Dict[str, str]:
        """Get all project data"""
        try:
            with self.get_connection() as conn:
                df_data = conn.execute("SELECT indikator, nilai FROM proyek_data").fetchall()
                return {row['indikator']: row['nilai'] for row in df_data}
        except sqlite3.Error as e:
            logger.error(f"Error fetching project data: {e}")
            return {}

    def update_single_data(self, indikator: str, nilai_baru: str, updated_by: str = None) -> bool:
        """Update single project indicator"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Get old value for audit
                cursor.execute("SELECT nilai FROM proyek_data WHERE indikator = ?", (indikator,))
                old_value = cursor.fetchone()

                if old_value:
                    cursor.execute(
                        """UPDATE proyek_data SET nilai = ?, last_updated = CURRENT_TIMESTAMP, updated_by = ? 
                           WHERE indikator = ?""",
                        (str(nilai_baru), updated_by, indikator)
                    )

                    # Log to audit
                    if updated_by:
                        cursor.execute(
                            """INSERT INTO audit_log (user, action, target, old_value, new_value) 
                               VALUES (?, ?, ?, ?, ?)""",
                            (updated_by, "UPDATE", indikator, old_value['nilai'], str(nilai_baru))
                        )

                    conn.commit()
                    logger.info(f"Updated {indikator} by {updated_by}")
                    return True
                else:
                    logger.warning(f"Indicator {indikator} not found")
                    return False

        except sqlite3.Error as e:
            logger.error(f"Error updating data: {e}")
            return False

    def get_user(self, username: str, password: str) -> Optional[Tuple]:
        """Get user by username and password"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username, role, departemen FROM users WHERE username = ? AND password = ? AND is_active = 1",
                    (username, password)
                )
                return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"Error fetching user: {e}")
            return None

    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username, role, departemen, is_active FROM users")
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error fetching users: {e}")
            return []

    def create_user(self, username: str, password: str, role: str, departemen: str) -> bool:
        """Create new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, role, departemen) VALUES (?, ?, ?, ?)",
                    (username, password, role, departemen)
                )
                conn.commit()
                logger.info(f"User {username} created")
                return True
        except sqlite3.IntegrityError:
            logger.warning(f"User {username} already exists")
            return False
        except sqlite3.Error as e:
            logger.error(f"Error creating user: {e}")
            return False

    def get_audit_logs(self, limit: int = 100) -> List[Dict]:
        """Get audit logs"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error fetching audit logs: {e}")
            return []

    def get_inventory_status(self) -> Dict[str, str]:
        """Get current inventory/warehouse status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT indikator, nilai FROM proyek_data WHERE indikator LIKE '%Gudang%' OR indikator LIKE '%Stok%'"
                )
                return {row['indikator']: row['nilai'] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            logger.error(f"Error fetching inventory: {e}")
            return {}

    def get_budget_status(self) -> Dict[str, str]:
        """Get budget and financial status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT indikator, nilai FROM proyek_data WHERE indikator LIKE '%Anggaran%' OR indikator LIKE '%Biaya%'"
                )
                return {row['indikator']: row['nilai'] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            logger.error(f"Error fetching budget: {e}")
            return {}


# Global database manager instance
db_manager = DatabaseManager()

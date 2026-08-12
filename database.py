import sqlite3
import os
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name="north_type.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        self.db_path = os.path.join(data_dir, db_name)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tablo yoksa tamamen yeni oluştur
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shortcuts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shortcut TEXT UNIQUE NOT NULL,
                replacement TEXT NOT NULL,
                category TEXT DEFAULT 'Kişisel',
                is_sensitive INTEGER DEFAULT 0,
                enabled INTEGER DEFAULT 1,
                usage_count INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Eski veritabanlarından geçiş için eksik sütunları güvenli bir şekilde ekle
        columns_to_add = [
            ("category", "TEXT DEFAULT 'Kişisel'"),
            ("is_sensitive", "INTEGER DEFAULT 0"),
            ("enabled", "INTEGER DEFAULT 1"),
            ("usage_count", "INTEGER DEFAULT 0"),
            ("created_at", "TEXT"),
            ("updated_at", "TEXT")
        ]
        
        for col_name, col_def in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE shortcuts ADD COLUMN {col_name} {col_def}")
            except sqlite3.OperationalError:
                pass  # Sütun zaten varsa hatayı yoksay

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shortcut_id INTEGER,
                used_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def get_all_shortcuts(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, shortcut, replacement, category, is_sensitive, enabled, usage_count FROM shortcuts")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_shortcut(self, shortcut, replacement, category='Kişisel', is_sensitive=0):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("""
                INSERT INTO shortcuts (shortcut, replacement, category, is_sensitive, enabled, usage_count, created_at, updated_at)
                VALUES (?, ?, ?, ?, 1, 0, ?, ?)
            """, (shortcut, replacement, category, is_sensitive, now, now))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success

    def update_shortcut(self, shortcut_id, shortcut, replacement, category, is_sensitive):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE shortcuts 
            SET shortcut = ?, replacement = ?, category = ?, is_sensitive = ?, updated_at = ?
            WHERE id = ?
        """, (shortcut, replacement, category, is_sensitive, now, shortcut_id))
        conn.commit()
        conn.close()

    def delete_shortcut(self, shortcut_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shortcuts WHERE id = ?", (shortcut_id,))
        cursor.execute("DELETE FROM usage_logs WHERE shortcut_id = ?", (shortcut_id,))
        conn.commit()
        conn.close()

    def increment_usage(self, shortcut_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE shortcuts SET usage_count = usage_count + 1 WHERE id = ?", (shortcut_id,))
        cursor.execute("INSERT INTO usage_logs (shortcut_id, used_at) VALUES (?, ?)", (shortcut_id, now))
        conn.commit()
        conn.close()

    def get_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(usage_count) FROM shortcuts")
        total_res = cursor.fetchone()
        total_count = total_res[0] if total_res and total_res[0] else 0

        one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("SELECT COUNT(*) FROM usage_logs WHERE used_at >= ?", (one_week_ago,))
        week_res = cursor.fetchone()
        week_count = week_res[0] if week_res and week_res[0] else 0

        cursor.execute("SELECT shortcut, usage_count FROM shortcuts ORDER BY usage_count DESC LIMIT 5")
        top_shortcuts = cursor.fetchall()

        conn.close()
        return total_count, week_count, top_shortcuts
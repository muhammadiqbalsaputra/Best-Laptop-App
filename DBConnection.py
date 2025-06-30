# DBConnection.py
#  Helper koneksi database MySQL / MariaDB (pymysql)
import os
import pymysql
from contextlib import contextmanager

# ---- Konfigurasi ----------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "spk_laptop")
DB_PORT = int(os.getenv("DB_PORT", 3306))

def get_connection():
    """Buat koneksi baru; caller wajib menutup."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )

@contextmanager
def db_cursor():
    """
    Context‑manager satu‑baris:
        with db_cursor() as cur:
            cur.execute(...)
            rows = cur.fetchall()
    Otomatis commit jika tidak ada exception,
    rollback bila ada exception.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

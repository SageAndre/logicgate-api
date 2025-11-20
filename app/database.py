import sqlite3
import logging

DB_NAME = "logicgate.db"
logger = logging.getLogger("logicgate")

def init_db():
    """Initialize the tables"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                id TEXT PRIMARY KEY,
                name TEXT,
                rule TEXT,
                created_at TEXT
            )
        """)
    logger.info("Database initialized.")

def get_db_connection():
    """Helper to get a connection"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn
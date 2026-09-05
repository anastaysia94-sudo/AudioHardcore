from __future__ import annotations
import sqlite3
from pathlib import Path

CURRENT_SCHEMA_VERSION = 2
MIGRATIONS = {
    1: """
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    2: """
    CREATE TABLE IF NOT EXISTS app_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_tracks_updated_at ON tracks(updated_at);
    CREATE INDEX IF NOT EXISTS idx_tracks_play_count ON tracks(play_count);
    """,
}

def migrate(conn: sqlite3.Connection, schema_path: Path) -> None:
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(schema_path.read_text(encoding="utf-8"))
    conn.execute("""CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    current = conn.execute("SELECT COALESCE(MAX(version), 0) FROM schema_migrations").fetchone()[0]
    for version in range(int(current) + 1, CURRENT_SCHEMA_VERSION + 1):
        conn.executescript(MIGRATIONS[version])
        conn.execute("INSERT INTO schema_migrations(version) VALUES (?)", (version,))
    conn.commit()

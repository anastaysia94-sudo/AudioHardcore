from __future__ import annotations
import os, sqlite3
from pathlib import Path
from core.migrations import migrate
ROOT = Path(__file__).resolve().parents[2]

def data_dir() -> Path:
    path = Path(os.environ.get('AUDIOHARDCORE_DATA_DIR', ROOT / '.data')).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path

def db_path() -> Path:
    explicit = os.environ.get('AUDIOHARDCORE_DB')
    if explicit:
        path = Path(explicit).expanduser(); path.parent.mkdir(parents=True, exist_ok=True); return path
    return data_dir() / 'audiohardcore.sqlite3'

SCHEMA = ROOT / 'db' / 'schema.sql'
DB_PATH = ROOT / '.data' / 'audiohardcore.sqlite3'

def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    return conn

def init_db() -> None:
    with connect() as conn:
        migrate(conn, SCHEMA)

def schema_version() -> int:
    with connect() as conn:
        row = conn.execute("SELECT COALESCE(MAX(version), 0) AS version FROM schema_migrations").fetchone()
        return int(row['version'])

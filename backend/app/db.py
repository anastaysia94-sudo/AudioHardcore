from __future__ import annotations
import os, sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def data_dir():
    path=Path(os.environ.get('AUDIOHARDCORE_DATA_DIR',ROOT/'.data')); path.mkdir(parents=True,exist_ok=True); return path
def db_path():
    explicit=os.environ.get('AUDIOHARDCORE_DB')
    if explicit:
        path=Path(explicit).expanduser(); path.parent.mkdir(parents=True,exist_ok=True); return path
    return data_dir()/'audiohardcore.sqlite3'
SCHEMA=ROOT/'db'/'schema.sql'; DB_PATH=ROOT/'.data'/'audiohardcore.sqlite3'
def connect():
    conn=sqlite3.connect(db_path()); conn.row_factory=sqlite3.Row; conn.execute('PRAGMA foreign_keys=ON'); return conn
def init_db():
    with connect() as conn: conn.executescript(SCHEMA.read_text(encoding='utf-8')); conn.commit()

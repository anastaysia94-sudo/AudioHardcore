from __future__ import annotations
from .db import connect

CURRENT_SCHEMA_VERSION = 2

def apply_migrations() -> int:
    with connect() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)')
        versions={r[0] for r in conn.execute('SELECT version FROM schema_migrations')}
        if 1 not in versions: conn.execute('INSERT INTO schema_migrations(version) VALUES (1)')
        if 2 not in versions:
            conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY,email TEXT NOT NULL UNIQUE COLLATE NOCASE,password_hash TEXT NOT NULL,display_name TEXT,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS devices (id TEXT PRIMARY KEY,user_id TEXT NOT NULL,name TEXT NOT NULL,platform TEXT,last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
            CREATE TABLE IF NOT EXISTS sync_changes (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id TEXT NOT NULL,device_id TEXT NOT NULL,entity_type TEXT NOT NULL,entity_id TEXT NOT NULL,field_name TEXT NOT NULL,value_json TEXT NOT NULL,changed_at TEXT NOT NULL,synced_at TEXT,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,FOREIGN KEY(device_id) REFERENCES devices(id) ON DELETE CASCADE);
            CREATE INDEX IF NOT EXISTS idx_sync_changes_user_time ON sync_changes(user_id,changed_at);
            CREATE INDEX IF NOT EXISTS idx_devices_user ON devices(user_id);
            ''')
            conn.execute('INSERT INTO schema_migrations(version) VALUES (2)')
        conn.commit()
    return CURRENT_SCHEMA_VERSION

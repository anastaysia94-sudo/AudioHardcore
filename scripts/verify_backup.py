#!/usr/bin/env python3
"""Validate an AudioHardcore SQLite backup without mutating it."""
from __future__ import annotations
import argparse
import json
import sqlite3
from pathlib import Path

REQUIRED_TABLES={"tracks","playlists","playlist_tracks","file_locations","metadata_backups"}

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("backup",type=Path)
    parser.add_argument("--max-age-hours",type=float,default=None)
    args=parser.parse_args()
    path=args.backup.expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"backup not found: {path}")
    if path.stat().st_size<=0:
        raise SystemExit("backup is empty")
    if args.max_age_hours is not None:
        import time
        age_hours=(time.time()-path.stat().st_mtime)/3600
        if age_hours>args.max_age_hours:
            raise SystemExit(f"backup is stale: {age_hours:.1f}h > {args.max_age_hours:.1f}h")
    uri=f"file:{path.as_posix()}?mode=ro"
    with sqlite3.connect(uri,uri=True) as conn:
        integrity=conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity!="ok":
            raise SystemExit(f"SQLite integrity_check failed: {integrity}")
        tables={row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        missing=sorted(REQUIRED_TABLES-tables)
        if missing:
            raise SystemExit(f"backup missing required tables: {', '.join(missing)}")
        track_count=conn.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
        playlist_count=conn.execute("SELECT COUNT(*) FROM playlists").fetchone()[0]
    print(json.dumps({"status":"ok","backup":str(path),"size_bytes":path.stat().st_size,"tracks":track_count,"playlists":playlist_count,"integrity":"ok"},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

from pathlib import Path
import sqlite3,tempfile
from core.library import iter_audio_files,file_sha256
def test_audio_extension_filtering():
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);(root/'a.mp3').write_bytes(b'x');(root/'b.txt').write_text('x');(root/'sub').mkdir();(root/'sub'/'c.flac').write_bytes(b'x');assert {p.name for p in iter_audio_files(root)}=={'a.mp3','c.flac'}
def test_sha256_is_deterministic():
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp)/'a.mp3';p.write_bytes(b'AudioHardcore');assert file_sha256(p)==file_sha256(p)
def test_schema_loads_and_foreign_keys_exist():
 schema=Path(__file__).parents[1]/'db'/'schema.sql'
 with sqlite3.connect(':memory:') as conn:
  conn.executescript(schema.read_text());names={r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")};assert {'tracks','artists','albums','file_locations'}<=names

from pathlib import Path
import tempfile
from mutagen.id3 import ID3
from core.metadata import write_mp3_metadata
def test_mp3_metadata_write_creates_backup_and_writes_title():
 with tempfile.TemporaryDirectory() as tmp:
  path=Path(tmp)/'test.mp3';path.write_bytes(b'not-real-audio-but-id3-will-be-created');result=write_mp3_metadata(path,{'title':'AudioHardcore Test'});assert Path(result.backup_path).exists();assert ID3(path)['TIT2'].text[0]=='AudioHardcore Test'

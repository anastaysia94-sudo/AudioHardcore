from __future__ import annotations
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import ID3, ID3NoHeaderError, APIC, Frames
except ImportError:
    MutagenFile=None; ID3=None; ID3NoHeaderError=Exception; APIC=None; Frames={}
@dataclass(slots=True)
class MetadataWriteResult:
    path:str; backup_path:str; fields_written:list[str]; artwork_written:bool
def _artwork_from_audio(audio):
    if audio is None or not getattr(audio,'tags',None): return None
    for key in audio.tags.keys():
        ks=str(key)
        if ks.startswith('APIC:'): return bytes(audio.tags[key].data)
        if ks=='covr':
            v=audio.tags[key]; return bytes(v[0] if isinstance(v,(list,tuple)) else v)
    return None
def read_artwork(path:Path):
    if MutagenFile is None: raise RuntimeError('Mutagen is not installed')
    return _artwork_from_audio(MutagenFile(path,easy=False))
def write_mp3_metadata(path:Path,fields:dict[str,str|None],artwork:bytes|None=None)->MetadataWriteResult:
    if ID3 is None: raise RuntimeError('Mutagen is not installed')
    path=path.resolve()
    if not path.exists() or not path.is_file(): raise FileNotFoundError(path)
    if path.suffix.lower()!='.mp3': raise ValueError('Safe write-back currently supports MP3 only')
    backup_dir=path.parent/'.audiohardcore-backups'; backup_dir.mkdir(parents=True,exist_ok=True)
    timestamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'); backup_path=backup_dir/f'{path.name}.{timestamp}.bak'; shutil.copy2(path,backup_path)
    try:
        try: tags=ID3(path)
        except ID3NoHeaderError: tags=ID3()
        mapping={'title':'TIT2','artist':'TPE1','album':'TALB','album_artist':'TPE2','genre':'TCON','year':'TDRC','track_number':'TRCK','disc_number':'TPOS'}
        written=[]
        for field,frame in mapping.items():
            if field in fields:
                value=fields[field]; tags.delall(frame)
                if value not in (None,''): tags.add(Frames[frame](encoding=3,text=[str(value)]))
                written.append(field)
        artwork_written=False
        if artwork is not None:
            tags.delall('APIC:'); tags.add(APIC(encoding=3,mime='image/jpeg',type=3,desc='AudioHardcore',data=artwork)); artwork_written=True
        tags.save(path); return MetadataWriteResult(str(path),str(backup_path),written,artwork_written)
    except Exception:
        shutil.copy2(backup_path,path); raise

from __future__ import annotations
import hashlib, os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
try:
    from mutagen import File as MutagenFile
except ImportError:
    MutagenFile = None
AUDIO_EXTENSIONS={'.mp3','.m4a','.flac','.aac','.ogg','.opus','.wav','.alac'}
def _first_tag(tags,*names):
    if not tags:return None
    for name in names:
        value=tags.get(name)
        if value is not None and value!='':
            if hasattr(value,'text'): value=value.text
            if isinstance(value,(list,tuple)): return str(value[0]) if value else None
            if isinstance(value,bytes): return value.decode('utf-8',errors='replace')
            return str(value)
    return None
def file_sha256(path:Path,chunk_size:int=1024*1024)->str:
    digest=hashlib.sha256()
    with path.open('rb') as handle:
        while chunk:=handle.read(chunk_size): digest.update(chunk)
    return digest.hexdigest()
@dataclass(slots=True)
class TrackRecord:
    track_id:str; path:str; filename:str; size_bytes:int; modified_ns:int; sha256:str
    title:str|None=None; artist:str|None=None; album:str|None=None; album_artist:str|None=None
    genre:str|None=None; year:str|None=None; track_number:str|None=None; disc_number:str|None=None
    duration_seconds:float|None=None; has_artwork:bool=False; metadata_error:str|None=None
    def to_dict(self)->dict:return asdict(self)
def parse_file(path:Path,compute_hash:bool=True)->TrackRecord:
    stat=path.stat(); sha=file_sha256(path) if compute_hash else ''
    stable_id=sha or hashlib.sha256(str(path.resolve()).encode()).hexdigest()
    record=TrackRecord(stable_id,str(path.resolve()),path.name,stat.st_size,stat.st_mtime_ns,sha)
    if MutagenFile is None: record.metadata_error='Mutagen is not installed'; return record
    try:
        audio=MutagenFile(path,easy=False)
        if audio is None: record.metadata_error='Unsupported or unreadable audio format'; return record
        tags=audio.tags
        record.title=_first_tag(tags,'TIT2','title','©nam'); record.artist=_first_tag(tags,'TPE1','artist','©ART')
        record.album=_first_tag(tags,'TALB','album','©alb'); record.album_artist=_first_tag(tags,'TPE2','albumartist','aART')
        record.genre=_first_tag(tags,'TCON','genre','©gen'); record.year=_first_tag(tags,'TDRC','date','year','©day')
        record.track_number=_first_tag(tags,'TRCK','tracknumber','trkn'); record.disc_number=_first_tag(tags,'TPOS','discnumber','disk')
        record.duration_seconds=float(audio.info.length) if getattr(audio,'info',None) and getattr(audio.info,'length',None) else None
        if tags: record.has_artwork=any(str(k).startswith('APIC:') or k in ('covr','metadata_block_picture') for k in tags.keys())
    except Exception as exc: record.metadata_error=f'{type(exc).__name__}: {exc}'
    return record
def iter_audio_files(root:Path)->Iterable[Path]:
    if root.is_file() and root.suffix.lower() in AUDIO_EXTENSIONS: yield root; return
    for dirpath,_,filenames in os.walk(root):
        for filename in filenames:
            path=Path(dirpath)/filename
            if path.suffix.lower() in AUDIO_EXTENSIONS: yield path
def scan_library(root:str|Path,compute_hash:bool=True)->list[TrackRecord]:
    base=Path(root).expanduser().resolve()
    if not base.exists(): raise FileNotFoundError(base)
    if not base.is_dir() and base.suffix.lower() not in AUDIO_EXTENSIONS: raise ValueError(f'Not an audio file or directory: {base}')
    return [parse_file(path,compute_hash) for path in iter_audio_files(base)]

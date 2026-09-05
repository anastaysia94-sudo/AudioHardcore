from __future__ import annotations
import mimetypes, shutil, sys, time
from contextlib import asynccontextmanager
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import FileResponse,Response
from pydantic import BaseModel,Field
from backend.app.db import connect,db_path,init_db
from core.library import scan_library
from core.metadata import read_artwork,write_mp3_metadata
WEB_ROOT=ROOT/'web'
@asynccontextmanager
async def lifespan(app:FastAPI): init_db(); yield
app=FastAPI(title='AudioHardcore API',version='0.6.0',description='Free/open-source local-first music library API.',lifespan=lifespan)
class ScanRequest(BaseModel): path:str=Field(min_length=1); compute_hash:bool=True
class MetadataUpdate(BaseModel):
 title:str|None=None; artist:str|None=None; album:str|None=None; album_artist:str|None=None; genre:str|None=None; year:str|None=None; track_number:str|None=None; disc_number:str|None=None
class TrackControlUpdate(BaseModel): is_favorite:bool|None=None; rating:int|None=Field(default=None,ge=1,le=5)
class PlaylistCreate(BaseModel): name:str=Field(min_length=1,max_length=200); description:str|None=None
class PlaylistUpdate(BaseModel): name:str|None=Field(default=None,min_length=1,max_length=200); description:str|None=None
class PlaylistTrackAdd(BaseModel): track_id:str
class PathDelete(BaseModel): path:str=Field(min_length=1)
class BackupRequest(BaseModel): destination:str=Field(min_length=1)
class RestoreRequest(BaseModel): source:str=Field(min_length=1)
@app.get('/',include_in_schema=False)
def home(): return FileResponse(WEB_ROOT/'index.html')
@app.get('/health')
def health():
 with connect() as conn: count=conn.execute('SELECT COUNT(*) FROM tracks').fetchone()[0]
 return {'status':'ok','service':'audiohardcore-api','version':app.version,'track_count':count}
def _track_row(track_id):
 with connect() as conn:return conn.execute('SELECT * FROM tracks WHERE id=?',(track_id,)).fetchone()
def _ensure_track(track_id):
 row=_track_row(track_id)
 if row is None: raise HTTPException(status_code=404,detail='Track not found')
 return row
@app.get('/library/tracks')
def list_tracks(q:str|None=Query(default=None),favorite:bool|None=Query(default=None),rating:int|None=Query(default=None,ge=1,le=5),limit:int=Query(default=100,ge=1,le=1000),offset:int=Query(default=0,ge=0)):
 clauses=[]; args=[]
 if q: clauses.append('(title LIKE ? OR artist LIKE ? OR album LIKE ? OR genre LIKE ? OR filename LIKE ?)'); args += [f'%{q}%']*5
 if favorite is not None: clauses.append('is_favorite=?'); args.append(1 if favorite else 0)
 if rating is not None: clauses.append('rating=?'); args.append(rating)
 where=' WHERE '+' AND '.join(clauses) if clauses else ''
 sql='SELECT * FROM tracks'+where+" ORDER BY is_favorite DESC, COALESCE(artist,''), COALESCE(album,''), CAST(COALESCE(NULLIF(track_number,''),'0') AS INTEGER), COALESCE(title,'') LIMIT ? OFFSET ?"
 with connect() as conn:
  rows=[dict(r) for r in conn.execute(sql,[*args,limit,offset]).fetchall()]; total=conn.execute('SELECT COUNT(*) FROM tracks'+where,args).fetchone()[0]
 return {'tracks':rows,'total':total,'limit':limit,'offset':offset}
@app.post('/library/tracks/{track_id}/play')
def record_play(track_id):
 _ensure_track(track_id)
 with connect() as conn: conn.execute('UPDATE tracks SET play_count=play_count+1,updated_at=CURRENT_TIMESTAMP WHERE id=?',(track_id,)); conn.execute('INSERT INTO play_history(track_id) VALUES (?)',(track_id,)); conn.commit()
 return get_track(track_id)
@app.delete('/library/by-path')
def delete_by_path(payload:PathDelete):
 normalized=str(Path(payload.path).expanduser().resolve())
 with connect() as conn:
  row=conn.execute('SELECT id FROM tracks WHERE path=?',(normalized,)).fetchone()
  if not row:return {'status':'not_found'}
  conn.execute('DELETE FROM tracks WHERE id=?',(row['id'],)); conn.execute('DELETE FROM file_locations WHERE path=?',(normalized,)); conn.commit()
 return {'status':'deleted','track_id':row['id']}
@app.post('/backup')
def backup_library(payload:BackupRequest):
 dest=Path(payload.destination).expanduser().resolve(); dest.parent.mkdir(parents=True,exist_ok=True); src=db_path();
 if not src.exists(): init_db()
 shutil.copy2(src,dest); return {'status':'ok','destination':str(dest),'size_bytes':dest.stat().st_size}
@app.post('/restore')
def restore_library(payload:RestoreRequest):
 src=Path(payload.source).expanduser().resolve()
 if not src.exists() or not src.is_file(): raise HTTPException(status_code=400,detail='Backup file does not exist')
 target=db_path(); pre=target.with_suffix(target.suffix+'.pre-restore-'+time.strftime('%Y%m%d-%H%M%S')+'.bak')
 if target.exists(): shutil.copy2(target,pre)
 shutil.copy2(src,target); return {'status':'ok','pre_restore_backup':str(pre),'source':str(src)}
@app.get('/library/stats')
def library_stats():
 with connect() as conn:
  tracks=conn.execute('SELECT COUNT(*) FROM tracks').fetchone()[0]; artists=conn.execute("SELECT COUNT(DISTINCT artist) FROM tracks WHERE artist IS NOT NULL AND artist!=''").fetchone()[0]; albums=conn.execute("SELECT COUNT(DISTINCT album) FROM tracks WHERE album IS NOT NULL AND album!=''").fetchone()[0]; seconds=conn.execute('SELECT COALESCE(SUM(duration_seconds),0) FROM tracks').fetchone()[0]; favorites=conn.execute('SELECT COUNT(*) FROM tracks WHERE is_favorite=1').fetchone()[0]; rated=conn.execute('SELECT COUNT(*) FROM tracks WHERE rating IS NOT NULL').fetchone()[0]
 return {'tracks':tracks,'artists':artists,'albums':albums,'duration_seconds':seconds,'favorites':favorites,'rated':rated}
@app.get('/library/duplicates')
def duplicates():
 with connect() as conn:
  groups=conn.execute("SELECT sha256,COUNT(*) count FROM tracks WHERE sha256!='' GROUP BY sha256 HAVING COUNT(*)>1 ORDER BY count DESC").fetchall(); result=[]
  for g in groups:
   rows=conn.execute('SELECT id,path,filename,size_bytes,title,artist,album FROM tracks WHERE sha256=? ORDER BY path',(g['sha256'],)).fetchall(); result.append({'sha256':g['sha256'],'count':g['count'],'tracks':[dict(r) for r in rows]})
 return {'groups':result,'duplicate_track_count':sum(x['count'] for x in result)}
@app.get('/library/tracks/{track_id}')
def get_track(track_id): return dict(_ensure_track(track_id))
@app.patch('/library/tracks/{track_id}')
def update_track(track_id,update:MetadataUpdate):
 _ensure_track(track_id); values=update.model_dump(exclude_unset=True)
 if not values:return get_track(track_id)
 sets=', '.join(f'{k}=?' for k in values)
 with connect() as conn: conn.execute(f'UPDATE tracks SET {sets},updated_at=CURRENT_TIMESTAMP WHERE id=?',[*values.values(),track_id]); conn.commit()
 return get_track(track_id)
@app.patch('/library/tracks/{track_id}/control')
def update_track_control(track_id,update:TrackControlUpdate):
 _ensure_track(track_id); values=update.model_dump(exclude_unset=True)
 if not values:return get_track(track_id)
 sets=', '.join(f'{k}=?' for k in values)
 with connect() as conn: conn.execute(f'UPDATE tracks SET {sets},updated_at=CURRENT_TIMESTAMP WHERE id=?',[*values.values(),track_id]); conn.commit()
 return get_track(track_id)
@app.get('/media/{track_id}')
def media(track_id):
 row=_ensure_track(track_id); path=Path(row['path'])
 if not path.exists() or not path.is_file(): raise HTTPException(status_code=404,detail='Audio file is missing from disk')
 return FileResponse(path,media_type=mimetypes.guess_type(path.name)[0] or 'application/octet-stream',filename=row['filename'])
@app.get('/library/tracks/{track_id}/artwork')
def track_artwork(track_id):
 row=_ensure_track(track_id)
 try:data=read_artwork(Path(row['path']))
 except Exception as exc:raise HTTPException(status_code=400,detail=str(exc)) from exc
 if not data:raise HTTPException(status_code=404,detail='No embedded artwork')
 return Response(content=data,media_type='image/jpeg')
@app.post('/library/tracks/{track_id}/write-back')
def write_back(track_id,update:MetadataUpdate):
 row=_ensure_track(track_id)
 try:result=write_mp3_metadata(Path(row['path']),update.model_dump(exclude_unset=True))
 except (FileNotFoundError,ValueError,RuntimeError) as exc:raise HTTPException(status_code=400,detail=str(exc)) from exc
 with connect() as conn:conn.execute('INSERT INTO metadata_backups(track_id,source_path,backup_path) VALUES (?,?,?)',(track_id,result.path,result.backup_path));conn.commit()
 refreshed=scan_library(result.path,compute_hash=True)[0]; data=refreshed.to_dict()
 with connect() as conn:conn.execute('UPDATE tracks SET path=?,filename=?,size_bytes=?,modified_ns=?,sha256=?,title=?,artist=?,album=?,album_artist=?,genre=?,year=?,track_number=?,disc_number=?,duration_seconds=?,has_artwork=?,metadata_error=?,updated_at=CURRENT_TIMESTAMP WHERE id=?',(data['path'],data['filename'],data['size_bytes'],data['modified_ns'],data['sha256'],data['title'],data['artist'],data['album'],data['album_artist'],data['genre'],data['year'],data['track_number'],data['disc_number'],data['duration_seconds'],int(data['has_artwork']),data['metadata_error'],track_id));conn.commit()
 return {'status':'ok','backup_path':result.backup_path,'fields_written':result.fields_written,'track':get_track(track_id)}
@app.post('/library/scan')
def scan(request:ScanRequest):
 try:records=scan_library(request.path,compute_hash=request.compute_hash)
 except (FileNotFoundError,ValueError) as exc:raise HTTPException(status_code=400,detail=str(exc)) from exc
 with connect() as conn:
  for record in records:
   d=record.to_dict(); conn.execute('''INSERT INTO tracks (id,path,filename,size_bytes,modified_ns,sha256,title,artist,album,album_artist,genre,year,track_number,disc_number,duration_seconds,has_artwork,metadata_error) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET path=excluded.path,filename=excluded.filename,size_bytes=excluded.size_bytes,modified_ns=excluded.modified_ns,sha256=excluded.sha256,title=excluded.title,artist=excluded.artist,album=excluded.album,album_artist=excluded.album_artist,genre=excluded.genre,year=excluded.year,track_number=excluded.track_number,disc_number=excluded.disc_number,duration_seconds=excluded.duration_seconds,has_artwork=excluded.has_artwork,metadata_error=excluded.metadata_error,updated_at=CURRENT_TIMESTAMP''',tuple(d.values())); conn.execute('''INSERT INTO file_locations(track_id,path,filename,size_bytes,modified_ns) VALUES (?,?,?,?,?) ON CONFLICT(path) DO UPDATE SET track_id=excluded.track_id,filename=excluded.filename,size_bytes=excluded.size_bytes,modified_ns=excluded.modified_ns,last_seen_at=CURRENT_TIMESTAMP''',(d['track_id'],d['path'],d['filename'],d['size_bytes'],d['modified_ns']))
  conn.commit()
 return {'scanned':len(records),'errors':sum(1 for r in records if r.metadata_error),'track_ids':[r.track_id for r in records]}
@app.post('/playlists')
def create_playlist(payload:PlaylistCreate):
 with connect() as conn: cur=conn.execute('INSERT INTO playlists(name,description) VALUES (?,?)',(payload.name.strip(),payload.description)); conn.commit(); return dict(conn.execute('SELECT * FROM playlists WHERE id=?',(cur.lastrowid,)).fetchone())
@app.get('/playlists')
def list_playlists():
 with connect() as conn:return [dict(r) for r in conn.execute('SELECT p.*,COUNT(pt.track_id) track_count FROM playlists p LEFT JOIN playlist_tracks pt ON pt.playlist_id=p.id GROUP BY p.id ORDER BY p.name COLLATE NOCASE').fetchall()]
@app.get('/playlists/{playlist_id}')
def get_playlist(playlist_id):
 with connect() as conn:
  p=conn.execute('SELECT * FROM playlists WHERE id=?',(playlist_id,)).fetchone()
  if p is None:raise HTTPException(status_code=404,detail='Playlist not found')
  tracks=conn.execute('SELECT t.* FROM playlist_tracks pt JOIN tracks t ON t.id=pt.track_id WHERE pt.playlist_id=? ORDER BY pt.position,t.title',(playlist_id,)).fetchall()
  return {'playlist':dict(p),'tracks':[dict(r) for r in tracks]}
@app.patch('/playlists/{playlist_id}')
def update_playlist(playlist_id,payload:PlaylistUpdate):
 get_playlist(playlist_id); values=payload.model_dump(exclude_unset=True)
 if not values:return get_playlist(playlist_id)['playlist']
 sets=', '.join(f'{k}=?' for k in values)
 with connect() as conn:conn.execute(f'UPDATE playlists SET {sets},updated_at=CURRENT_TIMESTAMP WHERE id=?',[*values.values(),playlist_id]);conn.commit()
 return get_playlist(playlist_id)['playlist']
@app.delete('/playlists/{playlist_id}')
def delete_playlist(playlist_id):
 get_playlist(playlist_id)
 with connect() as conn:conn.execute('DELETE FROM playlists WHERE id=?',(playlist_id,));conn.commit()
 return {'status':'deleted','playlist_id':playlist_id}
@app.post('/playlists/{playlist_id}/tracks')
def add_playlist_track(playlist_id,payload:PlaylistTrackAdd):
 get_playlist(playlist_id);_ensure_track(payload.track_id)
 with connect() as conn:pos=conn.execute('SELECT COALESCE(MAX(position)+1,0) FROM playlist_tracks WHERE playlist_id=?',(playlist_id,)).fetchone()[0];conn.execute('INSERT OR IGNORE INTO playlist_tracks(playlist_id,track_id,position) VALUES (?,?,?)',(playlist_id,payload.track_id,pos));conn.commit()
 return get_playlist(playlist_id)
@app.delete('/playlists/{playlist_id}/tracks/{track_id}')
def remove_playlist_track(playlist_id,track_id):
 get_playlist(playlist_id)
 with connect() as conn:
  row=conn.execute('SELECT position FROM playlist_tracks WHERE playlist_id=? AND track_id=?',(playlist_id,track_id)).fetchone()
  if row is not None:conn.execute('DELETE FROM playlist_tracks WHERE playlist_id=? AND track_id=?',(playlist_id,track_id));conn.execute('UPDATE playlist_tracks SET position=position-1 WHERE playlist_id=? AND position>?',(playlist_id,row['position']));conn.commit()
 return get_playlist(playlist_id)

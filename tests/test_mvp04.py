from fastapi.testclient import TestClient
from backend.app.db import connect,init_db
from backend.app.main import app
def seed(tmp_path,monkeypatch):
 db=tmp_path/'ah.sqlite3';monkeypatch.setenv('AUDIOHARDCORE_DB',str(db));init_db()
 with connect() as conn:conn.execute('INSERT INTO tracks(id,path,filename,size_bytes,modified_ns,sha256,title,artist,album,duration_seconds) VALUES(?,?,?,?,?,?,?,?,?,?)',('t1',str(tmp_path/'song.mp3'),'song.mp3',10,1,'abc','Song','Artist','Album',120.0));conn.commit()
def test_favorite_filter_and_stats(tmp_path,monkeypatch):
 seed(tmp_path,monkeypatch);client=TestClient(app);r=client.patch('/library/tracks/t1/control',json={'is_favorite':True,'rating':5});assert r.status_code==200;assert r.json()['is_favorite']==1;assert client.get('/library/tracks?favorite=true').json()['total']==1;assert client.get('/library/stats').json()['favorites']==1
def test_playlist_crud(tmp_path,monkeypatch):
 seed(tmp_path,monkeypatch);client=TestClient(app);p=client.post('/playlists',json={'name':'Mix'}).json();pid=p['id'];assert client.post(f'/playlists/{pid}/tracks',json={'track_id':'t1'}).status_code==200;assert len(client.get(f'/playlists/{pid}').json()['tracks'])==1;assert client.patch(f'/playlists/{pid}',json={'name':'Mix 2'}).json()['name']=='Mix 2';assert client.delete(f'/playlists/{pid}').status_code==200;assert client.get(f'/playlists/{pid}').status_code==404

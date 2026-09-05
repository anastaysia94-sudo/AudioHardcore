from __future__ import annotations
import json,os,shutil,subprocess,sys,threading,urllib.error,urllib.parse,urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import filedialog,messagebox,simpledialog,ttk
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from core.watcher import LibraryWatcher
API='http://127.0.0.1:8765'
def api(method,path,payload=None):
 data=None if payload is None else json.dumps(payload).encode(); req=urllib.request.Request(API+path,data=data,method=method,headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=6) as r: body=r.read(); return json.loads(body.decode()) if body else {}
 except urllib.error.HTTPError as exc:
  try:detail=json.loads(exc.read().decode()).get('detail',str(exc))
  except Exception:detail=str(exc)
  raise RuntimeError(detail) from exc
class AudioHardcoreDesktop(tk.Tk):
 def __init__(self):
  super().__init__();self.title('AudioHardcore');self.geometry('1360x820');self.minsize(1100,680);self.configure(bg='#111318');self.watcher=None;self.track_rows=[];self._style();self._ui();self.after(250,self._refresh);self.protocol('WM_DELETE_WINDOW',self._close)
 def _style(self):
  s=ttk.Style(self)
  try:s.theme_use('clam')
  except tk.TclError:pass
  s.configure('TFrame',background='#111318');s.configure('Panel.TFrame',background='#191c22');s.configure('TLabel',background='#111318',foreground='#eceff4',font=('Segoe UI',10));s.configure('Title.TLabel',font=('Segoe UI',22,'bold'),foreground='#fff');s.configure('Sub.TLabel',foreground='#a9afbb');s.configure('TButton',font=('Segoe UI',10,'bold'),padding=(12,7));s.configure('Treeview',background='#171a20',fieldbackground='#171a20',foreground='#f4f5f7',rowheight=35);s.configure('Treeview.Heading',background='#20242d',foreground='#f7f7f7');s.map('Treeview',background=[('selected','#394352')],foreground=[('selected','#fff')])
 def _ui(self):
  top=ttk.Frame(self,padding=(20,18));top.pack(fill='x');ttk.Label(top,text='AudioHardcore',style='Title.TLabel').pack(side='left');ttk.Label(top,text='  Your music. Your library. Your world.',style='Sub.TLabel').pack(side='left',pady=(8,0));self.search=tk.StringVar();e=ttk.Entry(top,textvariable=self.search,width=42);e.pack(side='right',padx=(10,0));e.bind('<Return>',lambda _e:self.refresh_tracks());ttk.Button(top,text='Search',command=self.refresh_tracks).pack(side='right')
  body=ttk.Frame(self);body.pack(fill='both',expand=True,padx=16);nav=ttk.Frame(body,style='Panel.TFrame',padding=14);nav.pack(side='left',fill='y',padx=(0,12))
  for text,cmd in [('Library',self.show_all),('Favorites',lambda:self.set_filter('favorite=true')),('5-Star',lambda:self.set_filter('rating=5')),('Duplicates',self.show_duplicates),('Import Folder',self.import_folder),('Backup Library',self.backup_library),('Restore Backup',self.restore_backup)]:ttk.Button(nav,text=text,command=cmd,width=19).pack(fill='x',pady=4)
  ttk.Label(nav,text='LIVE LIBRARY WATCH',style='Sub.TLabel').pack(anchor='w',pady=(22,4));self.watch_label=ttk.Label(nav,text='Not watching',style='Sub.TLabel',wraplength=170);self.watch_label.pack(anchor='w');ttk.Button(nav,text='Watch Folder…',command=self.choose_watch).pack(fill='x',pady=(8,4));ttk.Button(nav,text='Stop Watcher',command=self.stop_watch).pack(fill='x')
  center=ttk.Frame(body);center.pack(side='left',fill='both',expand=True);self.stats=ttk.Label(center,text='Loading…',style='Sub.TLabel');self.stats.pack(anchor='w',pady=(0,10));cols=('title','artist','album','genre','rating','favorite','duration');self.tree=ttk.Treeview(center,columns=cols,show='headings',selectmode='browse');head={'title':'Title','artist':'Artist','album':'Album','genre':'Genre','rating':'★','favorite':'♥','duration':'Time'};width={'title':280,'artist':170,'album':210,'genre':120,'rating':55,'favorite':55,'duration':80}
  for c in cols:self.tree.heading(c,text=head[c]);self.tree.column(c,width=width[c],anchor='w')
  self.tree.pack(fill='both',expand=True);self.tree.bind('<Double-1>',self.play_selected);self.tree.bind('<Button-3>',self.track_menu)
  player=ttk.Frame(self,style='Panel.TFrame',padding=12);player.pack(fill='x',padx=16,pady=16);self.now=ttk.Label(player,text='Nothing playing',font=('Segoe UI',11,'bold'));self.now.pack(side='left')
  for text,cmd in [('▶ Play',self.play_selected),('♥ Favorite',self.favorite_selected),('★ Rate',self.rate_selected),('Edit Metadata',self.edit_selected),('Add to Playlist',self.add_selected_to_playlist)]:ttk.Button(player,text=text,command=cmd).pack(side='right',padx=4)
 def _refresh(self):
  try:self._stats();self.refresh_tracks()
  except Exception as exc:self.stats.config(text=f'API not ready: {exc}')
  self.after(8000,self._stats)
 def _stats(self):
  try:
   s=api('GET','/library/stats');h=s['duration_seconds']/3600 if s['duration_seconds'] else 0;self.stats.config(text=f"{s['tracks']} tracks  •  {s['artists']} artists  •  {s['albums']} albums  •  {h:.1f} hours  •  {s['favorites']} favorites")
  except Exception:pass
  self.after(8000,self._stats)
 def refresh_tracks(self,query=None):
  path='/library/tracks?limit=1000';q=query if query is not None else self.search.get().strip()
  if q:path+='&'+q if '=' in q and q.split('=',1)[0] in {'favorite','rating'} else '&q='+urllib.parse.quote(q)
  data=api('GET',path);self.tree.delete(*self.tree.get_children());self.track_rows=data['tracks']
  for r in self.track_rows:self.tree.insert('','end',iid=r['id'],values=(r.get('title') or r['filename'],r.get('artist') or '',r.get('album') or '',r.get('genre') or '',r.get('rating') or '','♥' if r.get('is_favorite') else '',self._fmt(r.get('duration_seconds'))))
 def _fmt(self,s):
  if s is None:return '—'
  s=int(s);return f'{s//60}:{s%60:02d}'
 def show_all(self):self.search.set('');self.refresh_tracks()
 def set_filter(self,q):self.search.set('');self.refresh_tracks(q)
 def selected(self):
  ids=self.tree.selection()
  if not ids:messagebox.showinfo('AudioHardcore','Select a track first.');return None
  return next((r for r in self.track_rows if r['id']==ids[0]),None)
 def play_selected(self):
  r=self.selected()
  if not r:return
  p=r['path']
  if not Path(p).exists():messagebox.showerror('Missing file',p);return
  self.now.config(text=f"▶ {r.get('title') or r['filename']} — {r.get('artist') or 'Unknown artist'}")
  try:
   if os.name=='nt':os.startfile(p)
   elif sys.platform=='darwin':subprocess.Popen(['open',p])
   elif shutil.which('ffplay'):subprocess.Popen(['ffplay','-nodisp','-autoexit','-loglevel','quiet',p],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   else:subprocess.Popen(['xdg-open',p],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   api('POST',f"/library/tracks/{r['id']}/play")
  except Exception as exc:messagebox.showerror('Playback',str(exc))
 def favorite_selected(self):
  r=self.selected()
  if r:api('PATCH',f"/library/tracks/{r['id']}/control",{'is_favorite':not bool(r.get('is_favorite'))});self.refresh_tracks()
 def rate_selected(self):
  r=self.selected()
  if not r:return
  v=simpledialog.askinteger('Rating','Rate this track 1–5 stars:',minvalue=1,maxvalue=5,initialvalue=r.get('rating') or 5,parent=self)
  if v is not None:api('PATCH',f"/library/tracks/{r['id']}/control",{'rating':v});self.refresh_tracks()
 def edit_selected(self):
  r=self.selected()
  if r:Editor(self,r)
 def add_selected_to_playlist(self):
  r=self.selected()
  if not r:return
  ps=api('GET','/playlists')['playlists'];choice=simpledialog.askstring('Playlist','Enter existing playlist name or a new name:\n\n'+(', '.join(p['name'] for p in ps) if ps else 'No playlists yet'),parent=self)
  if not choice:return
  p=next((p for p in ps if p['name'].lower()==choice.lower()),None) or api('POST','/playlists',{'name':choice});api('POST',f"/playlists/{p['id']}/tracks",{'track_id':r['id']});messagebox.showinfo('Playlist',f"Added to {p['name']}")
 def track_menu(self,event):
  item=self.tree.identify_row(event.y)
  if not item:return
  self.tree.selection_set(item);m=tk.Menu(self,tearoff=False)
  for label,cmd in [('Play',self.play_selected),('Favorite',self.favorite_selected),('Rate',self.rate_selected),('Edit metadata',self.edit_selected),('Add to playlist',self.add_selected_to_playlist)]:m.add_command(label=label,command=cmd)
  m.tk_popup(event.x_root,event.y_root)
 def import_folder(self):
  f=filedialog.askdirectory(title='Import music folder')
  if f:
   try:r=api('POST','/library/scan',{'path':f,'compute_hash':True});messagebox.showinfo('Import complete',f"Scanned {r['scanned']} audio files.\nMetadata errors: {r['errors']}");self.refresh_tracks()
   except Exception as exc:messagebox.showerror('Import',str(exc))
 def choose_watch(self):
  f=filedialog.askdirectory(title='Choose folder to watch')
  if not f:return
  self.stop_watch();self.watcher=LibraryWatcher(f,self._on_watch_changes);self.watcher.start();self.watch_label.config(text=f'Watching:\n{f}')
 def _on_watch_changes(self,changes):
  def work():
   for p in changes['added']+changes['modified']:
    try:api('POST','/library/scan',{'path':p,'compute_hash':True})
    except Exception:pass
   for p in changes['removed']:
    try:api('DELETE','/library/by-path',{'path':p})
    except Exception:pass
   self.after(0,self.refresh_tracks)
  threading.Thread(target=work,daemon=True).start()
 def stop_watch(self):
  if self.watcher:self.watcher.stop()
  self.watcher=None;self.watch_label.config(text='Not watching')
 def backup_library(self):
  t=filedialog.asksaveasfilename(title='Save AudioHardcore backup',defaultextension='.ahbackup',filetypes=[('AudioHardcore Backup','*.ahbackup')])
  if t:
   try:r=api('POST','/backup',{'destination':t});messagebox.showinfo('Backup',f"Backup created:\n{r['destination']}")
   except Exception as exc:messagebox.showerror('Backup',str(exc))
 def restore_backup(self):
  s=filedialog.askopenfilename(title='Choose AudioHardcore backup',filetypes=[('AudioHardcore Backup','*.ahbackup'),('All files','*.*')])
  if not s:return
  if not messagebox.askyesno('Restore','Restore the library database from this backup? The current database will be backed up first.'):return
  try:r=api('POST','/restore',{'source':s});messagebox.showinfo('Restore',f"Restored. Previous DB backup:\n{r['pre_restore_backup']}\n\nRestart AudioHardcore to fully reload all state.");self.refresh_tracks()
  except Exception as exc:messagebox.showerror('Restore',str(exc))
 def show_duplicates(self):
  try:d=api('GET','/library/duplicates')
  except Exception as exc:messagebox.showerror('Duplicates',str(exc));return
  if not d['groups']:messagebox.showinfo('Duplicates','No duplicate content hashes found.');return
  lines=[]
  for g in d['groups'][:20]:lines.append(f"{g['count']} copies: {g['sha256'][:14]}…");lines += ['  '+t['path'] for t in g['tracks']]
  messagebox.showinfo('Duplicate content','\n'.join(lines))
 def _close(self):self.stop_watch();self.destroy()
class Editor(tk.Toplevel):
 FIELDS=['title','artist','album','album_artist','genre','year','track_number','disc_number']
 def __init__(self,parent,row):
  super().__init__(parent);self.title('Edit Metadata — AudioHardcore');self.row=row;self.vars={};f=ttk.Frame(self,padding=18);f.pack(fill='both',expand=True)
  for i,k in enumerate(self.FIELDS):ttk.Label(f,text=k.replace('_',' ').title()).grid(row=i,column=0,sticky='w',pady=4);v=tk.StringVar(value=row.get(k) or '');self.vars[k]=v;ttk.Entry(f,textvariable=v,width=52).grid(row=i,column=1,pady=4)
  ttk.Button(f,text='Save to database',command=self.save_db).grid(row=8,column=0,pady=12);ttk.Button(f,text='Write tags + backup',command=self.write_tags).grid(row=8,column=1,pady=12)
 def values(self):return {k:v.get() for k,v in self.vars.items()}
 def save_db(self):
  try:api('PATCH',f"/library/tracks/{self.row['id']}",self.values());self.master.refresh_tracks();self.destroy()
  except Exception as exc:messagebox.showerror('Metadata',str(exc),parent=self)
 def write_tags(self):
  try:r=api('POST',f"/library/tracks/{self.row['id']}/write-back",self.values());self.master.refresh_tracks();self.destroy();messagebox.showinfo('Metadata',f"Tags written safely.\nBackup: {r['backup_path']}",parent=self.master)
  except Exception as exc:messagebox.showerror('Metadata',str(exc),parent=self)
def main():AudioHardcoreDesktop().mainloop()
if __name__=='__main__':main()

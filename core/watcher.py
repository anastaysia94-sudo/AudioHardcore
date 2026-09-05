from __future__ import annotations
import os, threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable
from core.library import AUDIO_EXTENSIONS
@dataclass(frozen=True,slots=True)
class FileState:
    path:str; size_bytes:int; modified_ns:int
class LibraryWatcher:
    def __init__(self,root,on_changes:Callable[[dict[str,list[str]]],None],interval:float=2.5):
        self.root=Path(root).expanduser().resolve(); self.on_changes=on_changes; self.interval=max(.5,float(interval)); self._stop=threading.Event(); self._thread=None; self._snapshot={}
    def _iter_audio(self)->Iterable[Path]:
        if self.root.is_file() and self.root.suffix.lower() in AUDIO_EXTENSIONS: yield self.root; return
        if not self.root.exists(): return
        for dirpath,_,filenames in os.walk(self.root):
            for filename in filenames:
                p=Path(dirpath)/filename
                if p.suffix.lower() in AUDIO_EXTENSIONS: yield p
    def snapshot(self):
        state={}
        for path in self._iter_audio():
            try: st=path.stat()
            except OSError: continue
            resolved=str(path.resolve()); state[resolved]=FileState(resolved,st.st_size,st.st_mtime_ns)
        return state
    def scan_once(self):
        current=self.snapshot(); old=self._snapshot
        changes={'added':sorted(set(current)-set(old)),'removed':sorted(set(old)-set(current)),'modified':sorted(p for p in set(current)&set(old) if current[p].size_bytes!=old[p].size_bytes or current[p].modified_ns!=old[p].modified_ns)}
        self._snapshot=current
        if any(changes.values()): self.on_changes(changes)
        return changes
    def start(self,initial_snapshot=True):
        if self._thread and self._thread.is_alive(): return
        self._stop.clear(); self._snapshot=self.snapshot() if initial_snapshot else {}; self._thread=threading.Thread(target=self._run,name='AudioHardcoreWatcher',daemon=True); self._thread.start()
    def _run(self):
        while not self._stop.wait(self.interval):
            try:self.scan_once()
            except Exception:continue
    def stop(self):
        self._stop.set()
        if self._thread and self._thread.is_alive(): self._thread.join(timeout=min(self.interval+.5,3.0))
        self._thread=None

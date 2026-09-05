from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
cmd=[sys.executable,'-m','uvicorn','backend.app.main:app','--host','127.0.0.1','--port','8765']
raise SystemExit(subprocess.call(cmd,cwd=ROOT))

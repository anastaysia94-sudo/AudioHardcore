param([string]$InstallDir="$env:LOCALAPPDATA\AudioHardcore")
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force -Path $InstallDir|Out-Null
Copy-Item -Path (Join-Path $Root '*') -Destination $InstallDir -Recurse -Force
$py=Get-Command python -ErrorAction SilentlyContinue
if(-not $py){throw 'Python 3.11+ is required.'}
& $py.Source -m pip install --user -r (Join-Path $InstallDir 'backend\requirements.txt')
$desktop=Join-Path $InstallDir 'run_desktop.bat'
$ws=New-Object -ComObject WScript.Shell
$shortcut=$ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'AudioHardcore.lnk'))
$shortcut.TargetPath=$desktop;$shortcut.WorkingDirectory=$InstallDir;$shortcut.Description='AudioHardcore free music library';$shortcut.Save()
Write-Host "AudioHardcore installed to $InstallDir"

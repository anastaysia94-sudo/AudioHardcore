param([switch]$OneFolder)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$py=Get-Command python -ErrorAction SilentlyContinue
if(-not $py){throw 'Python is required.'}
& $py.Source -m pip install pyinstaller
$args=@('-m','PyInstaller','--noconfirm','--clean','--name','AudioHardcore','--windowed','--paths','.', 'run_audiohardcore_desktop.py')
if(-not $OneFolder){$args+='--onefile'}
& $py.Source @args
Write-Host 'Build complete. See dist\AudioHardcore.exe (or dist\AudioHardcore folder).'

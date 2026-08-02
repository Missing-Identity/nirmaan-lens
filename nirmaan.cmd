@echo off
setlocal

where pwsh.exe >nul 2>&1
if errorlevel 1 goto WindowsPowerShell

pwsh.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\nirmaan.ps1" %*
exit /b %errorlevel%

:WindowsPowerShell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\nirmaan.ps1" %*
exit /b %errorlevel%

@echo off
cd /d "%~dp0"
python tools\build_index.py
if errorlevel 1 exit /b 1
python app\server.py

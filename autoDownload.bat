@echo off
call activate autoDownload-env
cd /d %~dp0
python autodownload.py

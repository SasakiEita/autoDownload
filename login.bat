@echo off
call activate autoDownload-env
cd /d %~dp0
python ./sources/login.py

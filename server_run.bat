@echo off
set python=%cd%\venv\Scripts\python.exe
cd Server
:go
cls
%python% Libmanager_server.py
:input
set /p o="Press r to restart"
if %o% == r goto go 
pause
exit
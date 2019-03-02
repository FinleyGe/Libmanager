@echo off
set python=%cd%\venv\Scripts\python.exe
cd Client
:go
cls
%python% Python_Client.py
:input
set /p o="Press r to restart"
if %o% == r goto go 
pause
exit
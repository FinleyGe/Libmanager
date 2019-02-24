echo off
set sqlite=%cd%\sqlite\sqlite3.exe
set database=%cd%\Server\database.db
:go
%sqlite% %database%
pause
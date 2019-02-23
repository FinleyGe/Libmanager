echo 按任意键修改环境变量
pause
set python="%cd%\venv\Scripts"
setx /m path "path;%python%"
pause
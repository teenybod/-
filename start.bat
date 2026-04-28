@echo off
chcp 65001 >nul
echo ==========================================
echo     制药车间滤芯更换管理系统
echo ==========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
if not exist "venv" (
    echo [1/3] 正在创建虚拟环境...
    python -m venv venv
)

echo [2/3] 正在安装依赖...
venv\Scripts\pip install -r requirements.txt -q

echo [3/3] 正在启动系统...
echo.
echo 启动成功后，请在浏览器中访问：
echo   本机：http://localhost:5000
echo   局域网：http://%COMPUTERNAME%:5000 或本机IP:5000
echo.
echo 按 Ctrl+C 停止运行
echo ==========================================
venv\Scripts\python app.py

pause

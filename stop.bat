@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ==========================================
echo     停止物料效期管理系统
echo ==========================================
echo.

REM 查找并结束 Flask 进程
tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2>nul | findstr /I "app.py" >nul
if %errorlevel% == 0 (
    echo 正在停止后台运行的 Flask 进程...
    for /f "tokens=2 delims=," %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV ^| findstr /I "app.py"') do (
        set "PID=%%a"
        set "PID=!PID:"=!"
        taskkill /PID !PID! /F >nul 2>&1
        echo [✓] 已停止进程 PID: !PID!
    )
) else (
    echo 未检测到正在运行的 Flask 进程
)

echo.
pause

@echo off
chcp 65001 >nul
echo ==========================================
echo     设置开机自动启动
echo ==========================================
echo.

REM 获取当前目录
set "PROJECT_DIR=%~dp0"
set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

REM 启动文件夹路径（当前用户）
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM 创建快捷方式（使用 VBScript）
set "VBS_FILE=%TEMP%\create_shortcut.vbs"
(
echo Set WshShell = CreateObject("WScript.Shell"^)
echo Set oLink = WshShell.CreateShortcut("%STARTUP_DIR%\物料效期管理系统.lnk"^)
echo oLink.TargetPath = "%PROJECT_DIR%\start_silent.vbs"
echo oLink.WorkingDirectory = "%PROJECT_DIR%"
echo oLink.Description = "制药车间滤芯更换管理系统"
echo oLink.IconLocation = "shell32.dll,14"
echo oLink.Save
echo Set oLink = Nothing
echo Set WshShell = Nothing
) > "%VBS_FILE%"

cscript //nologo "%VBS_FILE%"
del "%VBS_FILE%"

echo.
echo [✓] 已添加到开机启动项
echo 启动位置：%STARTUP_DIR%\物料效期管理系统.lnk
echo.
echo 说明：
echo   - 下次开机系统会自动在后台启动本程序
echo   - 不需要再手动运行 start.bat
echo   - 直接浏览器访问 http://localhost:5000/ 即可
echo.
echo 如需取消开机启动，请删除上述快捷方式
echo.
pause

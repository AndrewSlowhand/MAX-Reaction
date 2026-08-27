@echo off
setlocal
cd /d "%~dp0"

if not exist "dist\MAX_Reaction\MAX_Reaction.exe" (
    echo Run build.bat first.
    pause
    exit /b 1
)

set "OUT=MAX_Reaction_Portable_READY_v1.3.zip"
if exist "%OUT%" del /q "%OUT%"

powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path 'dist\MAX_Reaction\*' -DestinationPath '%OUT%' -Force"

if errorlevel 1 (
    echo Failed to create ZIP.
    pause
    exit /b 1
)

echo.
echo READY: %CD%\%OUT%
echo Contains EXE + Chromium + BAT files.
echo.
pause

@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo MAX Reaction Portable 1.3 - build
echo ============================================================

where py >nul 2>nul
if errorlevel 1 (
    echo Python is required only on the build PC.
    echo Install Python and run build.bat again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" py -m venv .venv
call ".venv\Scripts\activate.bat"

python -m pip install --upgrade pip
python -m pip install playwright pyinstaller

set "PLAYWRIGHT_BROWSERS_PATH=%CD%\ms-playwright"
python -m playwright install chromium

if not exist "ms-playwright" (
    echo ERROR: Chromium was not downloaded.
    pause
    exit /b 1
)

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

pyinstaller --noconfirm --clean --onedir --name MAX_Reaction reaction.py
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

xcopy /e /i /y "ms-playwright" "dist\MAX_Reaction\ms-playwright" >nul
copy /y "daily.bat" "dist\MAX_Reaction\daily.bat" >nul
copy /y "login.bat" "dist\MAX_Reaction\login.bat" >nul
if exist "daily_hidden.vbs" copy /y "daily_hidden.vbs" "dist\MAX_Reaction\daily_hidden.vbs" >nul

if exist "package_portable.bat" copy /y "package_portable.bat" "dist\MAX_Reaction\package_portable.bat" >nul

>"dist\MAX_Reaction\VERSION.txt" echo MAX Reaction Portable 1.3

echo.
echo ============================================================
echo BUILD COMPLETE: dist\MAX_Reaction
echo ============================================================
echo Python is NOT required on the target PC.
echo Chromium is included in ms-playwright.
echo.
pause

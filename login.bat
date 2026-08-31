@echo off
setlocal
cd /d "%~dp0"

set "PROFILE=default"
if not "%~2"=="" set "PROFILE=%~2"

if not exist "bot_url.txt" (
    echo ERROR: bot_url.txt not found.
    pause
    exit /b 1
)

set /p BOT_URL=<bot_url.txt
if "%BOT_URL%"=="" (
    echo ERROR: enter the MAX Web URL in bot_url.txt
    pause
    exit /b 1
)

set "PLAYWRIGHT_BROWSERS_PATH=%~dp0ms-playwright"

echo Starting MAX Web...
echo URL: %BOT_URL%
echo Profile: %PROFILE%
echo.

MAX_Reaction.exe "%BOT_URL%" both --profile "%PROFILE%" --headed

echo.
echo Finished.
pause

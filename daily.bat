@echo off
setlocal
cd /d "%~dp0"

set "MODE=both"
set "PROFILE=default"

if not exist "bot_url.txt" exit /b 1
set /p BOT_URL=<bot_url.txt
if "%BOT_URL%"=="" exit /b 1

set "PLAYWRIGHT_BROWSERS_PATH=%~dp0ms-playwright"

MAX_Reaction.exe "%BOT_URL%" "%MODE%" --profile "%PROFILE%"
exit /b %ERRORLEVEL%

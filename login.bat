@echo off
setlocal
cd /d "%~dp0"

set "PROFILE=default"
set "BOT_URL="

rem ------------------------------------------------------------
rem Arguments:
rem   login.bat
rem       -> use URL from bot_url.txt
rem
rem   login.bat "https://max.ru/example_bot"
rem       -> use URL from command line
rem
rem   login.bat "https://max.ru/example_bot" account1
rem       -> use URL from command line and profile account1
rem ------------------------------------------------------------

if not "%~2"=="" set "PROFILE=%~2"

if not "%~1"=="" (
    set "BOT_URL=%~1"
) else (
    if not exist "bot_url.txt" (
        echo ERROR: bot_url.txt not found.
        pause
        exit /b 1
    )

    set /p BOT_URL=<bot_url.txt
)

if "%BOT_URL%"=="" (
    echo ERROR: enter the MAX bot URL in bot_url.txt
    echo or pass it as the first argument.
    pause
    exit /b 1
)

set "PLAYWRIGHT_BROWSERS_PATH=%~dp0ms-playwright"

echo Starting MAX...
echo Bot: %BOT_URL%
echo Profile: %PROFILE%
echo.

MAX_Reaction.exe "%BOT_URL%" both --profile "%PROFILE%" --headed

echo.
echo Finished.
pause

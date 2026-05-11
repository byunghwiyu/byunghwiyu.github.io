@echo off
REM ================================================================
REM  Double-click to publish a new LinkedIn post to byunghwiyu.github.io
REM
REM  Usage:
REM    1) Double-click this file (publish.bat)
REM    2) Paste LinkedIn post URL, press Enter
REM    3) Korean / English title prompts appear (in Python).
REM       Just press Enter to accept the auto-suggested series title.
REM    4) Done. Live within 1-2 minutes.
REM
REM  Note: This batch file deliberately contains ASCII only.
REM        All Korean prompts are emitted by Python via UTF-8 stdout.
REM ================================================================

chcp 65001 >nul 2>&1
cd /d "%~dp0"
set "PYTHONIOENCODING=utf-8"

echo.
echo ================================================================
echo   LinkedIn Post Publisher  -  byunghwiyu.github.io
echo ================================================================
echo.

set "URL=%~1"
if not defined URL (
    set /p "URL=Paste LinkedIn URL and press Enter: "
)

if not defined URL (
    echo.
    echo [X] URL required.
    echo.
    pause
    exit /b 1
)

echo.
python tools\add-post.py "%URL%" --push
set "EC=%ERRORLEVEL%"

echo.
echo ================================================================
if "%EC%"=="0" (
    echo   [DONE]  Live in 1-2 minutes at https://byunghwiyu.github.io/
) else (
    echo   [FAIL]  exit code %EC%
)
echo ================================================================
echo.
pause

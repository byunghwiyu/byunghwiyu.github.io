@echo off
REM ================================================================
REM  새 LinkedIn 포스트를 1번에 발행하는 더블클릭 실행 스크립트
REM
REM  사용법:
REM    1) 이 파일(publish.bat)을 더블클릭
REM    2) LinkedIn 포스트 URL 붙여넣고 Enter
REM    3) 한글 제목 / 영문 제목 (자동 제안 표시 → Enter로 수락 또는 직접 입력)
REM    4) 끝. 1~2분 뒤 https://byunghwiyu.github.io/ 에 반영
REM
REM  자동 처리: id 생성, 날짜 디코딩, og:image 다운로드, posts.json 갱신,
REM             git commit + push
REM ================================================================

chcp 65001 >nul
cd /d "%~dp0"
set "PYTHONIOENCODING=utf-8"

echo.
echo ================================================================
echo   LinkedIn 포스트 발행 (byunghwiyu.github.io)
echo ================================================================
echo.

REM 인자로 URL이 주어진 경우 사용, 아니면 인터랙티브 입력
set "URL=%~1"
if not defined URL (
    echo LinkedIn 포스트 URL을 붙여넣고 Enter ^(취소: Ctrl+C^):
    set /p "URL=URL: "
)

if not defined URL (
    echo.
    echo [X] URL이 필요합니다.
    echo.
    pause
    exit /b 1
)

echo.
python tools\add-post.py "%URL%" --push
set "EXITCODE=%ERRORLEVEL%"

echo.
echo ================================================================
if "%EXITCODE%"=="0" (
    echo   [완료]  1~2분 후 https://byunghwiyu.github.io/ 에 반영됩니다.
) else (
    echo   [실패]  exit code %EXITCODE%
)
echo ================================================================
echo.
pause

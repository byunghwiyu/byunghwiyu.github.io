# 새 LinkedIn 포스트 추가 + 자동 배포 원샷 (PowerShell 래퍼)
#
# 사용 예:
#   .\tools\publish.ps1                    # 인터랙티브 (URL/제목 입력 받음)
#   .\tools\publish.ps1 "URL"              # URL 만 인자로
#   .\tools\publish.ps1 "URL" "한글 제목"  # 한글 제목 직접 지정
#
# 동작:
#   1. tools/add-post.py 실행 (썸네일 자동 다운로드, posts.json 갱신)
#   2. git add → commit → push 자동
#   3. 1~2분 후 https://byunghwiyu.github.io/ 에 반영

$ErrorActionPreference = "Stop"

# 스크립트 위치 기준으로 repo 루트 이동
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

# UTF-8 인코딩으로 파이썬 stdout 출력 (한글 깨짐 방지)
$env:PYTHONIOENCODING = "utf-8"

# URL 인자가 없으면 인터랙티브 입력
$urlArg = $args[0]
if (-not $urlArg) {
    $urlArg = Read-Host "LinkedIn 포스트 URL"
    if (-not $urlArg) {
        Write-Host "X URL이 필요합니다" -ForegroundColor Red
        exit 1
    }
}

# add-post.py 호출 (--push 자동 포함)
$pyArgs = @("tools/add-post.py", $urlArg)
if ($args.Count -ge 2) { $pyArgs += $args[1] }
if ($args.Count -ge 3) { $pyArgs += $args[2] }
$pyArgs += "--push"

python @pyArgs

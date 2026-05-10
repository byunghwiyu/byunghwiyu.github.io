"""
새 LinkedIn 포스트를 1줄로 추가합니다.

사용 예:
    # 인터랙티브 (한글 제목만 입력 받음, 나머지 자동)
    python tools/add-post.py "https://www.linkedin.com/posts/byunghwi_..."

    # 한글 제목 직접 지정
    python tools/add-post.py URL "9번째 느좋 코딩 포스트모텀(바이브 코딩)"

    # 한·영 제목 모두 지정
    python tools/add-post.py URL "한글 제목" "English Title"

    # 추가 후 자동 commit + push
    python tools/add-post.py URL --push

자동 처리:
    - id 생성 (post-NNN 다음 번호)
    - 날짜 디코딩 (LinkedIn activity ID 기반)
    - og:image 다운로드 → assets/thumbs/{id}.jpg
    - 시리즈 패턴 감지해서 제목 기본값 제안
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "posts.json"
THUMBS_DIR = ROOT / "assets" / "thumbs"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


# ---------- HTTP / parsing helpers ----------

def http_get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def find_meta(html: str, prop: str) -> str | None:
    pattern = (
        rf'<meta[^>]+(?:property|name)=["\']{re.escape(prop)}["\'][^>]+content=["\']([^"\']+)["\']'
    )
    m = re.search(pattern, html)
    if not m:
        pattern = (
            rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']{re.escape(prop)}["\']'
        )
        m = re.search(pattern, html)
    return m.group(1).replace("&amp;", "&") if m else None


def detect_ext(img_url: str) -> str:
    path = urlparse(img_url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        if path.endswith(ext):
            return ext
    return ".jpg"


# ---------- LinkedIn URL parsing ----------

ACTIVITY_RE = re.compile(r"activity-(\d+)")


def extract_activity_id(url: str) -> int | None:
    m = ACTIVITY_RE.search(url)
    return int(m.group(1)) if m else None


def decode_date(activity_id: int) -> str:
    ts_ms = activity_id >> 22
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


# ---------- posts.json helpers ----------

ID_RE = re.compile(r"^post-(\d+)$")
SERIES_KO_RE = re.compile(r"^(\d+)\s*번째\s+느좋\s*코딩\s*포스트모텀\(바이브\s*코딩\)$")
SERIES_EN_RE = re.compile(r"^Vibe\s+Coding\s+Postmortem\s+#(\d+)$")


def next_id(posts: list[dict]) -> str:
    nums = [int(m.group(1)) for p in posts if (m := ID_RE.match(p.get("id", "")))]
    return f"post-{(max(nums, default=0) + 1):03d}"


def suggest_series_titles(posts: list[dict]) -> tuple[str, str]:
    """기존 시리즈 패턴이 있으면 다음 번호를 제안."""
    ko_nums = [int(m.group(1)) for p in posts if (m := SERIES_KO_RE.match(p.get("titleKo", "")))]
    en_nums = [int(m.group(1)) for p in posts if (m := SERIES_EN_RE.match(p.get("titleEn", "")))]
    next_ko = (max(ko_nums) + 1) if ko_nums else None
    next_en = (max(en_nums) + 1) if en_nums else None
    ko_default = f"{next_ko}번째 느좋 코딩 포스트모텀(바이브 코딩)" if next_ko else ""
    en_default = f"Vibe Coding Postmortem #{next_en}" if next_en else ""
    return ko_default, en_default


def url_already_exists(posts: list[dict], url: str) -> str | None:
    aid = extract_activity_id(url)
    for p in posts:
        if extract_activity_id(p.get("url", "")) == aid:
            return p.get("id")
    return None


# ---------- Thumbnail download ----------

def fetch_thumbnail(post_url: str, post_id: str) -> str | None:
    try:
        html = http_get(post_url).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ! HTML fetch 실패: {e}")
        return None
    og_img = find_meta(html, "og:image")
    if not og_img:
        print("  ! og:image 메타가 없습니다")
        return None
    ext = detect_ext(og_img)
    rel_path = f"assets/thumbs/{post_id}{ext}"
    abs_path = ROOT / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = http_get(og_img)
    except Exception as e:
        print(f"  ! 이미지 다운로드 실패: {e}")
        return None
    abs_path.write_bytes(data)
    print(f"  + 썸네일 저장: {rel_path}  ({len(data)//1024}KB)")
    return rel_path


# ---------- Git ----------

def run_git(args: list[str]) -> int:
    return subprocess.call(["git", *args], cwd=ROOT)


def git_publish(post_id: str, title: str) -> bool:
    print("\n[git] 변경사항 stage/commit/push 진행...")
    if run_git(["add", "posts.json", "assets/thumbs/"]) != 0:
        return False
    msg = f"Add post: {title} ({post_id})"
    if run_git(["commit", "-m", msg]) != 0:
        return False
    if run_git(["push"]) != 0:
        return False
    print("[git] 완료")
    return True


# ---------- Interactive prompts ----------

def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        ans = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        ans = ""
    return ans or default


# ---------- Main ----------

def main(argv: list[str]) -> int:
    args = list(argv)
    push = False
    if "--push" in args:
        push = True
        args.remove("--push")

    if not args:
        print(__doc__)
        return 1

    url = args[0]
    title_ko_arg = args[1] if len(args) > 1 else None
    title_en_arg = args[2] if len(args) > 2 else None

    if not url.startswith("http"):
        print(f"X 잘못된 URL: {url}")
        return 1

    activity_id = extract_activity_id(url)
    if activity_id is None:
        print("X URL에서 activity-... 부분을 찾지 못했습니다")
        return 1

    with JSON_PATH.open("r", encoding="utf-8") as f:
        meta = json.load(f)
    posts: list[dict] = meta.setdefault("posts", [])

    existing_id = url_already_exists(posts, url)
    if existing_id:
        print(f"! 이미 등록된 URL입니다 (id={existing_id}). 스킵.")
        return 0

    pid = next_id(posts)
    date = decode_date(activity_id)
    ko_default, en_default = suggest_series_titles(posts)

    title_ko = title_ko_arg if title_ko_arg is not None else ask("한글 제목", ko_default)
    if not title_ko:
        print("X 한글 제목은 필수입니다")
        return 1
    title_en = title_en_arg if title_en_arg is not None else ask("영문 제목 (선택)", en_default)

    print()
    print(f"  id      = {pid}")
    print(f"  date    = {date}  (activity ID 기반)")
    print(f"  titleKo = {title_ko}")
    if title_en:
        print(f"  titleEn = {title_en}")
    print()

    thumb_path = fetch_thumbnail(url, pid)

    new_entry = {
        "id": pid,
        "date": date,
        "tag": "Postmortem",
        "titleKo": title_ko,
        "titleEn": title_en or "",
        "summary": "",
        "kind": "external",
        "url": url,
        "thumbnail": thumb_path or "",
    }
    posts.insert(0, new_entry)

    with JSON_PATH.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"+ posts.json 저장 완료 ({len(posts)}개 포스트)")

    if push:
        ok = git_publish(pid, title_ko)
        return 0 if ok else 2
    else:
        print("\n다음 명령으로 배포:")
        print("  git add posts.json assets/thumbs/ && git commit -m \"Add post\" && git push")
        print("또는 다음번엔 --push 옵션을 붙여서 한 번에:")
        print(f'  python tools/add-post.py "URL" --push')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

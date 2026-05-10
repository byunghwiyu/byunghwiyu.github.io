"""
LinkedIn 포스트의 og:image 를 가져와 assets/thumbs/ 에 저장하고
posts.json 의 thumbnail 필드를 채운다.

사용법:
    cd D:\\byunghwiyu.github.io
    python tools/fetch-thumbs.py            # 비어있는 thumbnail 만 처리
    python tools/fetch-thumbs.py --force    # 전체 재다운로드 (LinkedIn URL 변경 등)
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "posts.json"
THUMBS_DIR = ROOT / "assets" / "thumbs"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def http_get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def find_og_image(html: str) -> str | None:
    m = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        html,
    )
    if not m:
        m = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            html,
        )
    return m.group(1).replace("&amp;", "&") if m else None


def detect_ext(img_url: str) -> str:
    path = urlparse(img_url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        if path.endswith(ext):
            return ext
    # LinkedIn feedshare는 보통 jpeg
    return ".jpg"


def fetch_one(post: dict, force: bool) -> bool:
    pid = post.get("id", "")
    if post.get("kind") != "external":
        return False
    if post.get("thumbnail") and not force:
        return False
    url = post.get("url", "")
    if not url.startswith("http"):
        return False

    try:
        html = http_get(url).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  X {pid}: HTML fetch failed - {e}")
        return False

    og = find_og_image(html)
    if not og:
        print(f"  ? {pid}: og:image not found")
        return False

    ext = detect_ext(og)
    rel_path = f"assets/thumbs/{pid}{ext}"
    abs_path = ROOT / rel_path

    try:
        data = http_get(og)
    except Exception as e:
        print(f"  X {pid}: image download failed - {e}")
        return False

    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_bytes(data)
    post["thumbnail"] = rel_path
    print(f"  O {pid}  ->  {rel_path}  ({len(data)//1024}KB)")
    return True


def main(argv: list[str]) -> int:
    force = "--force" in argv
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)

    with JSON_PATH.open("r", encoding="utf-8") as f:
        meta = json.load(f)

    print(f"Fetching og:image for {len(meta['posts'])} posts (force={force})...")
    updated = 0
    for p in meta["posts"]:
        if fetch_one(p, force):
            updated += 1

    if updated > 0:
        with JSON_PATH.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"\n{updated} thumbnail(s) updated. posts.json saved.")
    else:
        print("\nNo updates. posts.json unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

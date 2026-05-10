# byunghwiyu.github.io

**StarbornWorks** — 유병휘의 작업 아카이브 허브 페이지.
Personal hub page for Byunghwi Yu's writings & works.

🌐 Live: https://byunghwiyu.github.io/

---

## 무엇인가 / What is this

LinkedIn 포스팅에 매번 기존 작업물 링크를 줄줄이 붙이지 않기 위해 만든 **단일 허브 페이지**.
LinkedIn 본문에는 이 도메인 한 줄만 박으면 됨.

A single hub page so LinkedIn posts don't need to repeat the same backlog of links every time.

---

## 새 포스트 추가하기 / Adding a new post

이 사이트는 **두 종류의 글**을 지원합니다:

- **`external`** — LinkedIn 등 외부 URL로 링크 (기본)
- **`local`** — 사이트 자체에 호스팅하는 마크다운 글

### 1. LinkedIn 링크 추가 (external) — 가장 빠른 길

**제일 쉬운 방법: `publish.bat` 더블클릭**

1. 탐색기에서 `D:\byunghwiyu.github.io\publish.bat` 더블클릭
2. URL 붙여넣고 Enter
3. 한글/영문 제목은 시리즈 패턴 감지된 기본값을 그대로 Enter로 수락하거나 직접 입력
4. 끝. 1~2분 뒤 라이브 반영

자동 처리:
- `id`, `date` (LinkedIn activity ID 디코딩), 썸네일 (og:image 다운로드)
- 다음 번호 제목 자동 제안 (예: `9번째 느좋 코딩 포스트모텀(바이브 코딩)`)
- `posts.json` 갱신 + git commit + push

**터미널을 선호하면:**

```powershell
# PowerShell
.\tools\publish.ps1 "URL"
.\tools\publish.ps1 "URL" "한글 제목" "English Title"

# CMD / 더블클릭
publish.bat "URL"

# Python 직접
python tools\add-post.py "URL" --push
```

### 1-1. 자동 도구 없이 수동 추가하려면

`posts.json` 의 `posts` 배열 최상단에 객체 1개 추가 → 커밋 → 푸시.

```json
{
  "id": "post-003",
  "date": "2026-06-01",
  "tag": "Postmortem",
  "titleKo": "한국어 제목",
  "titleEn": "English Title",
  "summary": "한 줄 요약 / One-line summary.",
  "kind": "external",
  "url": "https://www.linkedin.com/posts/...",
  "thumbnail": ""
}
```

수동 추가 후 썸네일만 자동 채우려면: `python tools/fetch-thumbs.py`

### 2. 사이트 자체 글 추가 (local)

두 단계:

(a) `posts/{id}.md` 파일 생성 — 마크다운 본문 작성
(b) `posts.json` 에 항목 추가 (`kind: "local"`, `url` 불필요)

```json
{
  "id": "first-essay",
  "date": "2026-06-01",
  "tag": "Essay",
  "titleKo": "긴 호흡의 글 제목",
  "titleEn": "A Longer Essay",
  "summary": "한 줄 요약.",
  "kind": "local"
}
```

→ 카드 클릭 시 `post.html?id=first-essay` 로 열림. 글 내용은 `posts/first-essay.md` 에서 자동 로드.

### 필드 설명 / Fields

| 필드 | 설명 |
|---|---|
| `id` | 고유 ID. local 글은 파일명과 동일 (`posts/{id}.md`) |
| `date` | YYYY-MM-DD. 정렬 키 (최신이 위로) |
| `tag` | 한 단어 카테고리 (Postmortem, Devlog, Essay 등) |
| `titleKo` / `titleEn` | 카드 제목 한국어/영문 |
| `summary` | 카드 본문 한 줄 |
| `kind` | `"external"` 또는 `"local"`. 미지정 시 url 기준 자동 판단 |
| `url` | external 글에만 필요. LinkedIn 포스트 URL |
| `thumbnail` | (선택) 카드별 썸네일. 미사용 시 빈 문자열 |

### 마크다운에서 쓸 수 있는 것

- 헤딩 (`##`, `###`), 굵게/기울임, 인라인 코드, 링크
- 코드 블록 (펜스 ```)
- 표 (GFM), 인용 (`>`), 리스트, 이미지
- 자세한 문법: [marked.js docs](https://marked.js.org/)

---

## 로컬에서 확인하기 / Local preview

```bash
cd D:\byunghwiyu.github.io
python -m http.server 8000
```

브라우저에서 http://localhost:8000 열기.

> **주의 / Note**: `index.html` 을 `file://` 로 직접 열면 `fetch('posts.json')` 이 CORS 로 막힘.
> 반드시 로컬 서버를 통해 띄울 것.

---

## 디자인 톤 / Design notes

- StarbornWorks 컨셉: "별에서 태어난 창조물 / Born from stars, crafted as works."
- 다크 테마 + 우주/별빛 모티프 (CSS only, JS 의존 X)
- 한국어 메인 + 영문 병기
- 모든 외부 폰트는 Google Fonts CDN 로드 (Cormorant Garamond, Inter, Noto Sans KR)

---

## 썸네일 / Thumbnails

LinkedIn 포스트 og:image 자동 추출 가능. 새 LinkedIn 글 추가 후:

```bash
python tools/fetch-thumbs.py            # 비어있는 thumbnail 만 처리
python tools/fetch-thumbs.py --force    # 전체 재다운로드
```

→ `assets/thumbs/{id}.jpg` 다운로드 + `posts.json` 의 `thumbnail` 필드 자동 채움.

local 글의 경우 직접 이미지를 `assets/thumbs/` 에 넣고 posts.json `thumbnail` 필드에 경로 기입.

---

## 향후 작업 / TODO

- [ ] `assets/og-image.png` 추가 (1200×630, LinkedIn 카드 미리보기용)
- [ ] `assets/favicon.svg` 디자인 마무리
- [ ] LinkedIn Post Inspector 로 OG 카드 검증
- [ ] (선택) 카드별 썸네일 제작
- [ ] (선택) 커스텀 도메인 연결 (starbornworks.com 등)

---

© 2026 Byunghwi Yu / StarbornWorks

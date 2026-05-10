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

1. `posts.json` 을 연다
2. `posts` 배열 최상단에 객체 1개 추가
3. 커밋 → 푸시 → 끝 (GitHub Pages가 1~2분 내 자동 배포)

```json
{
  "id": "post-003",
  "date": "2026-06-01",
  "tag": "Devlog",
  "titleKo": "한국어 제목",
  "titleEn": "English Title",
  "summary": "한 줄 요약 / One-line summary.",
  "url": "https://www.linkedin.com/posts/...",
  "thumbnail": ""
}
```

### 필드 설명 / Fields

| 필드 | 설명 |
|---|---|
| `id` | 고유 ID (post-001, post-002…) |
| `date` | YYYY-MM-DD. 정렬 키. 최신이 위로 노출됨 |
| `tag` | 한 단어 카테고리 (Postmortem, Devlog, Insight 등) |
| `titleKo` / `titleEn` | 카드 제목 한국어/영문 |
| `summary` | 카드 본문 한 줄 (한영 어느 쪽이든 가능) |
| `url` | LinkedIn 포스트 URL. `#` 로 시작하면 "준비 중"으로 표시 |
| `thumbnail` | (선택) 카드별 썸네일. 미사용 시 빈 문자열 |

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

## 향후 작업 / TODO

- [ ] `assets/og-image.png` 추가 (1200×630, LinkedIn 카드 미리보기용)
- [ ] `assets/favicon.svg` 디자인 마무리
- [ ] LinkedIn Post Inspector 로 OG 카드 검증
- [ ] (선택) 카드별 썸네일 제작
- [ ] (선택) 커스텀 도메인 연결 (starbornworks.com 등)

---

© 2026 Byunghwi Yu / StarbornWorks

# 🧪 30 Days Test Code Mastery

> 백엔드(FastAPI/Python)와 프론트엔드(React/TypeScript) 테스트 코드를 자유자재로 손코딩하기 위한 1개월 일일 자율 학습 레포지토리

---

## 📅 Daily Study Log (학습 일지)

| Day | Date | Category | Target / Topic | One-line Summary | Test File Link |
| :---: | :---: | :---: | :--- | :--- | :---: |
| **Day 01** | 2026-10-07 | Backend | FastAPI & pytest 기초 | `TestClient`로 `GET`/`POST` 기본 요청 및 `isinstance` 방어적 응답 검증 손코딩 완성 | [test_get_drills.py](./backend/tests/test_get_drills.py) |
| Day 02 | - | - | - | - | - |
| Day 03 | - | - | - | - | - |
| Day 04 | - | - | - | - | - |
| Day 05 | - | - | - | - | - |

---

## 📂 디렉터리 구성 안내

```
test-code-mastery/
├── README.md                  # 📌 대시보드 (학습 일지 목차)
├── docs/                      # 💡 핵심 문법 및 치트시트 요약
│   ├── pytest-cheatsheet.md   # pytest, TestClient, Fixture 패턴 모음
│   └── vitest-cheatsheet.md   # Vitest, React Testing Library 패턴 모음
│
├── backend/                   # 🐍 파이썬 테스트 놀이터 (FastAPI + pytest)
│   ├── pyproject.toml         # 의존성 및 pytest 설정
│   ├── src/
│   │   ├── ontology_cases/    # ontology-map 워크스페이스 패턴
│   │   └── train_ticket/      # Fudan Train Ticket 비즈니스 도메인 모의 로직
│   └── tests/
│       ├── conftest.py        # 공통 fixture (TestClient 배달부)
│       ├── test_get_drills.py # 오늘 직접 손코딩한 GET 드릴
│       ├── test_post_drills.py# POST 생성 드릴
│       └── test_ticket_booking.py # 기차표 예매 도메인 테스트
│
└── frontend/                  # ⚡ 타입스크립트 테스트 놀이터 (React + Vitest)
    ├── package.json
    ├── tsconfig.json
    ├── src/
    └── tests/
```

---

## 🏷️ Category 태그 가이드
- `[BE-Basic]` : pytest, TestClient, HTTP Status Code
- `[BE-DB]`    : SQLAlchemy 세션 롤백, Fixture 오버라이드
- `[BE-Domain]`: Train Ticket / 비즈니스 규칙 엣지 케이스 테스트
- `[FE-Basic]` : Vitest, Jest Matcher, 순수 TypeScript 함수 테스트
- `[FE-React]` : 컴포넌트 렌더링, 클릭/입력 이벤트, 상태 변경 검증
- `[FE-Hook]`  : React 커스텀 훅 `renderHook` 테스트

# 🧪 30 Days Test Code Mastery

> 백엔드(FastAPI/Python)와 프론트엔드(React/TypeScript) 테스트 코드를 자유자재로 손코딩하기 위한 1개월 일일 자율 학습 레포지토리

---

## 🎯 학습 레퍼런스 프로젝트 (Reference Projects)

이 스터디 저장소는 단순히 문법만 외우는 것이 아니라, **실제 프로덕트 코드베이스와 유명 오픈소스 도메인을 분석하고 체리피킹**하여 실무 수준의 테스트 코드를 손코딩하는 것을 목표로 합니다.

### 1. `ontology-map-workspace` (현재 개발 중인 주력 프로덕트)
- **기술 스택**: Python(FastAPI) · TypeScript(React) · PostgreSQL · SQLAlchemy 2.0
- **학습 목적**: 실제 개발 중인 워크스페이스 제품의 프로덕션 코드와 테스트 코드를 분석하고 흡수
- **주요 학습 영역**:
  - 사용자 인증 및 격리(`auth`, `session`, `dependency_overrides`)
  - 개인 지도·문서·근거 관리 API (`workspaces`, `documents`, `nodes`, `edges`)
  - Pydantic v2 스키마 유효성 검사 및 엄격한 타입 체킹(`mypy`)
  - React 상태 관리 및 HITL(Human-in-the-loop) 검토 UI 컴포넌트 테스트

### 2. `Train Ticket` (Fudan University SELab / CodeWisdom)
- **원작 배경**: 중국 철도 예매(12306) 시스템을 모방한 푸단대학교의 40+ 마이크로서비스 벤치마크 시스템
- **학습 목적**: 대규모 트랜잭션 서비스의 핵심 비즈니스 도메인 규칙을 체리피킹하여 가벼운 Python/TS로 테스트 작성
- **주요 학습 영역**:
  - 열차 잔여석 조회(`GET 200/404`)
  - 실시간 좌석 차감 및 매진 충돌(`POST 201 Created` vs `409 Conflict`)
  - 네트워크 재시도 대비 중복 예매 방지 멱등성(`request_key` Idempotency) 검증

---

## 📅 Daily Study Log (학습 일지)

| Day | Date | Category | Target / Topic | One-line Summary | Test File Link |
| :---: | :---: | :---: | :--- | :--- | :---: |
| **Day 01** | 2026-10-07 | Backend | ontology-map & FastAPI 기초 | `TestClient`로 `GET`/`POST` 기본 요청 및 `isinstance` 방어적 응답 검증 손코딩 완성 | [GET 드릴](./backend/tests/test_get_drills.py)<br>[POST 드릴](./backend/tests/test_post_drills.py) |
| Day 02 | - | - | - | - | - |
| Day 03 | - | - | - | - | - |
| Day 04 | - | - | - | - | - |
| Day 05 | - | - | - | - | - |

---

## 📂 디렉터리 구성 안내

```
test-code-mastery/
├── README.md                  # 📌 대시보드 (학습 일지 목차 & 레퍼런스 프로젝트 소개)
├── docs/                      # 💡 핵심 문법 및 치트시트 요약
│   ├── pytest-cheatsheet.md   # pytest, TestClient, Fixture 패턴 모음
│   └── vitest-cheatsheet.md   # Vitest, React Testing Library 패턴 모음
│
├── backend/                   # 🐍 파이썬 테스트 놀이터 (FastAPI + pytest)
│   ├── pyproject.toml         # 의존성 및 pytest 설정
│   ├── src/
│   │   ├── ontology_cases/    # 🗺️ ontology-map-workspace 패턴 (워크스페이스, 인증, 세션)
│   │   └── train_ticket/      # 🚄 Fudan Train Ticket 비즈니스 도메인 (예매, 매진, 멱등성)
│   └── tests/
│       ├── conftest.py        # 공통 fixture (TestClient 배달부)
│       ├── test_get_drills.py # [Day 01] GET 기초 및 404/200 손코딩 드릴
│       ├── test_post_drills.py# [Day 01] ontology 워크스페이스 생성 POST 드릴
│       └── test_ticket_booking.py # Train Ticket 기차표 예매/매진/멱등성 도메인 테스트
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
- `[BE-Ontology]`: ontology-map-workspace 아키텍처 및 API 테스트
- `[BE-TrainTicket]`: Train Ticket 도메인 비즈니스 엣지 케이스 테스트
- `[BE-DB]`    : SQLAlchemy 세션 롤백, Fixture 오버라이드
- `[FE-Basic]` : Vitest, Jest Matcher, 순수 TypeScript 함수 테스트
- `[FE-React]` : 컴포넌트 렌더링, 클릭/입력 이벤트, 상태 변경 검증
- `[FE-Hook]`  : React 커스텀 훅 `renderHook` 테스트

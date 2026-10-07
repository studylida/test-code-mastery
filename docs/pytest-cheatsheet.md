# 🐍 Pytest & FastAPI TestClient Cheatsheet

> 테스트 코드 손코딩 시 막힐 때마다 꺼내보는 핵심 공식 모음

---

## 1. 테스트 함수의 3가지 절대 규칙

1. **함수명**: 무조건 `test_`로 시작 (`def test_login() -> None:`)
2. **반환값**: 테스트 함수는 값을 돌려주지 않음 (`-> None`)
3. **단언(검증)**: `assert` 키워드 사용 (`assert 실제값 == 기대값`)

---

## 2. GET 요청 3단계 공식

```python
def test_기능명(client: TestClient) -> None:
    # 1단계: 요청 보내기
    response = client.get("/api/v1/경로")

    # 2단계: 상태 코드 검증
    assert response.status_code == 200

    # 3단계: JSON 파싱 및 방어적 검증
    data = response.json()
    assert isinstance(data, dict)  # 또는 isinstance(data, list)
    assert data["key"] == "expected_value"
```

---

## 3. POST 요청 4단계 공식

```python
def test_생성_기능(client: TestClient) -> None:
    # 1단계: 보낼 데이터(Payload) 준비
    payload = {"name": "새 프로젝트"}

    # 2단계: json= 에 실어서 요청 전송
    response = client.post("/api/v1/workspaces", json=payload)

    # 3단계: 생성 성공 코드(201) 확인
    assert response.status_code == 201

    # 4단계: 생성된 결과물 검증
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "새 프로젝트"
```

---

## 4. Python vs TypeScript 비교 문법 주의사항

| 언어 | 값 비교 | 엄격 비교 | 특수 객체 비교 |
| :--- | :--- | :--- | :--- |
| **Python** | `assert a == b` | *(파이썬에는 `===` 연산자가 없음)* | `assert a is None`<br>`assert a is False` |
| **TypeScript** | `expect(a).toEqual(b)` | `===` 사용 | `toBe(null)` / `toBe(false)` |

---

## 5. 자주 쓰는 HTTP 상태 코드

- **`200 OK`**: 단순 조회(GET), 일반적인 성공
- **`201 Created`**: 새로운 데이터 생성 성공(POST)
- **`400 Bad Request`**: 잘못된 요청 형식
- **`401 Unauthorized`**: 로그인 필요
- **`403 Forbidden`**: 권한 없음 (남의 데이터 열람 불가)
- **`404 Not Found`**: 없는 리소스 또는 존재하지 않는 주소
- **`409 Conflict`**: 중복 충돌 (중복 예매, 중복 이메일 등)
- **`422 Unprocessable Entity`**: Pydantic 유효성 검사 실패 (필수 필드 누락 등)

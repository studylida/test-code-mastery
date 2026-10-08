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

## 4. 422 입력값 검증 정밀 타격 공식 (loc & type)

단순히 `"detail" in data`만 검사하지 않고, 어떤 필드가 왜 틀렸는지 **범인을 특정**하여 검증합니다:

```python
assert response.status_code == 422
data = response.json()
error = data["detail"][0]

# 어느 위치(loc)의 어떤 에러(type)인지 정밀 타격!
assert error["loc"] == ["body", "owner_user_id"]
assert error["type"] == "extra_forbidden"
```

---

## 5. Fixture의 Setup & Teardown (`yield`와 `Generator` 타입의 마법)

`yield`를 품은 Fixture는 **"테스트 전 준비(Setup)"**와 **"테스트 후 청소(Teardown)"**의 제어권을 테스트 함수와 주고받습니다.

### 💡 `Generator[YieldType, SendType, ReturnType]`의 3가지 자리
- **첫 번째 자리 (`YieldType`)**: `yield`로 테스트 함수에 던져주는 값의 타입 (예: `TestClient`, `Session`)
- **두 번째 자리 (`SendType`)**: 밖에서 안으로 찔러넣어 주는 값의 타입 (테스트 Fixture에서는 쓸 일 없으므로 `None`)
- **세 번째 자리 (`ReturnType`)**: 마지막에 진짜로 return하는 값의 타입 (Fixture는 return하지 않으므로 `None`)

```python
@pytest.fixture
def signed_client(client: TestClient) -> Generator[TestClient, None, None]:
    # 👉 [1] Setup: 테스트 전 가짜 로그인 장착
    app.dependency_overrides[get_current_user] = lambda: {"username": "alice"}

    try:
        yield client  # 👈 [2] 테스트 함수에게 제어권을 넘겨주고 여기서 일시 정지!
    finally:
        # 👉 [3] Teardown: 테스트가 성공하든 에러로 폭탄 맞든 100% 무조건 실행!
        app.dependency_overrides.clear()

def test_profile(signed_client: TestClient) -> None:
    # 👉 [2]의 순간에 이 테스트 함수가 실행됩니다!
    response = signed_client.get("/api/v1/profile")
    assert response.status_code == 200
```

---

## 6. 외부 통신 차단 및 몽키 패치 (`monkeypatch`)

테스트 도중 외부 인터넷(결제 API, OpenAI 등)을 실수로 호출하여 과금되거나 테스트가 실패하지 않도록 런타임에 함수를 가로챕니다.

```python
@pytest.fixture
def block_external_http(monkeypatch: pytest.MonkeyPatch) -> None:
    def block(*args: object, **kwargs: object) -> None:
        raise RuntimeError("외부 통신 금지!")

    # httpx.Client.post 호출을 가로채서 block 함수로 바꿔치기
    monkeypatch.setattr("httpx.Client.post", block)

def test_blocked(block_external_http: None) -> None:
    # with pytest.raises(예외클래스) 로 예외 발생 여부 검증
    with pytest.raises(RuntimeError) as exc_info:
        httpx.Client().post("https://api.openai.com/v1/chat")

    assert "외부 통신 금지!" in str(exc_info.value)
```

---

## 7. Python vs TypeScript 비교 문법 주의사항

| 언어 | 값 비교 | 엄격 비교 | 특수 객체 비교 |
| :--- | :--- | :--- | :--- |
| **Python** | `assert a == b` | *(파이썬에는 `===` 연산자가 없음)* | `assert a is None`<br>`assert a is False` |
| **TypeScript** | `expect(a).toEqual(b)` | `===` 사용 | `toBe(null)` / `toBe(false)` |

---

## 8. 자주 쓰는 HTTP 상태 코드

- **`200 OK`**: 단순 조회(GET), 일반적인 성공
- **`201 Created`**: 새로운 데이터 생성 성공(POST)
- **`400 Bad Request`**: 잘못된 요청 형식
- **`401 Unauthorized`**: 인증 실패 (토큰 없음/위조)
- **`403 Forbidden`**: 권한 없음 (남의 데이터 열람 불가)
- **`404 Not Found`**: 없는 리소스 또는 존재하지 않는 주소
- **`409 Conflict`**: 비즈니스 중복 충돌 (중복 예매, 매진 등)
- **`422 Unprocessable Entity`**: Pydantic 유효성 검사 실패 (필수 필드 누락 등)

"""[Day 01~02] Fudan Train Ticket 도메인을 활용한 POST & 엣지 케이스 테스트."""

from uuid import uuid4
from fastapi.testclient import TestClient


def test_book_ticket_success(client: TestClient) -> None:
    """[POST 기본 공식] 잔여석이 있는 열차 예매 시 201 Created 검증."""
    payload = {
        "train_number": "G101",
        "passenger_name": "홍길동",
        "seat_type": "economy",
        "request_key": uuid4().hex,
    }

    # 1. POST 요청 전송
    response = client.post("/api/v1/tickets/book", json=payload)

    # 2. 상태 코드 201 검증
    assert response.status_code == 201

    # 3. 방어적 dict 타입 검증 및 응답 데이터 확인
    data = response.json()
    assert isinstance(data, dict)
    assert data["train_number"] == "G101"
    assert data["passenger_name"] == "홍길동"
    assert data["status"] == "CONFIRMED"
    assert data["price"] == 60000


def test_book_ticket_sold_out_conflict(client: TestClient) -> None:
    """[엣지 케이스] 매진된 열차(K505) 예매 시 409 Conflict 에러 검증."""
    payload = {
        "train_number": "K505",
        "passenger_name": "이몽룡",
        "seat_type": "economy",
    }

    response = client.post("/api/v1/tickets/book", json=payload)

    # 매진 시 409 상태 코드 검증
    assert response.status_code == 409
    data = response.json()
    assert isinstance(data, dict)
    assert data["detail"]["code"] == "SEATS_SOLD_OUT"


def test_book_ticket_idempotency(client: TestClient) -> None:
    """[실무 고급 패턴] 동일한 request_key로 중복 요청 시 중복 예매 방지(멱등성) 검증."""
    same_key = "order_key_abc_123"
    payload = {
        "train_number": "G101",
        "passenger_name": "성춘향",
        "seat_type": "first",
        "request_key": same_key,
    }

    # 첫 번째 예매 요청 -> 201 Created
    first_resp = client.post("/api/v1/tickets/book", json=payload)
    assert first_resp.status_code == 201
    ticket_id = first_resp.json()["ticket_id"]

    # 네트워크 끊김 등으로 사용자가 광클하여 동일 키로 재요청 -> 중복 차감 없이 기존 티켓 반환
    second_resp = client.post("/api/v1/tickets/book", json=payload)
    assert second_resp.status_code == 201
    assert second_resp.json()["ticket_id"] == ticket_id

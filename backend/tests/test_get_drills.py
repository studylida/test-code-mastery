"""[Day 01] 학습자가 직접 손코딩으로 완성한 GET 요청 & 방어적 검증 드릴."""

from fastapi.testclient import TestClient


def test_not_found_endpoint(client: TestClient) -> None:
    """[손코딩 1] 없는 엔드포인트 요청 시 404 Not Found 검증."""
    response = client.get("/api/v1/invalid-path")

    assert response.status_code == 404


def test_get_seat_availability_success(client: TestClient) -> None:
    """[손코딩 2] 정상 열차 조회 시 200 OK 및 방어적 isinstance 검증."""
    response = client.get("/api/v1/tickets/trains/G101/availability")

    # 1. 상태 코드 검증
    assert response.status_code == 200

    # 2. 방어적 타입 검증 (data가 dict인지 확인)
    data = response.json()
    assert isinstance(data, dict)

    # 3. 상세 비즈니스 필드 검증
    assert data["train_number"] == "G101"
    assert data["available_seats"] == 2
    assert data["is_sold_out"] is False


def test_get_seat_availability_not_found(client: TestClient) -> None:
    """[손코딩 3] 존재하지 않는 열차 번호 요청 시 404 에러 검증."""
    response = client.get("/api/v1/tickets/trains/NO_TRAIN_999/availability")

    assert response.status_code == 404
    data = response.json()
    assert isinstance(data, dict)
    assert data["detail"]["code"] == "TRAIN_NOT_FOUND"

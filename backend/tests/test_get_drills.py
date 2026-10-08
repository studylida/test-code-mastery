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


def test_search_workspaces_by_query(client: TestClient) -> None:
    """[손코딩 6] 검색 쿼리 파라미터(params=) 및 리스트 컴프리헨션 in 방어 검증."""
    query = {"q": "연구"}
    response = client.get("/api/v1/workspaces", params=query)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data["total"] == 1

    # 🛡️ 리스트 컴프리헨션 + in 방어 검증: 순서가 바뀌어도, 빈 리스트여도 안전!
    names = [item["name"] for item in data["items"]]
    assert "연구 프로젝트" in names


def test_get_workspace_by_id(client: TestClient) -> None:
    """[손코딩 7] 경로 변수(f-string)를 사용한 단건 상세 조회 및 정밀 검증."""
    target_id = "ws-1"
    response = client.get(f"/api/v1/workspaces/{target_id}")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    # 타겟 ID와 반환된 객체의 ID/이름 검증
    assert data["id"] == target_id
    assert data["name"] == "연구 프로젝트"

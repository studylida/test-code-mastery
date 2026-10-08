"""[Day 01] 학습자가 직접 손코딩으로 완성한 POST 요청 & 생성/보안/Fixture 검증 드릴."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def sample_workspace_payload() -> dict[str, str]:
    """[손코딩 8 Fixture] 반복 사용되는 공통 워크스페이스 요청 데이터 준비물."""
    return {"name": "픽스처 프로젝트"}


def test_create_workspace(client: TestClient) -> None:
    """[손코딩 4] 데이터 생성 POST 요청 및 201 Created 응답 검증."""
    payload = {"name": "연구 프로젝트"}

    response = client.post("/api/v1/workspaces", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "연구 프로젝트"


def test_workspace_create_rejects_extra_fields(client: TestClient) -> None:
    """[손코딩 5] 허용되지 않은 추가 필드(owner_user_id) 전송 시 422 거절 검증."""
    payload = {"name": "New map", "owner_user_id": 999}

    response = client.post("/api/v1/workspaces", json=payload)

    assert response.status_code == 422

    data = response.json()
    assert isinstance(data, dict)
    assert "detail" in data


def test_create_workspace_using_fixture(
    client: TestClient, sample_workspace_payload: dict[str, str]
) -> None:
    """[손코딩 8] @pytest.fixture를 주입받아 POST 요청 및 data.get() 방어 검증."""
    response = client.post("/api/v1/workspaces", json=sample_workspace_payload)

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert data.get("name") == "픽스처 프로젝트"

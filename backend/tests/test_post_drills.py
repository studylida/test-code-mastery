"""[Day 01] 학습자가 직접 손코딩으로 완성한 POST 요청 & 생성 검증 드릴."""

from fastapi.testclient import TestClient


def test_create_workspace(client: TestClient) -> None:
    """[손코딩 4] 데이터 생성 POST 요청 및 201 Created 응답 검증.

    - payload를 json= 인자로 실어 보내기
    - 상태 코드 201 Created 확인
    - isinstance(data, dict) 방어적 검증
    - data["name"] 일치 확인
    """
    payload = {"name": "연구 프로젝트"}

    response = client.post("/api/v1/workspaces", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "연구 프로젝트"

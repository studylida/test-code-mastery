"""[Day 01] 학습자가 직접 손코딩으로 완성한 인증/헤더 & safe signed_client Fixture 드릴."""

from collections.abc import Generator
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
import pytest


def get_current_user() -> dict[str, str]:
    """실제 프로덕션의 인증 의존성 함수 (토큰이 없으면 401 발생)."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": "UNAUTHORIZED", "message": "인증 토큰이 필요합니다."},
    )


# 모의 프로필 앱
auth_app = FastAPI()


@auth_app.get("/api/v1/profile")
def get_profile() -> dict[str, str]:
    # get_current_user()를 의존성으로 호출한다고 가정
    return get_current_user()


@auth_app.get("/api/v1/workspaces")
def get_workspaces() -> dict[str, str]:
    return get_current_user()


@pytest.fixture
def auth_client() -> Generator[TestClient, None, None]:
    with TestClient(auth_app) as client:
        yield client


@pytest.fixture
def signed_client(auth_client: TestClient) -> Generator[TestClient, None, None]:
    """[손코딩 13 Fixture] try...finally와 yield를 사용한 100% 안전한 인증 Fixture."""
    auth_app.dependency_overrides[get_current_user] = lambda: {"username": "alice"}

    try:
        yield auth_client
    finally:
        auth_app.dependency_overrides.clear()


def test_get_workspaces_rejects_invalid_token_header(auth_client: TestClient) -> None:
    """[손코딩 12] 유효하지 않은 가짜 토큰 헤더 전송 시 401 Unauthorized 거절 검증."""
    headers = {"Authorization": "Bearer invalid_secret_token"}
    response = auth_client.get("/api/v1/workspaces", headers=headers)

    assert response.status_code == 401

    data = response.json()
    assert isinstance(data, dict)
    assert "detail" in data


def test_profile_with_safe_signed_client(signed_client: TestClient) -> None:
    """[손코딩 13] 방탄 signed_client Fixture를 사용하여 인증 통과 및 안전한 뒷정리 검증."""
    response = signed_client.get("/api/v1/profile")

    assert response.status_code == 200
    assert response.json()["username"] == "alice"

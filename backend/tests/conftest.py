"""pytest 공통 픽스처 (TestClient 배달부)."""

from collections.abc import Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from ontology_cases.workspaces import router as workspace_router
from train_ticket.booking import router as ticket_router


@pytest.fixture
def app() -> FastAPI:
    """테스트용 FastAPI 애플리케이션 생성."""
    application = FastAPI(title="Test Code Mastery API")
    application.include_router(ticket_router)
    application.include_router(workspace_router)
    return application


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    """모든 테스트 함수에 자동으로 주입되는 가짜 브라우저 client."""
    with TestClient(app) as test_client:
        yield test_client

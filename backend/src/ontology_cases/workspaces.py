"""ontology-map-workspace에서 배운 워크스페이스 생성 미니 API.

[손코딩 4번] POST 요청 테스트를 실제로 실행하고 통과시키기 위한 모의 엔드포인트입니다.
"""

from uuid import uuid4
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/workspaces")


class WorkspaceCreate(BaseModel):
    name: str = Field(..., min_length=1, description="워크스페이스 이름")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_workspace(body: WorkspaceCreate) -> dict[str, object]:
    """새로운 워크스페이스 생성 (201 Created 반환)."""
    return {
        "id": uuid4().hex,
        "name": body.name,
        "total_documents": 0,
    }

"""ontology-map-workspace에서 배운 워크스페이스 생성, 검색 및 단건 조회 미니 API.

[손코딩 4번] POST 생성, [손코딩 5번] 422 방어, [손코딩 6번] params 검색, [손코딩 7번] 경로 변수 조회 엔드포인트입니다.
"""

from uuid import uuid4
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/api/v1/workspaces")


class WorkspaceCreate(BaseModel):
    # 허용되지 않은 추가 필드(예: owner_user_id 조작)가 들어오면 422로 차단
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255, description="워크스페이스 이름")


# 가상 워크스페이스 저장소 (ontology-map 모의 데이터)
WORKSPACE_DB = [
    {"id": "ws-1", "name": "연구 프로젝트"},
    {"id": "ws-2", "name": "개발 프로젝트"},
]


@router.get("")
def list_workspaces(
    q: str = Query(default="", description="검색어 필터"),
    limit: int = Query(default=50, ge=1, le=100),
) -> dict[str, object]:
    """워크스페이스 목록 및 검색 API (GET ?q=연구&limit=10)."""
    filtered = [
        ws for ws in WORKSPACE_DB
        if not q or q.lower() in ws["name"].lower()
    ][:limit]

    return {
        "total": len(filtered),
        "items": filtered,
    }


@router.get("/{workspace_id}")
def get_workspace(workspace_id: str) -> dict[str, object]:
    """특정 워크스페이스 단건 상세 조회 API (GET /workspaces/{workspace_id})."""
    for ws in WORKSPACE_DB:
        if ws["id"] == workspace_id:
            return ws

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"code": "RESOURCE_NOT_FOUND", "message": "워크스페이스를 찾을 수 없습니다."},
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_workspace(body: WorkspaceCreate) -> dict[str, object]:
    """새로운 워크스페이스 생성 (201 Created 반환)."""
    new_ws = {
        "id": uuid4().hex,
        "name": body.name,
        "total_documents": 0,
    }
    WORKSPACE_DB.append(new_ws)
    return new_ws

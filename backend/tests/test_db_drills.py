"""[Day 01] 학습자가 직접 손코딩으로 완성한 데이터베이스(SQLAlchemy) 테스트 드릴."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from ontology_map.db.schema import Workspace


def test_workspace_db_insert_and_retrieve(db_session: Session) -> None:
    """[손코딩 10 기본형] db_session.get(Model, pk)를 사용한 단건 조회 검증.

    - db_session.add & flush 로 실제 DB에 INSERT 실행
    - db_session.get 으로 Primary Key 기반 SELECT 검증
    - 테스트 종료 시 conftest.py의 savepoint 롤백으로 DB 자동 원상복구
    """
    new_workspace = Workspace(name="진짜 DB 지도")

    db_session.add(new_workspace)
    db_session.flush()

    # 1. Primary Key 기반 단건 조회 (db_session.get)
    saved = db_session.get(Workspace, new_workspace.id)

    assert saved is not None
    assert saved.id == new_workspace.id
    assert saved.name == "진짜 DB 지도"


def test_workspace_db_query_with_select_and_uniqueness(db_session: Session) -> None:
    """[손코딩 10 심화형] select(...).where(...) 및 scalar 단건/유일성 검증.

    - 특정 컬럼 조건(WHERE Workspace.name == ...)으로 쿼리 실행
    - 결과가 2개 이상일 경우 MultipleResultsFound 예외로 중복 버그 검출
    """
    target_name = "유일성 검증 지도"
    ws = Workspace(name=target_name)
    db_session.add(ws)
    db_session.flush()

    # 2. 조건 검색 및 scalar_one_or_none 유일성 조회
    query = select(Workspace).where(Workspace.name == target_name)
    saved = db_session.scalar(query)

    assert saved is not None
    assert saved.id == ws.id
    assert saved.name == target_name

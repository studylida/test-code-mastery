"""Fudan Train Ticket 도메인을 모방한 미니 기차표 예매 API & 비즈니스 로직.

테스트 코드(단위/통합) 작성을 연습하기 위한 명확한 상태 코드와 엣지 케이스를 포함합니다.
"""

from dataclasses import dataclass, field
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/tickets")


class BookingRequest(BaseModel):
    train_number: str = Field(..., description="열차 번호 (예: G101)")
    passenger_name: str = Field(..., min_length=2, description="탑승자 이름")
    seat_type: str = Field(default="economy", description="좌석 등급: economy 또는 first")
    request_key: str = Field(default="", description="중복 요청 방지를 위한 멱등성 키")


class BookingResponse(BaseModel):
    ticket_id: str
    train_number: str
    passenger_name: str
    seat_type: str
    status: str
    price: int


@dataclass
class TrainInventory:
    train_number: str
    available_seats: int
    orders: dict[str, dict[str, object]] = field(default_factory=dict)
    idempotency_cache: dict[str, str] = field(default_factory=dict)


# 인메모리 열차 좌석 현황 (테스트용 가상 DB)
TRAIN_DATABASE: dict[str, TrainInventory] = {
    "G101": TrainInventory(train_number="G101", available_seats=2),  # 잔여석 2자리
    "K505": TrainInventory(train_number="K505", available_seats=0),  # 매진 열차
}


@router.get("/trains/{train_number}/availability")
def get_seat_availability(train_number: str) -> dict[str, object]:
    """열차 잔여석 조회 API (GET 연습용)."""
    train = TRAIN_DATABASE.get(train_number)
    if not train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "TRAIN_NOT_FOUND", "message": "존재하지 않는 열차입니다."},
        )
    return {
        "train_number": train.train_number,
        "available_seats": train.available_seats,
        "is_sold_out": train.available_seats <= 0,
    }


@router.post("/book", status_code=status.HTTP_201_CREATED)
def book_ticket(request: BookingRequest) -> BookingResponse:
    """기차표 예매 API (POST, 201 Created, 409 Conflict, 멱등성 연습용)."""
    train = TRAIN_DATABASE.get(request.train_number)
    if not train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "TRAIN_NOT_FOUND", "message": "존재하지 않는 열차입니다."},
        )

    # 멱등성 처리: 동일한 request_key로 이미 예매한 경우 기존 티켓 반환
    if request.request_key and request.request_key in train.idempotency_cache:
        cached_ticket_id = train.idempotency_cache[request.request_key]
        cached_order = train.orders[cached_ticket_id]
        return BookingResponse(**cached_order)

    # 잔여석 확인
    if train.available_seats <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "SEATS_SOLD_OUT", "message": "해당 열차는 매진되었습니다."},
        )

    # 예매 성공 처리
    ticket_id = f"TKT-{uuid4().hex[:8].upper()}"
    train.available_seats -= 1
    price = 60000 if request.seat_type == "economy" else 120000

    order_data = {
        "ticket_id": ticket_id,
        "train_number": request.train_number,
        "passenger_name": request.passenger_name,
        "seat_type": request.seat_type,
        "status": "CONFIRMED",
        "price": price,
    }
    train.orders[ticket_id] = order_data

    if request.request_key:
        train.idempotency_cache[request.request_key] = ticket_id

    return BookingResponse(**order_data)

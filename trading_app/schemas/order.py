from pydantic import BaseModel
from typing import List
from trading_app.db.models.order import OrderStatus


class OrderRequest(BaseModel):
    stock_symbol: str
    quantity: float


class OrderResponse(BaseModel):
    id: str
    stock_symbol: str
    quantity: float
    status: OrderStatus


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]


class StatusChangeRequest(BaseModel):
    status: OrderStatus

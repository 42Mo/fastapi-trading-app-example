from pydantic import BaseModel, Field
from enum import Enum


class OrderStatus(str, Enum):
    """Enumeration class representing order status"""
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"


class Order(BaseModel):
    """Class representing a stock order"""
    id: str
    stock_symbol: str
    quantity: float = Field(..., gt=0)
    status: OrderStatus = OrderStatus.PENDING

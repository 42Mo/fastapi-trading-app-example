from typing import Dict, List
import asyncio
import uuid
import copy
from trading_app.db.models.order import Order, OrderStatus
from trading_app.db.models.errors import OrderNotFoundError
from trading_app.db.database_interface import DatabaseInterface


class InMemoryDatabase(DatabaseInterface):
    """In-memory database for managing orders"""
    def __init__(self):
        self._db: Dict[str, Order] = {}
        self._lock = asyncio.Lock()

    async def add_order(self, stock_symbol: str, quantity: float) -> Order:
        async with self._lock:
            order_id: str = str(uuid.uuid4())
            order = Order(id=order_id, stock_symbol=stock_symbol, quantity=quantity)
            self._db[order_id] = order
            return order

    async def update_order_status(self, order_id: str, new_status: OrderStatus) -> None:
        async with self._lock:
            if order_id not in self._db:
                raise OrderNotFoundError(order_id)
            self._db[order_id].status = new_status

    async def get_order(self, order_id: str) -> Order:
        async with self._lock:
            if order_id not in self._db:
                raise OrderNotFoundError(order_id)
            return copy.deepcopy(self._db[order_id])

    async def get_all_orders(self) -> List[Order]:
        async with self._lock:
            return [copy.deepcopy(order) for order in self._db.values()]

    async def delete_order(self, order_id: str) -> None:
        async with self._lock:
            if order_id not in self._db:
                raise OrderNotFoundError(order_id)
            del self._db[order_id]

from abc import ABC, abstractmethod
from typing import List
from trading_app.db.models.order import Order, OrderStatus


class DatabaseInterface(ABC):

    @abstractmethod
    async def add_order(self, stock_symbol: str, quantity: float) -> Order:
        pass

    @abstractmethod
    async def update_order_status(self, order_id: str, new_status: OrderStatus) -> None:
        pass

    @abstractmethod
    async def get_order(self, order_id: str) -> Order:
        pass

    @abstractmethod
    async def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    async def delete_order(self, order_id: str) -> None:
        pass

from trading_app.db.database_interface import DatabaseInterface
from trading_app.db.models.order import Order as OrderModel, OrderStatus
from typing import List
import asyncio
import random


class OrderService:
    def __init__(self, db: DatabaseInterface):
        self.db = db

    async def create_order(self, stock_symbol: str, quantity: float) -> OrderModel:
        """Create an order"""
        return await self.db.add_order(stock_symbol, quantity)

    async def get_orders(self) -> List[OrderModel]:
        """Get orders list"""
        return await self.db.get_all_orders()

    async def get_order_by_id(self, order_id: str) -> OrderModel:
        """Get an order by id"""
        return await self.db.get_order(order_id)

    async def delete_order(self, order_id: str) -> None:
        """Delete an order by id"""
        await self.db.delete_order(order_id)

    async def update_order_status(self, order_id: str, new_status: OrderStatus) -> None:
        """Update order status"""
        await self.db.update_order_status(order_id, new_status)

    async def update_order_status_delayed(self, order_id: str) -> None:
        """Update order status after a random delay"""
        await asyncio.sleep(random.uniform(5, 10))
        await self.db.update_order_status(order_id, OrderStatus.EXECUTED)

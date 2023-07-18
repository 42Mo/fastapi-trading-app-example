from abc import ABC, abstractmethod
from trading_app.db.models.order import OrderStatus


class Observer(ABC):
    @abstractmethod
    async def update_status_event(self, order_id: str, new_status: OrderStatus) -> None:
        pass

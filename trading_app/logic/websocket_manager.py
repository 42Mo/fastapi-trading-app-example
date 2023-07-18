import json

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
from trading_app.db.database import OrderStatus
from trading_app.logic.observer_interface import Observer


class ConnectionManager(Observer):
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, order_id: str) -> None:
        if order_id not in self.active_connections:
            self.active_connections[order_id] = []
        self.active_connections[order_id].append(websocket)
        # await websocket.send_text(f"subscribed on {order_id} order")

    async def disconnect(self, websocket: WebSocket, order_id: str) -> None:
        self.active_connections[order_id].remove(websocket)
        if not self.active_connections[order_id]:
            del self.active_connections[order_id]
        # await websocket.send_text(f"unsubscribed from {order_id} order")

    async def disconnect_all(self) -> None:
        self.active_connections.clear()

    async def update_status_event(self, order_id: str, new_status: OrderStatus) -> None:
        if order_id in self.active_connections:
            connections = self.active_connections[order_id].copy()
            for connection in connections:
                try:
                    await connection.send_text(json.dumps({"order_id": order_id, "new_status": new_status.value}))
                except WebSocketDisconnect:
                    self.active_connections[order_id].remove(connection)
                    if not self.active_connections[order_id]:
                        del self.active_connections[order_id]

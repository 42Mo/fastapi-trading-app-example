import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from trading_app.logic.websocket_manager import ConnectionManager
from trading_app.db.database import InMemoryDatabase
from logging import getLogger

logger = getLogger(__name__)


def create_websocket_endpoint(db: InMemoryDatabase):
    websocket_router = APIRouter()
    manager = ConnectionManager()
    db.register_observer(manager)

    @websocket_router.websocket("/ws")
    async def websocket_order_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                # await websocket.send_text(f"Message text was: {data}")
                try:
                    message = json.loads(data)
                    action = message.get('action')
                    order_id = message.get('order_id')
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({"error": "Invalid JSON format"}))
                    continue
                except Exception:
                    await websocket.send_text(json.dumps({"error": "error"}))
                    continue

                if not order_id:
                    await websocket.send_text(json.dumps({"error": "Missing order_id"}))
                    continue

                if action == 'subscribe':
                    await manager.connect(websocket, order_id)
                elif action == 'unsubscribe':
                    await manager.disconnect(websocket, order_id)
                else:
                    await websocket.send_text(json.dumps({"error": "Invalid action"}))

        except WebSocketDisconnect:
            await manager.disconnect_all()

    return websocket_router

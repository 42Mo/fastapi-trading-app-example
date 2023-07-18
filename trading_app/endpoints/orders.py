from logging import getLogger
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from trading_app.logic.order_service import OrderService
from trading_app.schemas.order import OrderRequest, OrderResponse, OrderListResponse, StatusChangeRequest
from trading_app.db.models.errors import OrderNotFoundError

logger = getLogger(__name__)


def create_endpoints(order_service: OrderService):
    order_router = APIRouter()

    @order_router.post(
        "/orders",
        status_code=status.HTTP_201_CREATED,
        response_model=OrderResponse,
    )
    async def create_order_endpoint(order: OrderRequest, background_tasks: BackgroundTasks):
        """Create an order"""
        try:
            order = await order_service.create_order(order.stock_symbol, order.quantity)
            background_tasks.add_task(order_service.update_order_status_delayed, order.id)
            logger.info(f"Created order with id {order.id}")
            return OrderResponse(**order.model_dump())
        except RequestValidationError:
            raise HTTPException(status_code=400, detail="Invalid order ID.")

    @order_router.get(
        "/orders",
        status_code=status.HTTP_200_OK,
        response_model=OrderListResponse,
    )
    async def get_orders_endpoint():
        """get order list"""
        orders = await order_service.get_orders()
        return OrderListResponse(orders=[OrderResponse(**order.model_dump()) for order in orders])

    @order_router.get(
        "/orders/{order_id}",
        status_code=status.HTTP_200_OK,
        response_model=OrderResponse,
    )
    async def get_order_by_id(order_id: str):
        try:
            order = await order_service.get_order_by_id(order_id)
            return OrderResponse(**order.model_dump())
        except OrderNotFoundError:
            raise HTTPException(status_code=404, detail="Order not found")

    @order_router.put(
        "/orders/{order_id}",
        status_code=status.HTTP_200_OK,
        response_model=OrderResponse,
    )
    async def update_order_status_endpoint(order_id: str, new_status: StatusChangeRequest):
        try:
            await order_service.update_order_status(order_id, new_status.status)
            order = await order_service.get_order_by_id(order_id)
            logger.info(f"Updated order with id {order_id} with status {status}")
            return OrderResponse(**order.model_dump())
        except OrderNotFoundError:
            raise HTTPException(status_code=404, detail="Order not found")

    @order_router.delete(
        "/orders/{order_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_order_by_id(order_id: str):
        try:
            await order_service.delete_order(order_id)
            logger.info(f"Deleted order with id {order_id}")
            return {"id": order_id}
        except OrderNotFoundError:
            raise HTTPException(status_code=404, detail="Order not found")

    return order_router

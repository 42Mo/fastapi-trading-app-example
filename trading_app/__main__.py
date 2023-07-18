import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from uvicorn import run
from trading_app.endpoints.orders import create_endpoints
from trading_app.logic.order_service import OrderService
from trading_app.db.database import InMemoryDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": str(exc.detail)},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": str(exc.detail)},
    )

db = InMemoryDatabase()
order_service = OrderService(db)

# Bind routes
app.include_router(create_endpoints(order_service))


if __name__ == "__main__":
    run(
        "trading_app.__main__:app",
        host="localhost",
        port=8080,
        reload=False,
        log_level="debug",
    )

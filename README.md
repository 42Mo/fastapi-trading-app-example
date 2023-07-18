# fastapi-trading-app-example
🐍 FastAPI Trading App: A fun, practice project for trading simulation 📈

This is a practice project for a simulated trading platform built with Python and FastAPI.
The API also supports WebSockets for real-time updates of trading orders.

## Overview
The trading-app is a RESTful API that simulates a trading platform with support for real-time order updates via WebSockets.
It allows for the placement, retrieval, and cancellation of trading orders.

This project also makes use of Poetry for dependency management and Docker for easy setup and deployment.

## Getting Started
### Requirements
- Python 3.10
- Docker (Optional)


### Local Setup

1. Clone the repository.
```bash
git clone https://github.com/42Mo/fastapi-trading-app-example
```

2. Navigate into the project directory.
```bash
cd fastapi-trading-app-example
```

3. Install the project dependencies using Poetry.
```bash
poetry install
```

4. Run the application.
```bash
poetry run python -m trading_app
```
The server will start on http://localhost:8080.

### Docker Setup

1. Clone the repository.
```bash
git clone https://github.com/42Mo/fastapi-trading-app-example
```

2. Navigate into the project directory.
```bash
cd trading-app
```

3. Build the Docker image.
```bash
docker build -t trading-app .
```

4. Run the Docker container.
```bash
docker run -p 8080:8080 trading-app
```
The server will start on http://localhost:8080.


## API Endpoints
This project follows the OpenAPI Specification (OAS) for designing and documenting its API.
Here is a brief overview of the available endpoints:

- GET /orders: Retrieve all orders
- POST /orders: Place a new order
- GET /orders/{orderId}: Retrieve a specific order
- DELETE /orders/{orderId}: Cancel an order
- GET /ws: Establish a WebSocket connection for real-time order information

For more detailed information, please refer to the api_spec.yaml file in the root of the project.
# Trading App Tests
This folder contains a suite of tests for a trading simulation server application.
It includes API tests, WebSocket tests, and a performance scenario for load testing.
All tests are written in Python using the pytest framework.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.10+
- Docker (optional)

### Installation
#### Option 1: Run tests in a virtual environment

1. Open dir
```bash
cd tests
```

2. Install dependencies
The project uses Poetry as a package manager. If you don't have Poetry installed, install it with the following command:
```bash
pip install poetry
```
Then, install project dependencies with:
```bash
poetry install
```

3. Run the tests
You can run the tests with pytest:
```bash
poetry run pytest
```

#### Option 2: Run tests in Docker
1. Open dir
```bash
cd tests
```

2. Build the Docker image
```bash
docker build -t trading-app-tests .
```

3. Run the Docker container
```bash
docker run -e BASE_HOST=<server-name> -e BASE_PORT=<server-port> trading-app-tests
```
Or run within the same machine:
```bash
docker network create my_network
docker network connect my_network <server-container-name>
docker run --rm -e BASE_HOST=<server-container-name> --network=my_network trading-app-tests
```

### Configuration
The tests use the environment variables BASE_HOST and BASE_PORT to configure the base URL for the trading server API and WebSocket connections.
By default, these are set to localhost and 8080, respectively.

You can set these variables in your environment or modify the default values in the conftest.py file.

### Test Files
- api_test.py: Contains tests for the trading server's REST API.
- websocket_test.py: Contains tests for the trading server's WebSocket connection.
- performance_scenario.py: Contains a load test scenario for the trading server.

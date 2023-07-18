# App requirements

### Task:
Build an automated test suite for a RESTful API that simulates a trading platform with WebSocket support.
Dockerize the test suite and server.

### Description:
You need to create a sample RESTful API server that exposes a set of endpoints to simulate a trading platform.
The API should support managing and executing orders.
In advanced requirements, the platform should use WebSocket connections for receiving real-time order status messages.
There's also a requirement to build an automated test suite for the API using Python and pytest (or any other framework you like) and Dockerize both the test suite and the server.

**Platform**: `Windows, Python 3.6+`

**Knowledge base**: `Python, Pytest, FastAPI, Docker`

## Server requirements:

All provided schemas and requests requirements are optional. Use them if they suit you.
It's important that you implement all required endpoints with described functionality.

Implement the following API endpoints:

1. GET /orders
1. POST /orders
1. GET /orders/{orderId}
1. DELETE /orders/{orderId}

For more info regarding responses from each endpoint, you can follow the provided OpenAPI documentation or use your own solution.
After the client sends POST/orders request, the server sends confirmation and orderId.
Then a client can request order info by using GET /orders/{orderId} and receive status.
Each endpoint should have a random short delay between 0.1 and 1 second.
The Database can be kept in memory.


### Advanced requirements:

- Make server asynchronous.
- Implement WebSocket functionality into your server.
- After orders are received from the client, the server sends back orderId and orderStatus as a response.
- Assume that Order has three statuses: PENDING, EXECUTED, CANCELLED. They should be assigned after a random short delay.
- Notify all subscribed clients about the order execution through WebSocket connection.


## Test cases requirements:

1. The test suite should cover all endpoints and methods of the API.
1. The test cases should be organized into test suites and test functions using pytest or any other testing framework of your choice.
1. The test cases should include both positive and negative scenarios, including input validation errors.
1. The test cases should assert the correctness of the API responses and the expected behavior of the API.
1. The test suite and the API server should be dockerized and should be able to run in separate containers
1. Generate report as a standalone file (e.g. HTML).


### Advanced requirements:

1. The test suite should include checks for the WebSocket connections, including:
    - Ensuring that real-time order status events are properly received by connected WebSocket clients.
    - Ensuring that the order of receiving messages are correct (orderStatus=PENDING, received before orderStatus=EXECUTED or no messages are received after receiving orderStatus=CANCELLED).

1. Implement performance testing according to the following scenario:
    - place 100 orders at the same time, validate the responses from REST API,
    - receive WS messages from the server,
    - calculate average order execution delay and standard deviation based on the a. and b. timestamps,
    - print all the metrics to the console.

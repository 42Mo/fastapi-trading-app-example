import asyncio
import aiohttp
import websockets
import json
import numpy as np
import matplotlib.pyplot as plt
import time
import logging
import os


ORDERS_QUANTITY = 100

HOST = os.getenv('BASE_HOST', 'localhost')
PORT = os.getenv('BASE_PORT', '8080')
API_URL = f"http://{HOST}:{PORT}"
WS_URL = f"ws://{HOST}:{PORT}/ws"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def post_order(session, quantity):
    url = f'{API_URL}/orders'
    start_time = time.time()
    async with session.post(url, json={'stock_symbol': 'EURUSD', 'quantity': quantity}) as resp:
        assert resp.status == 201
        data = await resp.json()
        logging.info(f"Order placed. ID: {data['id']}")
        return data['id'], start_time


async def place_orders():
    async with aiohttp.ClientSession() as session:
        tasks = [post_order(session, 100) for _ in range(ORDERS_QUANTITY)]
        return await asyncio.gather(*tasks)


async def subscribe_order(ws, order_id):
    subscribe_message = {
        "action": "subscribe",
        "order_id": order_id,
    }
    await ws.send(json.dumps(subscribe_message))


async def receive_updates(ws, order_ids, start_times):
    execution_times = []
    while len(execution_times) < len(order_ids):
        update = await ws.recv()
        update_data = json.loads(update)
        if update_data['order_id'] in order_ids:
            # execution_times.append(time.time() - start_times[update_data['order_id']])
            execution_times.append((update_data['order_id'], time.time() - start_times[update_data['order_id']]))
            logging.info(f"Order execution delay: {execution_times[-1]} seconds")

    return execution_times


async def ws_connection(order_ids, start_times):
    async with websockets.connect(WS_URL) as ws:
        await asyncio.gather(*(subscribe_order(ws, order_id) for order_id in order_ids))
        return await receive_updates(ws, order_ids, start_times)


def plot_execution_times(execution_times):
    times = [et[1] for et in execution_times]
    plt.figure(figsize=(10, 6))
    plt.plot(times, marker='o')
    plt.title('Order Execution Delay')
    plt.xlabel('Order Index')
    plt.ylabel('Execution Delay (seconds)')
    # plt.show()


async def main():
    order_ids, start_times = zip(*await place_orders())
    logging.info(f"All orders placed.")
    start_times = dict(zip(order_ids, start_times))
    execution_times = await ws_connection(order_ids, start_times)
    execution_times.sort(key=lambda x: start_times[x[0]])  # Sort by order start times
    logging.info(f"All orders executed.")
    average_time = np.mean([et[1] for et in execution_times])
    std_dev = np.std([et[1] for et in execution_times])
    logging.info(f"Average order execution delay: {average_time} seconds")
    logging.info(f"Standard deviation of execution delay: {std_dev} seconds")
    plot_execution_times(execution_times)


if __name__ == "__main__":
    asyncio.run(main())

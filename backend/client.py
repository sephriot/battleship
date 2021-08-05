import asyncio
import time

import websockets


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            now = time.strftime("%X")
            print("Sending:", now)
            await websocket.send(now)
            msg = await websocket.recv()
            print("Received:", msg)
            await asyncio.sleep(1)


asyncio.get_event_loop().run_until_complete(hello())


# A ----> S -----> B
# B -----> S -----> A
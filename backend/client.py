import asyncio
import sys
import time

import websockets

message = sys.argv[1]


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            now = time.strftime("%X")
            print("Sending:", now, message)
            await websocket.send(message)
            msg = await websocket.recv()
            print("Received:", msg)


asyncio.get_event_loop().run_until_complete(hello())

# A ----> S -----> B
# B -----> S -----> A

# C ----> S -----> D
# D -----> S -----> C

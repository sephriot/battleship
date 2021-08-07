import asyncio
import sys
import time

import websockets

message = sys.argv[1]


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                now = time.strftime("%X")
                print("Sending:", now, message)
                await websocket.send(message)
                msg = await websocket.recv()
                print("Received:", msg)
                if msg == "Disconnect":
                    print(msg)
                    await websocket.close()
                    break
        except websockets.exceptions.ConnectionClosed as ex:
            print(ex)


asyncio.get_event_loop().run_until_complete(hello())

# A ----> S -----> B
# B -----> S -----> A

# C ----> S -----> D
# D -----> S -----> C

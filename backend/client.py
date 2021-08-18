import asyncio
import json
import sys
import time

import websockets

from message.Message import BaseMessage, AttackMessage

message = AttackMessage(x=sys.argv[1], y=sys.argv[2])


def handleAttack(msg: AttackMessage):
    print("I've been hit", msg.x, msg.y)


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                now = time.strftime("%X")
                print("Sending:", now, message.toJSON())
                await websocket.send(message.toJSON())
                msg = await websocket.recv()
                print("Received:", msg)
                msg = BaseMessage(data=json.loads(msg))
                if msg.type == BaseMessage.PLAYER_DISCONNECTED:
                    print(BaseMessage.PLAYER_DISCONNECTED)
                    await websocket.close()
                    break
                elif msg.type == BaseMessage.ATTACK:
                    handleAttack(msg)
        except websockets.exceptions.ConnectionClosed as ex:
            print(ex)


asyncio.get_event_loop().run_until_complete(hello())

# A ----> S -----> B
# B -----> S -----> A

# C ----> S -----> D
# D -----> S -----> C

import asyncio
import json

import websockets

import Message


class Client:

    def __init__(self, onMessage):
        self._stop = False
        self.messages = []
        self.onMessage = onMessage

    async def run(self):
        while not self._stop:
            uri = "ws://31.214.157.25:8765"
            async with websockets.connect(uri) as websocket:
                await asyncio.gather(self.send(websocket), self.receive(websocket))

    def sendMessage(self, message):
        self.messages.append(message)

    async def send(self, websocket):
        while not self._stop or len(self.messages) > 0:
            if len(self.messages) == 0:
                await asyncio.sleep(0.1)
                continue
            message = self.messages.pop().toJSON()
            print("Sending:", message)
            await websocket.send(message)

    async def receive(self, websocket):
        while not self._stop:
            message = await websocket.recv()
            print("Received:", message)
            self.onMessage(Message.BaseMessage(data=json.loads(message)))

    def stop(self):
        self.sendMessage(Message.PlayerDisconnectedMessage())
        self._stop = True

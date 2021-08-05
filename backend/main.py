import asyncio

import websockets


class Server:
    clients = {}

    def __init__(self):
        self.clients = {}

    async def echo(self, websocket, path):
        try:
            async for message in websocket:
                if websocket not in self.clients:
                    self.clients[websocket] = True

                for key in self.clients:
                    if key == websocket:
                        continue
                    await key.send(message)

        except RuntimeError:
            print("Error")


s = Server()
asyncio.get_event_loop().run_until_complete(
    websockets.serve(s.echo, 'localhost', 8765)
)
asyncio.get_event_loop().run_forever()

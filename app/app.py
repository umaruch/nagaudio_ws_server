import logging
import asyncio
import websockets
import json

import app.config as settings
from app.command import Command, ValidationError
from app.routes import routes, mpd_client

logging.basicConfig(level=logging.DEBUG)


class Server:
    """
    Основа основ приложения
    """

    def __init__(self):
        self.clients = set()
        self.host, self.port = settings.SERVER_HOST, settings.SERVER_PORT

    # Вызывается для запуска сервера после его инициализации
    async def run(self):
        start_server = websockets.serve(self._ws_handler, self.host, self.port)
        event_listener = asyncio.create_task(self._listen_updates())

        await asyncio.gather(start_server, event_listener)

    async def _listen_updates(self):
        try:
            await mpd_client.client.connect(mpd_client.host, mpd_client.port)
            logging.debug("Successfully connection to MPD server")
            async for event in mpd_client.client.idle(("playlist", "player", "mixer", "options")):
                if event[0] is "playlist":
                    # Вернуть обновленный плейлист
                    data = await mpd_client.playlist_info({'name': 'current'})
                    message = json.dumps({
                        'cmd': "EVENT",
                        'type': "playlist",
                        'data': data
                    })
                else:
                    # Вернуть новый статус
                    data = await mpd_client.status()
                    message = json.dumps({
                        'cmd': "EVENT",
                        'type': "status",
                        'data': data
                    })

                await self.notify_clients(message)

        except Exception as e:
            logging.error(e)
            exit()

    async def notify_clients(self, message: str):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def _ws_handler(self, websocket: websockets.WebSocketServerProtocol, url: str):
        await self._register(websocket)
        try:
            await self._messages_handler(websocket)
        finally:
            await self._unregister(websocket)

    async def _register(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.add(websocket)
        logging.info(f"Client {websocket.remote_address} connected")

    async def _unregister(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.remove(websocket)
        logging.info(f"Client {websocket.remote_address} disconnected")

    async def _messages_handler(self, websocket: websockets.WebSocketServerProtocol):
        async for message in websocket:
            try:
                command = Command.parse_raw(message)
            except ValidationError as e:
                logging.error(e.json())
            else:
                func = routes.get(command.cmd, None)
                if func:
                    response = await func(command.args)
                    if response:
                        await websocket.send(json.dumps(response))

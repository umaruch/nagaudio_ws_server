import asyncio
from app.app import Server

# from app.device import init_device

# init_device()

server = Server()
asyncio.run(server.run())


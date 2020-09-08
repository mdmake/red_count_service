import aiohttp
import asyncio
from routes import setup_routes
from aiohttp import web
from db import close_db, init_db

async def hello(request):
    return web.Response(text="Hello, world")


app = web.Application()

setup_routes(app)
#app.on_startup.append(init_db())
#app.on_startup.append(close_db())
web.run_app(app, host="localhost", port=9093)





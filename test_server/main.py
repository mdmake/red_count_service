from settings import config
from routes import setup_routes
from aiohttp import web
from db import close_pg, init_pg
from telegramm_bot import init_telegramm_bot


async def hello(request):
    return web.Response(text="Hello, world")


app = web.Application()
app['config'] = config

setup_routes(app)
app.on_startup.append(init_pg)
app.on_startup.append(init_telegramm_bot)
app.on_cleanup.append(close_pg)
web.run_app(app, host="localhost", port=9093)





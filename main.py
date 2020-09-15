from red_service.routes import setup_routes
from aiohttp import web
from red_service.db import init_db
from red_service.tgbot import tg_on_close, tg_on_start
import os

app = web.Application()
app['tg_bot_url'] = os.environ.get('TG_SERVICE_URL')
app['token'] = os.environ.get('TOKEN')
port = int(os.environ.get('PORT', 8001))

setup_routes(app)
app.on_startup.append(init_db)
app.on_startup.append(tg_on_start)
app.on_cleanup.append(tg_on_close)

web.run_app(app,  port=port)

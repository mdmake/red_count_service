from settings import config
from routes import setup_routes
from aiohttp import web
from db import close_db, init_db
from telegramm_bot import init_telegramm_bot


app = web.Application()
app['config'] = config
app['tg_data'] = {}
app['tg_users'] = list()
app['token'] = app['config']['telegram']['token']


setup_routes(app)
app.on_startup.append(init_db)
app.on_startup.append(init_telegramm_bot)
app.on_cleanup.append(close_db)
web.run_app(app, host="localhost", port=9093)





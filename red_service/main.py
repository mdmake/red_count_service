from settings import config
from routes import setup_routes
from aiohttp import web
from db import close_db, init_db
from telegramm_bot import init_telegramm_bot, close_telegramm_bot
import os


async def create_app():
    app = web.Application()
    app['config'] = config
    app['tg_data'] = {}
    app['tg_users'] = list()
    app['token'] = app['config']['telegram']['token']

    setup_routes(app)
    app.on_startup.append(init_db)
    app.on_startup.append(init_telegramm_bot)
    app.on_cleanup.append(close_db)
    app.on_cleanup.append(close_telegramm_bot)
    return app

# If running directly https://docs.aiohttp.org/en/stable/web_quickstart.html
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    web.run_app(create_app(), port=port)






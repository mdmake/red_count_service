from red_service.routes import setup_routes
from aiohttp import web
from red_service.db import init_db
from red_service.telegramm_bot import init_telegramm_bot, close_telegramm_bot
import os
import asyncio


app = web.Application()
app['tg_data'] = {}      # надо убрать
app['tg_users'] = list() # надо убрать
app['token'] = os.environ.get('TOKEN')

port = int(os.environ.get('PORT', 8000))
print(f'port: ->  {port}')

setup_routes(app)
app.on_startup.append(init_db)
app.on_startup.append(init_telegramm_bot)
app.on_cleanup.append(close_telegramm_bot)


loop = asyncio.get_event_loop()
runner = web.AppRunner(app)
loop.run_until_complete(runner.setup())
site = web.TCPSite(runner, port=port)
loop.run_until_complete(site.start())
loop.run_forever()


#web.run_app(app,  port=port)







import aiohttp




async def send_to_tg(url, data):
    async with aiohttp.ClientSession() as session:
        await session.post(url, json=data)


async def tg_on_close(app):
    async with aiohttp.ClientSession() as session:
        await session.post(app['tg_bot_url'], data="RedService down. No more funny numbers.")
        #print("app['tg_bot_url']: ", app['tg_bot_url'])
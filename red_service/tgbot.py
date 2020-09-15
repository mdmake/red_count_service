import aiohttp


async def send_to_tg(url, data):
    """
    :param url: bot'saddress
    :param data: json to send
    send json with image params to telegram-bot
    """
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(url, json=data)
    except Exception as e:
        pass


async def tg_on_close(app):
    """
    sends a text with a warning about service termination
    """
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(app['tg_bot_url'], data="RedService down. No more funny numbers.")
    except Exception as e:
        pass
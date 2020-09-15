import aiohttp


async def send_to_tg(url, data):
    """
    :param url: bot's address
    :param data: json to send
    send json with image params to telegram-bot
    """
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(url, json=data)
    except Exception as e:
        pass
        # This is bad, but now the service has
        # no one to tell about it


async def tg_on_close(app):
    """
    sends a text with a warning about service termination
    """
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(app['tg_bot_url'], data="RedService down. No more funny numbers.")
    except Exception as e:
        pass
        # This is bad, but now the service has
        # no one to tell about it

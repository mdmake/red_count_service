import telebot


async def init_telegramm_bot(app):
    bot = telebot.TeleBot(app['token'])
    app['bot'] = bot

async def close_telegramm_bot(app):
    if app['tg_users']:
        try:
            for user in app['tg_users']:
                app['bot'].send_message(user, "Извини, я закончил работу, забавных чиселок пока не будет.")
        except Exception as e:
            pass

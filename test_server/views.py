from aiohttp import web
import aiohttp
import os
from image_service import get_red_persent
import db
import json
from db import redtable

async def post_image_handler(request):

    # print("request.version",        request.version)
    # print("request.method",         request.method)
    # print("request.url",            request.url)
    # print("request.rel_url",        request.rel_url)
    # print("request.scheme",         request.scheme)
    # print("request.host",           request.host)
    # print("request.raw_path",       request.raw_path)
    # print("request.query",          request.query)
    # print("request.headers",        request.headers)
    # print("request.content",        request.content)
    # print("request.body_exists",    request.body_exists)
    # print("request.can_read_body",  request.can_read_body)
    # print("request.has_body",       request.has_body)
    # print("request.content_type",   request.content_type)

    if request.body_exists and request.can_read_body:
        query = request.rel_url.query
        user_id = query.get("id", "NoneId")
        image_tag = query.get("tag", "NoneTag")
        # проверка на user_id

        content = await request.content.read()

        red_pixel_percent = get_red_persent(content, threshold=0.7)

        conn = request.app['db'].connect()
        print("conn", conn)
        expr1 = redtable.insert().returning(redtable.c.id)
        dd = conn.execute(expr1, [{'user_id': user_id, 'image_tag': image_tag, 'red': red_pixel_percent}])
        for item in dd:
            rez_id = item[0]
        # print(dd[0])
        # print(dd.id)
        conn.close()
    else:
        return web.Response(status=400, text="No image was sent!")

    #xj = '{"image_id":"{}}", "red":{}}'.format(rez_id, red_pixel_count)
    data_set = {"image_id": rez_id, "red": red_pixel_percent}
    return web.json_response(data_set)



#  Ресурсы /images/{image_id} c методом GET, который отдаёт
#  {'image_id": x, "red": ..., "account_id": ..., "tag": ...}.
#  Метод DELETE удаляет картинку из базы.

# redtable = Table(
#     'red_count_base', meta,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('user_id', Integer),
#     Column('image_tag', String),
#     Column('red', Float)
# )
async def get_image_handler(request):
    image_number = request.match_info.get('image_number', "Anonymous")

    # а так ли нужно?
    try:
        im_number = int(image_number)
    except Exception as e:
        return web.Response(status=400, text="{} not correct image number".format(image_number))

    conn = request.app['db'].connect()

    expr1 = redtable.select(redtable).where(redtable.c.id == im_number)
    dd = conn.execute(expr1)

    data = list()
    keys = ['id', 'user_id', 'image_tag', 'red']
    for item in dd:
        values = list(item)
        data.append(dict(zip(keys, values)))

    conn.close()
    print(data)


    if data:
        data_set = {'image_id': data[0]['id'],
                    "red": data[0]['red'],
                    "account_id": data[0]['user_id'],
                    "tag": data[0]['image_tag']
                    }
        return web.json_response(data_set)

    else:
        return web.Response(status=400, text="Image with id={} not exist".format(im_number))


async def delete_image_handler(request):
    image_number = request.match_info.get('image_number', "NotFindANumber")

    try:
        im_number = int(image_number)
    except Exception as e:
        return web.Response(status=400, text="{} not correct image number".format(image_number))

    conn = request.app['db'].connect()
    expr1 = redtable.delete(redtable).where(redtable.c.id == im_number)
    result = conn.execute(expr1)

    #print(dd)
    # for item in dd:
    #     print("del item", item)
    conn.close()

    if result.rowcount > 0:
        return web.Response(text="Image with id={} was deleted".format(im_number))
    else:
        return web.Response(status=400, text="Image with id={} not exist".format(im_number))

# Ресурс /images/count, который на метод
# GET принимает следующие query параметры:
# account_id, tag, red__gt и ищет в базе сколько
# записей уддовлетворяет им (red__gt - минимальное количество красного)
# и отдаёт это число в ответе

async def get_image_count_handler(request):

    data1 = request.match_info
    print(data1)
    try:
        query = request.rel_url.query
        user_id = int(query.get('account_id', "None"))
        tag = query.get('tag', "None")
        red__gt = float(query.get('red__gt', "0"))
    except Exception as e:
        return web.Response(status=400, text="Something get wrong")

    conn = request.app['db'].connect()

    expr1 = redtable.select(redtable).where((redtable.c.user_id == user_id) & (redtable.c.image_tag == tag) & (redtable.c.red >= red__gt))
    result = conn.execute(expr1)

    data = list()
    keys = ['id', 'user_id', 'image_tag', 'red']
    for item in result:
        values = list(item)
        data.append(dict(zip(keys, values)))

    conn.close()
    print(data)

    return web.Response(text=str(result.rowcount))

#после происходит асинхронная отправка json сообщения боту в телеграмм {'image_id": x, "red": ..., "account_id": ..., "tag": ...}.

chatnum = None

async def post_telegramm_handler(request):
    d = request.app['bot'].get_updates()

    print("new ==================")
    for item in d:
        print(item.message.chat.id)

    print(d[0].message.chat.id)
    print(d[-1].message.chat.id)

    print("end ==================")



    request.app['bot'].send_message(d[-1].message.chat.id, "Привет от сервера!!")
    #request.app['bot'].send_message(68735827, "Привет от сервера!!")

    return web.Response(text="it's ok!")



     # https://api.telegram.org/bot1166074327:AAHGChSL2f3QkY8AUcDu9VcPo2Zvc1y-_6s/sendMessage?chat_id=-373550763&text=privet
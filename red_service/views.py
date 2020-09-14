from aiohttp import web
import aiohttp
import os
from red_service.image_service import get_red_percent
import red_service.db
import json
from red_service.db import redtable, db_get_image_handler, \
    db_delete_image_handler, db_post_image_handler, \
    db_get_image_count_handler


async def post_image_handler(request):

    """
    :param request:
    :return:
    Обрабатывает  POST запросы от пользователя, тело запроса представляет из
    себя байты. В этих байтах лежит картинка (jpg).
    Query параметром передаётся account_id пользователя (int) и, опционално,
    вторым query параметром пользователь может передать tag картинки (str).
    После того, как картинка принята, сервис преобразует её в numpy array и считает процент пикселей, в
    которых преобладает красный цвет.
    полученное число он сохраняет в базу вместе с account_id аккаунта, tag-ом.
    База должна выдать картинке новый уникальный идентификатор x (под капотом автоинкримент
    и returning в sql).
    После того, как картинка сохранена в базе, ей выдан порядковый номер x,
    пользователю отдаётся в ответе json содержания {'image_id": x, "red": ...}.
    После происходит асинхронная отправка json сообщения боту в телеграмм {'image_id": x, "red": ..., "account_id": ..., "tag": ...}.
    """

    try:
        query = request.rel_url.query
        account_id = int(query["account_id"])
        tag = query.get("tag", "NoTag")
    except Exception as e:
        return web.Response(status=500, text="Incorrect query parameters")

    if request.body_exists and request.can_read_body:

        content = await request.content.read()

        red_pixel_percent = get_red_percent(content)

        result = db_post_image_handler(request.app['db'], account_id, tag, red_pixel_percent)


        rez_id = list()
        for item in result:
            rez_id.append(item[0])

        print(rez_id)
        data_set = {"image_id": rez_id[0], "red": red_pixel_percent}

        request.app['tg_data'] = {'image_id': rez_id[0],
                    "red": red_pixel_percent,
                    "account_id": account_id,
                    "tag": tag
                    }
        if request.app['tg_users']:
            try:
                for user in request.app['tg_users']:
                    request.app['bot'].send_message(user, str(request.app['tg_data']))
            except Exception as e:
                pass

        return web.json_response(data_set)
    else:
        return web.Response(status=400, text="No image was sent!")


def create_dict_from_select_result(prxobject):
    data = list()
    keys = ['image_id', 'account_id', 'tag', 'red']
    for item in prxobject:
        values = list(item)
        data.append(dict(zip(keys, values)))
    if data:
        return data
    else:
        return None


async def get_image_handler(request):
    """

    :param request:
    :return:

    Обрабатывает запрос по image_id картинки, отдаёт
    {'image_id": x, "red": ..., "account_id": ..., "tag": ...}.
    """

    image_number = request.match_info.get('image_number', "NoNumber")

    try:
        im_number = int(image_number)

        result = db_get_image_handler(request.app['db'], im_number)


        data = create_dict_from_select_result(result)

        if data:
            data_set = {'image_id': data[0]['image_id'],
                        "red": data[0]['red'],
                        "account_id": data[0]['account_id'],
                        "tag": data[0]['tag']
                        }
            return web.json_response(data_set)

        else:
            return web.Response(status=400, text="Image with image_id={} not exist".format(im_number))

    except Exception as e:
        return web.Response(status=500, text=str(e))


async def delete_image_handler(request):

    """
    :param request:
    :return:
    Удаляет картинку из базы по image_id
    """

    image_number = request.match_info.get('image_number', 'NoNumber')

    try:
        im_number = int(image_number)

        result = db_delete_image_handler(request.app['db'], im_number)


        if result.rowcount > 0:
            return web.Response(text="Image with image_id={} was deleted".format(im_number))
        else:
            return web.Response(status=400, text="Image with image_id={} not exist".format(im_number))
    except Exception as e:
        return web.Response(status=500, text=str(e))


async def get_image_count_handler(request):
    """

    :param request:
    :return:

    Принимает следующие query параметры: account_id, tag, red__gt и
    ищет в базе сколько записей уддовлетворяет им
    (red__gt - минимальное количество красного) и
    отдаёт это число в ответе
    """

    try:
        query = request.rel_url.query
        account_id = int(query['account_id'])
        tag = query['tag']
        red__gt = float(query['red__gt'])
    except Exception as e:
        return web.Response(status=400, text="Incorrect request")

    print("====================================================")
    print("query1", query)
    print("query2", account_id, tag, red__gt)
    print("====================================================")

    try:
        result = db_get_image_count_handler(request.app['db'], account_id, tag, red__gt)

        return web.Response(text=str(result.rowcount))
    except Exception as e:
        return web.Response(status=500, text="Error DB connection")


async def get_telegramm_handler(request):
    """
    :param request:
    :return:
    Принимает запрос от телеграм-сервиса с account_id текущего пользователя
    и токеном бота.
    """
    account_id = request.rel_url.query.get('account_id', None)
    token = request.rel_url.query.get('token', None)
    if account_id:
        if account_id not in request.app['tg_users']:
            request.app['tg_users'].append(account_id)
        request.app['token'] = token
        print(request.app['tg_users'])

    return web.Response(text="Ok")






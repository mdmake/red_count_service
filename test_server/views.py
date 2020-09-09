from aiohttp import web
import aiohttp
import os
from image_service import get_red_persent
import db
import json
from db import redtable
from functools import wraps
#
# async def bad_handler(request ,text):
#     return web.Response(status=400, text=text)
#
# def inspect_query_param2(func=None, *, arg=None, types=None):
#
#     arg = list(arg or [])
#     types = list(types or [])
#
#     if func is None:
#         return lambda func: inspect_query_param2(func, arg=arg, types=types)
#
#     @wraps(func)
#     def inner(request):
#         query = request.rel_url.query
#
#         result = False
#         for item, tp in zip(arg,types):
#             if item in request.rel_url.query:
#                 try:
#                     tp(item)
#                 except:
#                     break
#         else:
#             result = True
#
#         if result:
#             return inner(request)
#         else:
#             return bad_handler(request, "Incorrect request")
#
#     return inner
#
#
#
#
# def inspect_query_param(func):
#
#     def inner(request, *args, **kwargs):
#         try:
#             query = request.rel_url.query
#             user_id = int(query.get('account_id', "None"))
#             tag = query.get('tag', "None")
#             red__gt = float(query.get('red__gt', "0"))
#             return func(request, user_id, tag, red__gt)
#         except Exception as e:
#             return web.Response(status=400, text="Incorrect request")
#
#     return inner


async def post_image_handler(request):

    try:
        query = request.rel_url.query
        user_id = int(query["id"])
        image_tag = query.get("tag", "NoneTag")
    except Exception as e:
        return web.Response(status=500, text=str(e))


    if request.body_exists and request.can_read_body:

        content = await request.content.read()

        red_pixel_percent = get_red_persent(content, threshold=0.7)

        conn = request.app['db'].connect()
        expression = redtable.insert().returning(redtable.c.id)
        result = conn.execute(expression, [{'user_id': user_id, 'image_tag': image_tag, 'red': red_pixel_percent}])
        conn.close()

        rez_id = list()
        for item in result:
            rez_id.append(item[0])

        print(rez_id)
        data_set = {"image_id": rez_id[0], "red": red_pixel_percent}

        request.app['tg_data'] = {'image_id': rez_id[0],
                    "red": red_pixel_percent,
                    "account_id": user_id,
                    "tag": image_tag
                    }

        return web.json_response(data_set)
    else:
        return web.Response(status=400, text="No image was sent!")


def create_dict_from_select_result(prxobject):
    data = list()
    keys = ['id', 'user_id', 'image_tag', 'red']
    for item in prxobject:
        values = list(item)
        data.append(dict(zip(keys, values)))
    if data:
        return data
    else:
        return None


async def get_image_handler(request):
    image_number = request.match_info.get('image_number', "NoNumber")

    try:
        im_number = int(image_number)

        conn = request.app['db'].connect()
        expression = redtable.select(redtable).where(redtable.c.id == im_number)
        result = conn.execute(expression)
        conn.close()

        data = create_dict_from_select_result(result)

        if data:
            data_set = {'image_id': data[0]['id'],
                        "red": data[0]['red'],
                        "account_id": data[0]['user_id'],
                        "tag": data[0]['image_tag']
                        }
            return web.json_response(data_set)

        else:
            return web.Response(status=400, text="Image with id={} not exist".format(im_number))

    except Exception as e:
        return web.Response(status=500, text=str(e))


async def delete_image_handler(request):
    image_number = request.match_info.get('image_number', 'NoNumber')

    try:
        im_number = int(image_number)

        conn = request.app['db'].connect()
        expr1 = redtable.delete(redtable).where(redtable.c.id == im_number)
        result = conn.execute(expr1)
        conn.close()

        if result.rowcount > 0:
            return web.Response(text="Image with id={} was deleted".format(im_number))
        else:
            return web.Response(status=400, text="Image with id={} not exist".format(im_number))
    except Exception as e:
        return web.Response(status=500, text=str(e))


async def get_image_count_handler(request):
    try:
        query = request.rel_url.query
        user_id = int(query.get('account_id', "None"))
        tag = query.get('tag', "None")
        red__gt = float(query.get('red__gt', "0"))
    except Exception as e:
        return web.Response(status=400, text="Incorrect request")


    try:
        conn = request.app['db'].connect()
        expression = redtable.select(redtable).where((redtable.c.user_id == user_id) & (redtable.c.image_tag == tag) & (redtable.c.red >= red__gt))
        result = conn.execute(expression)

        return web.Response(text=str(result.rowcount))
    except Exception as e:
        return web.Response(status=500, text=str(e))


async def post_telegramm_handler(request):

    print(request.app['tg_data'])

    return web.json_response(request.app['tg_data'])



    # https://api.telegram.org/bot1166074327:AAHGChSL2f3QkY8AUcDu9VcPo2Zvc1y-_6s/sendMessage?chat_id=-373550763&text=privet
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

    conn = request.app['db'].connect()

    try:
        im_number = int(image_number)
    except Exception as e:
        return web.Response(status=400, text="{} not correct image number".format(image_number))

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



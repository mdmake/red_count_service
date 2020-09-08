from aiohttp import web
import aiohttp
import os
from image_service import get_red_persent
from db import engine, conn, redtable
import json

async def handler(request):
    # print(request)
    return web.Response(text="Hello, world")


async def post_handler(request):
    post = await request.post()
    body = request.rel_url.query
    image = post.get('image')
    tag = post.get('tag')
    print(type(image))
    print(image)  # see post details
    print(tag)  # see post details
    return web.Response(text="get you picture )) ")


async def post_image_handler(request):

    print("request.version",        request.version)
    print("request.method",         request.method)
    print("request.url",            request.url)
    print("request.rel_url",        request.rel_url)
    print("request.scheme",         request.scheme)
    print("request.host",           request.host)
    print("request.raw_path",       request.raw_path)
    print("request.query",          request.query)
    print("request.headers",        request.headers)
    print("request.content",        request.content)
    print("request.body_exists",    request.body_exists)
    print("request.can_read_body",  request.can_read_body)
    print("request.has_body",       request.has_body)
    print("request.content_type",   request.content_type)

    if request.body_exists and request.can_read_body:

        if "image" in request.content_type:

            query = request.rel_url.query
            user_id = query.get("id", "NoneId")
            image_tag = query.get("tag", "NoneTag")
            # проверка на user_id

            # redtable = Table(
            #     'red_count_base', meta,
            #     Column('id', Integer, primary_key=True, autoincrement=True),
            #     Column('user_id', Integer),
            #     Column('image_tag', String),
            #     Column('red', Float)
            # )

            content = await request.content.read()

            red_pixel_count, all_pixel_count = get_red_persent(content, threshold=0.7)

            expr1 = redtable.insert().returning(redtable.c.id)

            # говнокод
            rez_id = 0
            for ret_id in conn.execute(expr1, [{'user_id': user_id, 'image_tag': image_tag, 'red': red_pixel_count}]):
                rez_id = ret_id
                break


            #with open("testimage.jpg", "wb") as f:
            #    f.write(content)

            #post = await request.json()
            #print("request.post", content)
            print("request.post len ", len(content))
            print("content type", type(content))
            pass
        elif "multipart" in request.content_type:
            reader = await request.multipart()
            print("reader", reader)
            pass

        query = request.rel_url.query

        print(query.get("id", "NoneId"))
        print(query.get("tag", "NoneTag"))
    else:
        print("NO BODY!!!")

    xj = '{"image_id":"{}}", "red":{}}'.format(rez_id, red_pixel_count)
    return web.Response(json=xj)


async def get_image_handler(request):
    body = await request.text()
    print()
    body2 = request.rel_url.query
    print(body, body2)

    return web.Response(text="text")
    # return web.Response(text="Hello, world")

async def put_handler(request):
    print(request)
    return web.Response(text="Hello, world")
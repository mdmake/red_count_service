from aiohttp import web
import aiohttp
import os
from red_service.image_service import get_red_percent
import red_service.db
import json
from red_service.db import redtable, db_get_image_handler, \
    db_delete_image_handler, db_post_image_handler, \
    db_get_image_count_handler

import requests
tg_url = os.environ.get('TG_SERVICE_URL')

async def post_image_handler(request):

    """
    process POST-request from user and return image_id if succeed
    """

    try:
        query = request.rel_url.query
        account_id = int(query["account_id"])
        tag = query.get("tag", "NoTag")
    except Exception as e:
        return web.Response(status=400, text="Incorrect query parameters")

    if request.body_exists and request.can_read_body:

        content = await request.content.read()

        red_pixel_percent = get_red_percent(content)

        result = db_post_image_handler(request.app['db'], account_id, tag, red_pixel_percent)

        # send data to telegram
        # request.app['tg_data'] = {'image_id': result["image_id"],
        #             "red": red_pixel_percent,
        #             "account_id": account_id,
        #             "tag": tag
        #             }

        # if request.app['tg_users']:
        #     try:
        #         for user in request.app['tg_users']:
        #             request.app['bot'].send_message(user, str(request.app['tg_data']))
        #     except Exception as e:
        #         pass

        requests.post(tg_url, json=result)

        return web.json_response(result)
    else:
        return web.Response(status=400, text="No image was sent!")


async def get_image_handler(request):

    image_id = request.match_info.get('image_id', None)

    if image_id:

        image_id = int(image_id)

        data = db_get_image_handler(request.app['db'], image_id)

        if data:
            return web.json_response(data)
        else:
            return web.Response(status=404, text=f"Image with image_id={image_id} not exist")
    else:
        return web.Response(status=400, text="Incorrect query param!")


async def delete_image_handler(request):

    image_id = request.match_info.get('image_id', None)

    if image_id:
        image_id = int(image_id)

        result = db_delete_image_handler(request.app['db'], image_id)

        if result > 0:
            return web.Response(text="Image with image_id={} was deleted".format(image_id))
        else:
            return web.Response(status=400, text="Image with image_id={} not exist".format(image_id))
    else:
        return web.Response(status=400, text="Incorrect query param!")


async def get_image_count_handler(request):

    try:
        query = request.rel_url.query
        account_id = int(query['account_id'])
        tag = query['tag']
        red__gt = float(query['red__gt'])
    except Exception:
        return web.Response(status=400, text="Incorrect query param!")

    result = db_get_image_count_handler(request.app['db'], account_id, tag, red__gt)
    return web.Response(text=str(result))







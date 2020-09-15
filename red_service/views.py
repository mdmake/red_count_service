from aiohttp import web
from red_service.image_service import get_red_percent
from red_service.db import (db_get_image_by_id, db_del_image_by_id,
                            db_save_image, db_get_image_count)

from red_service.tgbot import send_to_tg


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

        result = db_save_image(request.app['db'], account_id, tag, red_pixel_percent)

        await send_to_tg(request.app["tg_bot_url"], result)

        return web.json_response(result)
    else:
        return web.Response(status=400, text="No image was sent!")


async def get_image_handler(request):

    image_id = request.match_info.get('image_id', None)

    if image_id:

        image_id = int(image_id)

        data = db_get_image_by_id(request.app['db'], image_id)

        if data:
            return web.json_response(data)
        else:
            return web.Response(status=404, text=f"Image with image_id={image_id} not exist")
    else:
        return web.Response(status=400, text="Incorrect query param!")


async def delete_image_handler(request):

    """
    delete image's record from db
    """

    image_id = request.match_info.get('image_id', None)

    if image_id:
        image_id = int(image_id)

        result = db_del_image_by_id(request.app['db'], image_id)

        if result > 0:
            return web.Response(text="Image with image_id={} was deleted".format(image_id))
        else:
            return web.Response(status=400, text="Image with image_id={} not exist".format(image_id))
    else:
        return web.Response(status=400, text="Incorrect query param!")


async def get_image_count_handler(request):

    """
    returns the number of records that match the conditions specified
    in the request's query
    """

    try:
        query = request.rel_url.query
        account_id = int(query['account_id'])
        tag = query['tag']
        red__gt = float(query['red__gt'])
    except Exception:
        return web.Response(status=400, text="Incorrect query param!")

    result = db_get_image_count(request.app['db'], account_id, tag, red__gt)
    return web.Response(text=str(result))

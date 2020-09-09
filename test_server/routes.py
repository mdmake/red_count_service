from aiohttp import web
from views import get_image_handler, post_image_handler, delete_image_handler, get_image_count_handler
from views import post_telegramm_handler



def setup_routes(app):
    app.add_routes([#web.get('/', handler),
                    web.get('/image/count', get_image_count_handler),
                    web.get('/image/{image_number:\d+}', get_image_handler),
                    web.post('/image', post_image_handler),
                    web.delete('/image/{image_number:\d+}', delete_image_handler),
                    web.get('/telegramm', post_telegramm_handler),

                    #web.put('/put', put_handler)
    ])
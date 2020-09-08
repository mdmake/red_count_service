from aiohttp import web
from views import handler, post_handler, put_handler, get_image_handler, post_image_handler

def setup_routes(app):
    app.add_routes([web.get('/', handler),
                    web.get('/image', get_image_handler),
                    #web.post('/image', post_handler),
                    web.post('/image', post_image_handler),
                    web.put('/put', put_handler)])
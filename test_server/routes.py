from aiohttp import web
from views import get_image_handler, post_image_handler, delete_image_handler

def setup_routes(app):
    app.add_routes([#web.get('/', handler),
                    web.get('/image/{image_number}', get_image_handler),
                    web.post('/image', post_image_handler),
                    web.delete('/image/{image_number}', delete_image_handler),
                    #web.put('/put', put_handler)
    ])
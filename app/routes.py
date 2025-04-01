from Router import Router
from app.AdvancedHandler import AdvancedHTTPRequestHandler



def register_routes(router: Router, handler_class: AdvancedHTTPRequestHandler):
    router.add_route('GET', '/api/images/', handler_class.get_images)
    router.add_route('POST', '/upload/', handler_class.post_upload)
    router.add_route('DELETE', '/api/delete/<image_id>',
                     handler_class.delete_image)

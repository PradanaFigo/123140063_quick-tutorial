from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')

def main(global_config, **settings):
    """ Fungsi ini mengembalikan aplikasi WSGI Pyramid.
    """
    with Configurator(settings=settings) as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
    return config.make_wsgi_app()
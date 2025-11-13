from pyramid.config import Configurator
from pyramid.view import view_config

class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.project = 'tutorial'

    @view_config(route_name='hello', renderer='hello_world.jinja2')
    def hello_world(self):
        print('Incoming request')
        return {'name': 'Pyramid', 'project': 'tutorial'}

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('hello', '/')
        
        # ----------------------------------------------------------
        # ↓↓↓ BARIS BARU DITAMBAHKAN DI SINI ↓↓↓
        # ----------------------------------------------------------
        config.add_static_view(name='static', path='tutorial:static')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    settings['pyramid.includes'] = 'pyramid_jinja2'
    return app(global_config, **settings)
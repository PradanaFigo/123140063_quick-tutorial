from pyramid.config import Configurator
from pyramid.view import view_config

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI SINI ↓↓↓
# ------------------------------------------------------------------

class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.project = 'tutorial'

    @view_config(route_name='home', renderer='home.jinja2')
    def home_view(self):
        print('Incoming request (home)')
        return {'name': 'Home', 'project': self.project}

    @view_config(route_name='hello', renderer='hello.jinja2')
    def hello_view(self):
        print('Incoming request (hello)')
        # Ambil 'name' dari URL (matchdict)
        name = self.request.matchdict['name']
        return {'name': name, 'project': self.project}

# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        # Rute lama (/) sekarang bernama 'home'
        config.add_route('home', '/')
        # Rute baru dinamis: /hello/{name}
        config.add_route('hello', '/hello/{name}')
        
        # 'config.scan' akan menemukan kedua @view_config
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
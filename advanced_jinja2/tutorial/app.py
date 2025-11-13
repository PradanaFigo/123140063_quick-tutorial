from pyramid.config import Configurator
from pyramid.view import view_config

# HAPUS SEMUA impor Jinja2Renderer yang salah

class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.project = 'tutorial'

    @view_config(route_name='home', renderer='home.jinja2')
    def home_view(self):
        return {'name': 'Home', 'project': self.project}

    @view_config(route_name='hello', renderer='hello.jinja2')
    def hello_view(self):
        name = self.request.matchdict['name']
        return {'name': name, 'project': self.project}

    @view_config(route_name='hello_json', renderer='json')
    def hello_json(self):
        name = self.request.matchdict['name']
        return {'name': name, 'project': self.project}
    
    # Method ini tetap ada dari tutorial
    @view_config(route_name='change_name')
    def change_name(self):
        print('Change name view called')
        return self.request.response

# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        
        # ----------------------------------------------------------
        # KEMBALI MENGGUNAKAN 'add_jinja2_search_path'
        # HAPUS 'add_renderer' yang rusak
        # ----------------------------------------------------------
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('home', '/')
        config.add_route('hello_json', '/hello/{name}.json')
        config.add_route('hello', '/hello/{name}')
        config.add_route('change_name', '/change/{name}')
        
        # ----------------------------------------------------------
        # PERBAIKAN: Baris ini harus ada di sini
        # ----------------------------------------------------------
        config.add_static_view(name='static', path='tutorial:static')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
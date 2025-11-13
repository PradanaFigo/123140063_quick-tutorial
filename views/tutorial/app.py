from pyramid.config import Configurator
from pyramid.view import view_config

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI SINI ↓↓↓
# ------------------------------------------------------------------

class TutorialViews:
    def __init__(self, request):
        # Simpan 'request' agar bisa diakses di method lain
        # sebagai self.request
        self.request = request

    # Dekorator ini menggantikan config.add_view()
    @view_config(route_name='hello', renderer='hello_world.jinja2')
    def hello_world(self):
        print('Incoming request')
        return {'name': 'Pyramid', 'project': 'tutorial'}

# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        # Rute tetap ditambahkan di sini
        config.add_route('hello', '/')
        
        # 'config.scan' akan mencari @view_config di file .py ini
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
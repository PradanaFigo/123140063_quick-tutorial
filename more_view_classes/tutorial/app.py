from pyramid.config import Configurator
from pyramid.view import view_config

class TutorialViews:
    def __init__(self, request):
        self.request = request

    # ----------------------------------------------------------
    # ↓↓↓ VIEW LAMA DIUBAH MENJADI 'home_get' ↓↓↓
    # ----------------------------------------------------------
    @view_config(
        route_name='home',
        renderer='home.jinja2',
        request_method='GET'  # <-- Hanya merespons GET
    )
    def home_get(self):
        print('Incoming GET request')
        return {'name': 'Pyramid', 'project': 'tutorial'}

    # ----------------------------------------------------------
    # ↓↓↓ VIEW BARU UNTUK POST (FORM) ↓↓↓
    # ----------------------------------------------------------
    @view_config(
        route_name='home',
        renderer='home.jinja2',
        request_method='POST' # <-- Hanya merespons POST
    )
    def home_post(self):
        print('Incoming POST request')
        # Ambil 'project' dari data form yang di-POST
        project_name = self.request.params['project']
        # Kembalikan nama proyek baru ke template
        return {'name': 'Pyramid', 'project': project_name}

    # ----------------------------------------------------------
    # ↓↓↓ VIEW JSON LAMA DIUBAH NAMANYA ↓↓↓
    # ----------------------------------------------------------
    @view_config(route_name='home_json', renderer='json')
    def home_json(self):
        print('Incoming request (JSON)')
        return {'name': 'Pyramid', 'project': 'tutorial'}


def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        # ----------------------------------------------------------
        # ↓↓↓ NAMA RUTE DIPERBARUI ↓↓↓
        # ----------------------------------------------------------
        config.add_route('home', '/')
        config.add_route('home_json', '/home.json')
        
        config.add_static_view(name='static', path='tutorial:static')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    settings['pyramid.includes'] = 'pyramid_jinja2'
    return app(global_config, **settings)
from pyramid.config import Configurator

def hello_world(request):
    print('Incoming request')
    return {'name': 'Pyramid', 'project': 'tutorial'}

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI SINI ↓↓↓
# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        
        # 1. Tambahkan setingan untuk Jinja2
        # Ini memberi tahu jinja2 untuk mencari template
        # di folder 'tutorial:templates'
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('hello', '/')
        
        # 2. Perbarui renderer
        # Kita hanya perlu nama file, karena search path sudah diatur
        config.add_view(
            hello_world,
            route_name='hello',
            renderer='hello_world.jinja2' # <-- Lebih sederhana
        )
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
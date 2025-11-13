from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI SINI ↓↓↓
# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi (sebelumnya ada di main).
        Kita memisahkannya agar bisa diimpor untuk pengujian.
    """
    with Configurator(settings=settings) as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
        Sekarang dia hanya memanggil 'app()'.
    """
    return app(global_config, **settings)
from setuptools import setup

# Daftar dependensi utama
requires = [
    'pyramid',
    'waitress',
]

# Daftar dependensi *hanya* untuk pengembangan
dev_requires = [
    'pyramid_debugtoolbar',
]

# Daftar dependensi BARU *hanya* untuk testing
testing_requires = [
    'pytest',
    'pytest-cov', # Ini untuk mengukur cakupan tes
    'webtest',    # Ini untuk mensimulasikan permintaan web
]

setup(
    name='tutorial',
    install_requires=requires,
    # 'extras_require' sekarang memiliki DUA kunci: dev dan testing
    extras_require={
        'dev': dev_requires,
        'testing': testing_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = tutorial.app:main',
        ],
    },
)

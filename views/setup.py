from setuptools import setup

# 1. Tambahkan 'pyramid_jinja2' di sini
requires = [
    'pyramid',
    'pyramid_jinja2',
    'waitress',
]

# Daftar dependensi *hanya* untuk pengembangan
dev_requires = [
    'pyramid_debugtoolbar',
]

# Daftar dependensi *hanya* untuk testing
testing_requires = [
    'pytest',
    'pytest-cov',
    'webtest',
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
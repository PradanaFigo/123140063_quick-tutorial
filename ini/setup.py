from setuptools import setup

# 1. Tambahkan 'pyramid_debugtoolbar' di sini
requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
]

setup(
    name='tutorial',
    install_requires=requires,
    # 2. Tambahkan seluruh blok 'entry_points' ini
    entry_points={
        'paste.app_factory': [
            'main = tutorial.app:main',
        ],
    },
)
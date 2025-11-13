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

setup(
    name='tutorial',
    install_requires=requires,
    # Menambahkan 'extras_require' baru
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = tutorial.app:main',
        ],
    },
)
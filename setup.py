try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Alancoding GPX analyzer',
    'author': 'Alancoding',
    'url': 'https://github.com/AlanCoding/gpx-analyzer',
    'download_url': 'https://github.com/AlanCoding/gpx-analyzer.git',
    'author_email': 'alan.rominger@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'alancoding-gpx-analyzer'
}

setup(**config)

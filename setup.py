try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'GPX analyzer',
    'author': 'AlanCoding',
    'url': 'https://github.com/AlanCoding/gpx-analyzer',
    'download_url': 'https://github.com/AlanCoding/gpx-analyzer.git',
    'author_email': 'alan.rominger@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['gpxstats'],
    'scripts': [],
    'name': 'alancoding-gpx-analyzer'
}

setup(**config)

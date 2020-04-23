from setuptools import setup, find_packages
from libfind import __author__, __author_email__, __description__, __version__

setup(
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    entry_points={
        'console_scripts': [
            'pyfind = libfind.pyfind:py_find'
        ]
    },
    name='libfind',
    packages=['libfind'],
    python_requires='>=3.4',
    version=__version__,
)

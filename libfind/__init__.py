"""
Package for providing behavior like the unix/linux "find" command.
Supports glob expressions and python regex objects.
"""
from typing import List

from .functions import find

__all__: List[str] = ['findpath', 'functions']
__author__: str = 'Ian S. Evans'
__author_email__: str = 'ievans3024@gmail.com'
__description__: str = 'A python implementation of linux/unix find behavior'
__version__: str = '0.0.1'

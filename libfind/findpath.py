import fnmatch
import os
import re

from datetime import datetime
from pathlib import Path
from stat import filemode
from typing import Union, Tuple

from .functions import get_datetime


# have to instantiate Path because it returns a different type in Path.__new__()
# see https://codereview.stackexchange.com/questions/162426/subclassing-pathlib-path
class FindPath(type(Path())):
    """
    A class to provide some convenience for testing aspects of a given path.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        split_path: Tuple[Union[bytes, str], Union[bytes, str]] = os.path.split(self.path)
        self.dir: Union[bytes, str] = split_path[0]
        self.basename: Union[bytes, str] = split_path[1]

    @property
    def absolute_path(self) -> Union[str, bytes, os.PathLike]:
        return self.resolve().path

    @property
    def atime(self) -> datetime:
        return get_datetime(self.stat().st_atime)

    @property
    def ctime(self) -> datetime:
        return get_datetime(self.stat().st_ctime)

    @property
    def filemode(self) -> str:
        """
        Get the file's mode as a string, e.g. "-rwxrwxrwx"
        """
        return filemode(self.stat().st_mode)

    @property
    def gid(self) -> int:
        return self.stat().st_gid

    @property
    def is_dir(self) -> bool:
        return super().is_dir()

    @property
    def is_file(self) -> bool:
        return super().is_file()

    @property
    def is_link(self) -> bool:
        return os.path.islink(self.path)

    @property
    def mtime(self) -> datetime:
        return get_datetime(self.stat().st_mtime)

    @property
    def path(self):
        return os.path.join(*self._parts)

    @property
    def size(self) -> int:
        return self.stat().st_size

    @property
    def uid(self) -> int:
        return self.stat().st_uid

    def matches(self, pattern: Union[str, re.Pattern], case_sensitive: bool = True) -> bool:
        """
        Determine if a path matches a given pattern.
        :param pattern:  A string or regular expression object to test the basename against.
        :param case_sensitive:  Whether or not comparisons to pattern should be case-sensitive.
        :return:
        """

        if not isinstance(pattern, re.Pattern):
            # use fnmatch.translate to create a regex to test against, provide for case (in)sensitivity
            # this is better than glob.glob, which is inconsistently case (in)sensitive across platforms.
            flags: int = 0
            if not case_sensitive:
                flags: int = flags | re.IGNORECASE

            pattern: re.Pattern = re.compile(fnmatch.translate(pattern), flags=flags)

        return bool(pattern.match(self.basename))

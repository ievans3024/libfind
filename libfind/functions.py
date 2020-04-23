import os
import os.path
import re

from datetime import datetime, timedelta, timezone
from time import timezone as tzoffset, tzname
from typing import Union, Iterable


def get_datetime(timestamp: Union[int, float]) -> datetime:
    """
    Construct a localized datetime object from a timestamp.
    :param timestamp:  The unix timestamp (number of seconds from epoch)
    :return:
    """
    if os.name == 'posix':
        # negating tzoffset because POSIX timezones have the opposite sign
        # see https://github.com/eggert/tz/blob/fe36e5f9ef5b5b9404f38d431fedd91d83da2a44/etcetera#L29-45
        offset: int = -tzoffset
    else:
        offset: int = tzoffset
    local_timezone: timezone = timezone(timedelta(seconds=offset), tzname[0])

    return datetime.fromtimestamp(timestamp, local_timezone)


def find(base_path: Union[str, bytes, os.PathLike],
         pattern: Union[str, re.Pattern] = '*',
         types: Iterable[str] = 'fdl',
         follow_links: bool = False,
         case_sensitive: bool = True,
         ) -> Iterable[Union[str, bytes, os.PathLike]]:
    """
    Generator to find files in base_path that match pattern.
    :param base_path:  The directory to start searching.
    :param pattern:  The pattern to search against, as a string or regular expression object.
    :param types:  An iterable to indicate types to find.
                   Currently, "f", "d", and "l" are supported (file, directory, link)
    :param follow_links:  Whether or not to follow symlinks
    :param case_sensitive:  Whether or not comparisons to pattern should be case-sensitive.
    :return:
    """

    from .findpath import FindPath

    tree: Iterable = os.walk(base_path, followlinks=follow_links)

    for _dir, _, _files in tree:

        dirpath: FindPath = FindPath(_dir)

        if (('d' in types) and dirpath.is_dir) or (('l' in types) and dirpath.is_link):
            if dirpath.matches(pattern, case_sensitive=case_sensitive):
                if _dir == base_path:
                    yield base_path
                else:
                    yield _dir

        if ('f' in types) or ('l' in types):
            for _f in _files:
                filepath: FindPath = FindPath(os.path.join(_dir, _f))
                if ('l' in types and filepath.is_link) or ('f' in types and filepath.is_file):
                    if filepath.matches(pattern, case_sensitive=case_sensitive):
                        yield filepath.path


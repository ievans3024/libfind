# Find
*A python implementation of the linux/unix `find` command.*

## Installation

Install the package using `make`. From the project root:
```
make install
```

If `make` is not available, use pip. From the project root:
```
pip install . --user
```

The package can also be removed using make:
```
make uninstall
```

or pip:
```
pip uninstall libfind
```

## Usage

The primary purpose of this package is to provide the find functionality for use in python code.

Some examples:

```
from libfind import find
import re

# all files
for f in find('/path/to/some/dir'):
    print(f)

# follow links
for f in find('/path/to/some/dir', follow_links=True):
    print(f)


# plain filename
# find any files/folders that match the name 'abc'

# case sensitive
for f in find('/path/to/some/dir', pattern='abc'):
    # does not match, e.g. ABC, Abc, aBc, etc.
    print(f)

# case insensitive
for f in find('/path/to/some/dir', pattern='abc', case_sensitive=False):
    # matches, e.g. abc, ABC, Abc, aBc, etc.
    print(f)


# glob expression
# find any files/folders that start with 'ab'

# case sensitive
for f in find('/path/to/some/dir', pattern='ab*'):
    # does not match, eg., ABC, Abc, aBc, etc.
    print(f)

# case sensitive
for f in find('/path/to/some/dir', pattern='ab*', case_sensitive=False):
    # matches, eg., abc, ABC, Abc, aBc, etc.
    print(f)


# regex
# find any files/folders with names composed of any combination
# of the characters a, b, and c, of any length

# case sensitive
for f in find('/path/to/some/dir', pattern=re.compile(r'[abc]+')):
    print(f)

# case insensitive
for f in find('/path/to/some/dir', pattern=re.compile(r'(?i:[abc]+)')):
    print(f)
```

The `FindPath` class extends `pathlib.Path` to provide some convenience for examining paths

```
>>> from libfind.findpath import FindPath
>>> p = FindPath('/path/to/some/dir')
>>> p.filemode
'drwxr-xr-x'
>>> p.is_dir
True
>>> p.absolute_path
'/path/to/some/dir'
>>> p.atime
datetime.datetime(2020, 4, 21, 4, 8, 51, 196532, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=64800), 'CST'))
```

`pip` installs a [command line tool](libfind/pyfind.py) as `pyfind` into the default python `bin` path.

This script can be used in a similar fashion to linux/unix `find`.

Some examples:

```
# all files under /path/to/some/dir
pyfind /path/to/some/dir

# also follow links
pyfind -L /path/to/some/dir

# plain filename
pyfind /path/to/some/dir --name abc  # case sensitive
pyfind /path/to/some/dir --iname abc  # case insensitive

# glob expression
pyfind /path/to/some/dir --name 'ab*'  # case sensitive
pyfind /path/to/some/dir --iname 'ab*'  # case insensitive

# regex
pyfind /path/to/some/dir --rname '[abc]+'  # case sensitive
pyfind /path/to/some/dir --rname '(?i:[abc]+)'  # case insensitive
```

## Changelog
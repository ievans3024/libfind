def py_find() -> None:
    """
    An implementation of linux/unix find using libfind.
    :return:
    """

    import re

    from argparse import ArgumentParser
    from libfind import find

    parser = ArgumentParser()
    parser.add_argument('path', help='The base path to search from.')
    parser.add_argument('-L', '--follow-links', action='store_true', help='Follow links')
    parser.add_argument('--type',
                        help='File type(s) to search. "f" for regular file, "d" for directory, and/or "l" for link')

    name_mutex = parser.add_mutually_exclusive_group()
    name_mutex.add_argument('--iname', help='Case-insensitive name search. Supports non-recursive glob patterns.')
    name_mutex.add_argument('--name', help='Case-sensitive name search. Supports non-recursive glob patterns.')
    name_mutex.add_argument('--rname', type=re.compile, help='Python regular expression for name search.')

    args = parser.parse_args()

    find_kwargs = {
        'follow_links': args.follow_links
    }

    if args.type:
        find_kwargs['types'] = args.type

    if args.iname:
        find_kwargs['pattern'] = args.iname
        find_kwargs['case_sensitive'] = False
    elif args.name:
        find_kwargs['pattern'] = args.name
    elif args.rname:
        find_kwargs['pattern'] = args.rname

    print(*find(args.path, **find_kwargs), sep='\n')

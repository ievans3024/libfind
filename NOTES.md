After installing using `pip install .` inside a virtualenv, the resulting virtualenv installation looks like:
```
/home/ian/PycharmProjects/find/venv
 ├ pyenv.cfg
 ├ bin/
 │  ├ ...  # activate, deactivate, easy_install, etc.
 │  ├ pyfind
 │  └ ...  # pip, python, etc.
 ├ include/  # empty
 ├ lib64/  # link to lib/ (below)
 └ lib/
    └ python3.8/
       └ site-packages/
          ├ ... # pip, setuptools, etc.
          ├ libfind-0.0.1-py3.8.egg-info/
          │  ├ dependency_links.txt
          │  ├ entry_points.txt
          │  ├ installed_files.txt
          │  ├ PKG-INFO
          │  ├ SOURCES.txt
          │  └ top_level.txt
          └ libfind/
             ├ __init__.py
             ├ findpath.py
             ├ functions.py
             └ pyfind.py
```

Running the script produces the following:
```
$ pyfind /home/ian/test
Traceback (most recent call last):
  File "/home/ian/PycharmProjects/find/venv/bin/pyfind", line 11, in <module>
    load_entry_point('libfind==0.0.1', 'console_scripts', 'pyfind')()
  File "/home/ian/PycharmProjects/find/venv/lib/python3.8/site-packages/pkg_resources/__init__.py", line 490, in load_entry_point
    return get_distribution(dist).load_entry_point(group, name)
  File "/home/ian/PycharmProjects/find/venv/lib/python3.8/site-packages/pkg_resources/__init__.py", line 2859, in load_entry_point
    return ep.load()
  File "/home/ian/PycharmProjects/find/venv/lib/python3.8/site-packages/pkg_resources/__init__.py", line 2450, in load
    return self.resolve()
  File "/home/ian/PycharmProjects/find/venv/lib/python3.8/site-packages/pkg_resources/__init__.py", line 2456, in resolve
    module = __import__(self.module_name, fromlist=['__name__'], level=0)
ModuleNotFoundError: No module named 'libfind.pyfind'
```

Running `import libfind.pyfind` inside a python REPL from outside the project directory produces the same `ModuleNotFoundError`, suggesting that the module cannot be found.

Running `import libfind.findpath` inside the same python REPL works just fine. So the package and its contained modules are visible to the path/import system.

As indicated by the resulting virtualenv directory structure, the entire package, including `pyfind.py` is getting installed to the python path.

File permissions for `pyfind.py` are no different from its siblings:
```
$ ls -l venv/lib/python3.8/site-packages/libfind                                                                                                                                                                                                       [20-04-22:19:36]
total 16
-rw-r--r-- 1 ian ian 2776 Apr 22 19:33 findpath.py
-rw-r--r-- 1 ian ian 2457 Apr 22 17:42 functions.py
-rw-r--r-- 1 ian ian  414 Apr 22 19:35 __init__.py
drwxr-xr-x 1 ian ian  182 Apr 22 19:35 __pycache__
-rw-r--r-- 1 ian ian 1375 Apr 22 19:35 pyfind.py
```

There is no reason `pyfind.py` should not be visible while `findpath.py` and `functions.py` are. 

Interestingly, running `pyfind` with PyCharm's debugger has it working just fine. Here's the debugger output:
```
/home/ian/PycharmProjects/find/venv/bin/python /home/ian/.local/share/JetBrains/Toolbox/apps/PyCharm-P/ch-0/201.6668.115/plugins/python/helpers/pydev/pydevd.py --multiproc --qt-support=auto --client 127.0.0.1 --port 44431 --file /home/ian/PycharmProjects/find/venv/bin/pyfind
pydev debugger: process 267094 is connecting

Connected to pydev debugger (build 201.6668.115)
usage: pyfind [-h] [-L] [--type TYPE]
               [--iname INAME | --name NAME | --rname RNAME]
               path
pyfind: error: the following arguments are required: path

Process finished with exit code 2
```

The above output shows the expected argparse help output when required arguments are not satisfied.
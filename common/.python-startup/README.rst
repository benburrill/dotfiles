~/.python-startup/
==================

Python startup files to be loaded by ~/lib/python-startup-loader.py.

``python-startup-loader.py`` is a obsessively compatible $PYTHONSTARTUP
script which I have (minimally) tested on every Python minor release
since Python 1.5 (!!!).  It loads the files in this directory based on a
``# @version:`` comment at the start of each script.

Of the startup scripts here, ``snazzyexit.py`` is probably the most
interesting.  It causes ``>>> exit`` to exit Python REPL using 
``sys.displayhook``.  In doing so, it also adds the ability to override
any object's displayhook behavior by defining ``_display_hook_``.

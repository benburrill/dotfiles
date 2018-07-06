# @version: python < 3.4
# Since Python 3.4, this is done automatically, so it is not needed
# https://docs.python.org/3/library/site.html#rlcompleter-config
# However, if we're going to make history files version dependent (see
# below), we might want to run this on all Python versions.

__all__ = []

try:
    import os
    import sys
    import atexit
    import readline
    import rlcompleter

    # See: https://docs.python.org/2/tutorial/interactive.html

    readline.parse_and_bind("tab: complete")

    # TODO: maybe make the file name version dependent?
    history_file = os.path.expanduser("~/.python_history")
    
    if os.path.exists(history_file):
        readline.read_history_file(history_file)

    atexit.register(lambda: readline.write_history_file(history_file))
except ImportError:
    red = lambda s: "\x1b[31m%s\x1b[0m" % s
    print(red("Unable to setup auto-completion and/or history, "
              "likely due to missing or non-standard readline: "
              "try installing pyreadline (Windows) or gnureadline."))

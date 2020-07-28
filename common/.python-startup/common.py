# The lack of a version specifier means that this will be loaded on all
# versions of python.  I haven't tested how compatible it actually is
# though.

def add_a_random_variable_to_the_global_scope_that_starts_with_potato():
    """
    One of those functions where you never know how much you need it
    until it is gone.
    """

    import __main__
    import random
    setattr(__main__, "potato_%d" % random.randint(0, 42),
            random.randint(0, 42))


from pprint import pprint

try:
    from see import see
except ImportError:
    pass

try:
    from pydoc import pager

    try:
        from StringIO import StringIO as _StringIO
    except ImportError:
        from io import StringIO as _StringIO

    import sys as _sys

    class _PagerCtx(object):
        def __init__(self, pfunc):
            self.buffer = None
            self.old_stdout = None
            self.pfunc = pfunc

        def __enter__(self):
            if self.old_stdout is not None:
                raise RuntimeError("Nested pagers")

            self.buffer = _StringIO()
            self.old_stdout = _sys.stdout
            _sys.stdout = self.buffer

        def __exit__(self, t_exc, exc, tb):
            _sys.stdout = self.old_stdout
            self.old_stdout = None

            text = self.buffer.getvalue()
            self.buffer = None

            self(text)

        def __call__(self, text):
            self.pfunc(text)

    less = more = pager = _PagerCtx(pager)
except ImportError:
    pass

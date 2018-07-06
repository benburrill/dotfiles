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
    less = more = pager
except ImportError:
    pass

# @version: 2.1 <= python
# Version 2.1 added display hooks, which are needed for this to work.


import sys as _sys
try:
    import builtins as _builtins
except ImportError:
    import __builtin__ as _builtins


try:
    object
except NameError: # Python 2.1
    class object:
        pass


class _QuitOnDisplay(object):
    """
    Exits from the program when displayed or called.  "Displayed" means
    using it like 
    
        >>> exit
    
    when the overloadable display hook is in use.

    Typically, the names ``exit`` and ``quit`` are made to be
    _QuitOnDisplay instances.

    Note that _QuitOnDisplay objects do not exit when repr is called on
    them.  If this was the case, any structure, such as ``globals()``,
    that contains a _QuitOnDisplay object would exit when its repr is
    called.  This would be generally undesirable.
    """

    def __call__(self, code=None):
        _sys.exit(code)

    def _displayhook_(self):
        self(0)


exit = quit = _QuitOnDisplay()


# --- Stuff to make _QuitOnDisplay actually work ---


_last_displayhook = _default_displayhook = _sys.__displayhook__


def _new_displayhook(value):
    if hasattr(value, "_displayhook_"):
        value._displayhook_()
        _builtins._ = value
    else:
        _last_displayhook(value)


def use_overloadable_displayhook(make_default=0):
    """
    Use a display hook that can be overloaded with the method
    _displayhook_(self) -> str.  
    
    If ``make_default`` is True, ``sys.__displayhook__`` will also be
    set, making it less likely for another display hook modifier to
    remove overloading.  If this happens anyway, re-calling
    ``use_overloadable_displayhook`` will make the other program's
    display hook compatible with overloading.

    ``_displayhook_`` methods need not worry about dealing with the
    ``_`` variable, but are otherwise responsible for everything else
    ``sys.displayhook`` does.
    """
    
    global _last_displayhook
    
    # Never update the last display hook to the overloadable display
    # hook because it is used to restore to the time before the
    # overloadable display hook was used.
    if _sys.displayhook is not _new_displayhook:
        _last_displayhook = _sys.displayhook
        _sys.displayhook = _new_displayhook

    if make_default:
        _sys.__displayhook__ = _new_displayhook


def reset_displayhooks():
    """
    Reset ``sys.__displayhook__`` to what it was before %s was loaded
    and ``sys.displayhook`` to what it was before the overloadable
    display hook was used.
    """

    _sys.displayhook = _last_displayhook
    _sys.__displayhook__ = _default_displayhook

reset_displayhooks.__doc__ %= __file__


# Update the display hook 
use_overloadable_displayhook(0)

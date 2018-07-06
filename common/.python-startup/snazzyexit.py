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

    def _display_hook_(self):
        self(0)


exit = quit = _QuitOnDisplay()


# --- Stuff to make _QuitOnDisplay actually work ---


class _ReprWrapper(object):
    "Tongue twister"
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return self.string


_last_display_hook = _default_display_hook = _sys.__displayhook__


def _new_display_hook(value):
    actual_value = value
    if hasattr(value, "_display_hook_"):
        to_display = value._display_hook_()

        if to_display is not None:
            value = _ReprWrapper(to_display)

    _last_display_hook(value)

    # If value was a _ReprWrapper, _ will be incorrect, so set it to the
    # actual value.
    _builtins._ = actual_value


def use_overloadable_display_hook(make_default=0):
    """
    Use a display hook that can be overloaded with the method
    _display_hook_(self) -> str.  
    
    If ``make_default`` is True, ``sys.__displayhook__`` will also be
    set, making it less likely for another display hook modifier to
    remove overloading.  If this happens anyway, re-calling
    ``use_overloadable_display_hook`` will make the other program's
    display hook compatible with overloading.

    The string that ``_display_hook_`` methods return is displayed.  If
    ``None`` is returned, the object will be displayed normally.
    ``_display_hook_`` methods need not worry about dealing with the
    ``_`` variable.
    """
    
    global _last_display_hook
    
    # Never update the last display hook to the overloadable display
    # hook because it is used to restore to the time before the
    # overloadable display hook was used.
    if _sys.displayhook is not _new_display_hook:
        _last_display_hook = _sys.displayhook
        _sys.displayhook = _new_display_hook

    if make_default:
        _sys.__displayhook__ = _new_display_hook


def reset_display_hooks():
    """
    Reset ``sys.__displayhook__`` to what it was before %s was loaded
    and ``sys.displayhook`` to what it was before the overloadable
    display hook was used.
    """

    _sys.displayhook = _last_display_hook
    _sys.__displayhook__ = _default_display_hook

reset_display_hooks.__doc__ %= __file__


# Update the display hook 
use_overloadable_display_hook(0)

# Putting everything in a class like this  allows compatibility with
# versions of Python with messed up globals/locals for function
# definitions.
class module:
    import os
    import sys
    import re
    import traceback
    
    def filter_all(mod, module_dict):
        """
        Filter out the items from module_dict that would not be added to
        the global scope if ``from module import *`` was run, where
        ``vars(module) == module_dict``.
        """
        
        try:
            all_items = module_dict["__all__"]
        except KeyError:
            # We can't use str.startswith in ancient versions of Python.
            all_items = filter(
                lambda key: key[:1] != "_",
                module_dict.keys()
            )
        
        # For compatibility reasons we can't use comprehensions or even
        # the dict builtin!
        result = {}
        for key in all_items:
            result[key] = module_dict[key]
        return result
        # return dict(map(lambda key: (key, module_dict[key]), all_items))

    try:
        # We're going to try importing imp here, but imp is deprecated
        # in recent versions of Python.  Unfortunately, due to bugs with
        # the alternative we use (runpy) in old versions of Python, it
        # makes most sense to default to imp rather than runpy.  To
        # avoid DeprecationWarnings, we temporarily disable warnings
        # while we import imp.
        try:
            import warnings
            # This is essentially what warnings.catch_warnings does.
            # However, warnings.catch_warnings is Python 2.6+ only,
            # which makes compatibility more complicated than just
            # trying to do it myself.
            _old_showwarning = warnings.showwarning
            warnings.showwarning = lambda *a, **k: None
        except ImportError:
            pass

        try:
            import imp
        finally:
            try:
                import warnings
                warnings.showwarning = _old_showwarning
                # Not sure if this is a good idea:
                # imp = sys.modules.pop("imp", None)
            except ImportError:
                pass

        def _import_all(mod, file_path, run_name):
            # Don't spew bytecode all over the place if possible
            old_dwbc = getattr(mod.sys, "dont_write_bytecode", None)
            mod.sys.dont_write_bytecode = 1 # True
            
            # For compatibility, we don't use context managers
            source_file = open(file_path)
            try:
                # Although we don't need to call imp.load_source with
                # the source_file argument, the IOError raised by
                # load_source is missing a filename in Python 2, which
                # is something we check later on.  Opening the file
                # ourselves has the desirable effect of raising a proper
                # IOError when things go wrong.
                return mod.filter_all(vars(mod.imp.load_source(
                    run_name, file_path, source_file
                )))
            finally:
                source_file.close()
                mod.sys.dont_write_bytecode = old_dwbc
    except ImportError:
        # Because imp is deprecated since 3.4, we write another version
        # of _import_all that should work in future versions.  I don't
        # use importlib because it is a pain to use for importing
        # something from a path.  Instead I use runpy.  runpy is really
        # nice, and I would even make it the default choice, but in
        # older versions of Python it has a bug described very briefly
        # in https://bugs.python.org/issue15230 that causes every global
        # variable to be set to None once run_path returns.  That bug
        # report also describes a number of other strange behaviors.
        # However, given that these problems seem to be fixed in modern
        # versions of Python, it makes a good future-compatible choice.

        import runpy
        def _import_all(mod, file_path, run_name):
            return mod.filter_all(mod.runpy.run_path(
                file_path, run_name=run_name
            ))

    try:
        from functools import partial
    except ImportError:
        # A shitty and probably wrong -- but good enough -- version of
        # partial for versions of Python that don't have it.  We need
        # partial because lambdas (like all functions) have scoping
        # issues in early versions of Python.
        class partial:
            def __init__(self, func, *args, **kwargs):
                self.func = func
                self.args = args
                self.kwargs = kwargs
            
            def __call__(self, *args, **kwargs):
                fargs = self.args + args
                fkwargs = self.kwargs.copy()
                fkwargs.update(kwargs)
                return apply(self.func, fargs, fkwargs)

    def _get_s_method(mod, meth):
        try:
            return getattr(str, meth)
        except AttributeError:
            import string
            return getattr(string, meth)

    def import_all(mod, file_path, run_name=None):
        """
        Import ``*`` items from a file.  By default, generates a module
        name (run_name) based on file_path.

        Follows the same rules as ``from module import *``.  If the
        module defines ``__all__``, those items will be imported.
        Otherwise, all values without a leading underscore will be.
        """
        
        s_rep = mod._get_s_method("replace")

        # Generate a unique name for the module if not provided
        if run_name is None:
            run_name = "[module@%s]" % (
                s_rep(s_rep(file_path, "_", "__"), ".", "_")
            )

        return mod._import_all(file_path, run_name)

    def version_info_tuple(mod, hexversion=sys.hexversion):
        """
        Grabs a version info tuple similar to ``sys.version_info`` from
        a version number similar to ``sys.hexversion``.  This makes it
        easier to deal with REALLY old versions of Python.
        """

        hex_release_levels = {
            0xA: "alpha",
            0xB: "beta",
            0xC: "candidate",
            0xF: "final"
        }

        return (
            hexversion >> 6 * 4,
            hexversion >> 4 * 4 & 0xFF,
            hexversion >> 2 * 4 & 0xFF,
            hex_release_levels[hexversion >> 1 * 4 & 0xF],
            hexversion & 0xF
        )

    version_spec = re.compile(r"""
        ^\s*
        \#\s*@version\s*:\s*        # version indicator
        (
            (?:
                ([\d.]+)\s*         # left version number
                (<|>|<=|>=|==)      # left operator
            )?
            \s*python\s*            # "python"
            (?:
                (<|>|<=|>=|==)      # right operator
                \s*([\d.]+)         # right version number
            )?

            \s*$
        )?
    """, re.VERBOSE | re.IGNORECASE)

    # for comparing version tuples
    op_map = {
        "<": lambda l, r: l < r,
        ">": lambda l, r: l > r,
        "<=": lambda l, r: l[:len(r)] <= r[:len(l)],
        ">=": lambda l, r: l[:len(r)] >= r[:len(l)],
        "==": lambda l, r: l[:len(r)] == r[:len(l)]
    }

    def ver_match(mod, l_ver, op, r_ver):
        """
        Compare one version to another using the operator ``op``.
        """

        if l_ver is None or r_ver is None:
            return 1 # True
        return mod.op_map[op](l_ver, r_ver)

    def parse_ver(mod, ver_str):
        """
        Parse a version string into a version tuple.
        """

        s_split = mod._get_s_method("split")

        if ver_str is None:
            return None
        return tuple(map(int, s_split(ver_str, ".")))
        
    def file_filter(mod, filename, version):
        """
        Determine whether ``filename`` refers to a startup file that
        should be loaded by the python version specified by ``version``.
        """

        s_split = mod._get_s_method("split")
        s_strip = mod._get_s_method("strip")

        if s_split(filename, ".")[-1] == "py":
            startup_file = open(filename)
            # Fun fact: in early versions of python, you couldn't do
            # try-except-finally, but you could do try-finally.
            # If at first you don't succeed,
            try:
                try:
                    # again

                    line = startup_file.readline()
                    match = mod.version_spec.match(line)

                    # No version spec means any Python version is OK.
                    if match is None:
                        return 1 # True

                    valid, l_ver, l_op, r_op, r_ver = match.groups()
                    if not valid:
                        raise ImportError(
                            "%s has invalid version spec %r" % (
                                filename,
                                s_strip(s_split(line, ":", 1)[-1])
                            )
                        )

                    l_ver = mod.parse_ver(l_ver)
                    r_ver = mod.parse_ver(r_ver)

                    return (mod.ver_match(l_ver, l_op, version) and
                            mod.ver_match(version, r_op, r_ver))
                except IOError:
                    return 0 # False
            finally:
                startup_file.close()
        return 0 # False
    
    def subpaths(mod, directory):
        """
        This is like os.listdir, except that the results are:
         - sorted
         - full paths, rather than relative to directory
         - an empty list if not given a valid directory

        In Python 3, the return value is actually a map object, not a
        list.
        """

        try:
            filenames = mod.os.listdir(directory)
        except OSError:
            filenames = []
        
        filenames.sort()

        return map(mod.partial(mod.os.path.join, directory), filenames)

    def import_startup_files(mod, startup_base=None, version=None):
        """
        See reload_startup_files
        """

        if startup_base is None:
            startup_base = mod.os.environ.get(
                "PYTHON_STARTUP_LOADER_BASE",
                "~/.python-startup"
            )

        startup_base = mod.os.path.expanduser(startup_base)

        if version is None:
            version = mod.version_info_tuple()
        
        filenames = filter(
            mod.partial(mod.file_filter, version=version),
            mod.subpaths(startup_base)
        )

        result = {}
        for filename in filenames:
            try:
                result.update(mod.import_all(filename))
            except Exception:
                # Print out errors from the imported file, but don't
                # stop importing.
                mod.traceback.print_exc()
        return result
    
    def reload_startup_files(mod, startup_base=None, version=None):
        """
        ``reload_startup_file`` reloads the startup files with a given
        configuration.

        By specifying a ``startup_base``, you can load a different set
        of startup files.  By default, this is the directory of the
        startup script, or the directory specified in the environment
        variable ``PYTHON_STARTUP_LOADER_BASE``, if defined.

        ``version`` is the version number of Python used to determine
        which startup files to run.  By default this is the actual
        version of Python from ``sys.version_info``.  ``version`` need
        not be as exact as ``sys.version_info``, but should follow the
        general format.  ``(3,)`` means Python 3, ``(3, 5)`` means
        Python 3.5, etc.
        """

        globals().update(
            mod.import_startup_files(
                startup_base=startup_base,
                version=version
            )
        )


if __name__ == "__main__": # we're PYTHONSTARTUP
    reload_startup_files = module().reload_startup_files
    del module
    
    reload_startup_files()
else:
    globals().update(vars(module()))

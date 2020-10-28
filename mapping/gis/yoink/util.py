import os

import decorator

def catching(exception_type=Exception, handler=None):
    '''Adds an 'except' block around a method, optionally calling a handler
    when an exception is caught.

    Args:
      * exception_type: The type of exception to catch.
      * handler: A handler to call if an exception is caught. Must be
          a callable taking a single argument (the exception.)
    '''
    def catching(f, *args, **kw):
        try:
            return f(*args, **kw)
        except exception_type as e:
            if handler:
                handler(e)

    return decorator.decorator(catching)

def fullpath(path):
    '''Calculates a full, absolute path from some (possibly relative) path.

    Essentially, this just calls abspath(expanduser(path)).

    Args:
      * path: The path to expand fully.
    '''
    return os.path.abspath(
        os.path.expanduser(path))
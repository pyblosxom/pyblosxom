#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""Holds memcache functions.
"""

# Whether or not to use memcache.
usecache = False

_memcache_cache = {}


def memcache_decorator(scope, instance=False):
    """Caches function results in memory

    This is a pretty classic memoization system for plugins. There's
    no expiration of cached data---it just hangs out in memory
    forever.

    This is great for static rendering, but probably not for running
    as a CGI/WSGI application.

    This is disabled by default. It must be explicitly enabled
    to have effect.

    Some notes:

    1. the function arguments MUST be hashable--no dicts, lists, etc.
    2. this probably does not play well with
       non-static-rendering--that should get checked.
    3. TODO: the two arguments are poorly named--that should get fixed.

    :arg scope: string defining the scope. e.g. 'pycategories'.
    :arg instance: whether or not the function being decorated is
        bound to an instance (i.e. is the first argument "self" or
        "cls"?)
    """
    def _memcache(fun):
        def _memcache_decorated(*args, **kwargs):
            if not usecache:
                return fun(*args, **kwargs)

            try:
                if instance:
                    hash_key = hash((args[1:], frozenset(sorted(kwargs.items()))))
                else:
                    hash_key = hash((args, frozenset(sorted(kwargs.items()))))
            except TypeError:
                print(repr((args, kwargs)))
                hash_key = None

            if not hash_key:
                return fun(*args, **kwargs)

            try:
                ret = _memcache_cache.setdefault(scope, {})[hash_key]
            except KeyError:
                ret = fun(*args, **kwargs)
                _memcache_cache[scope][hash_key] = ret
            return ret
        return _memcache_decorated
    return _memcache

# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
#
# This file is part of Canopsis.
#
# Canopsis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Canopsis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Canopsis.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------

from __future__ import unicode_literals

#: dictionary which contains singleton per scope
_SINGLETONS_PER_SCOPE = {}


def singleton_per_scope(cls, scope=None, args=None, kwargs=None):
    """Get one instance of ``cls`` per ``scope``.

    :param type cls: class to instanciate.
    :param collections.Hashable scope: key for unique instance of cls.
    :param collections.Iterable args: cls instanciation varargs.
    :param dict kwargs: cls instanciation kwargs.
    :return: singleton of type cls per scope.
    """

    result = None

    # check if an instance has already been created
    if cls in _SINGLETONS_PER_SCOPE and scope in _SINGLETONS_PER_SCOPE[cls]:
        result = _SINGLETONS_PER_SCOPE[cls][scope]

    else:
        # initialiaze both args and kwargs
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        # instanciate the singleton
        result = cls(*args, **kwargs)
        # register the instance
        _SINGLETONS_PER_SCOPE.setdefault(cls, {})[scope] = result

    return result

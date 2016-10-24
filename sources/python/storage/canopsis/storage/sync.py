# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2015 "Capensis" [http://www.capensis.com]
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

"""Storage synchronization module."""

from b3j0f.conf import Configurable, category, Parameter, Array
from canopsis.middleware.registry import MiddlewareRegistry

from six import string_types

CONF_PATH = 'middleware/sync.conf'
CATEGORY = 'SYNC'
CONTENT = [
    Parameter(name='source'),
    Parameter(name='targets', ptype=Array(string_types))
]


@Configurable(paths=CONF_PATH, conf=category(CATEGORY, *CONTENT))
class Synchronizer(MiddlewareRegistry):
    """Synchronize data from a source storage to target storages.

    Targets must respect a common storage type with the source storage.
    """

    def __init__(self, source=None, targets=None, *args, **kwargs):
        """

        :param source: source storage to synchronize with targets
        :type source: str

        :param targets: targets to synchronize with source
        :type targets: list of str
        """

        super(Synchronizer, self).__init__(*args, **kwargs)

        self.source = source
        self.targets = targets

    def copy(self, source=None, targets=None):
        """
        Copy content of source storage to target storages
        """

        raise NotImplementedError()

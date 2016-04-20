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
from collections import Hashable


class HashGenerator(object):

    def __init__(self, *args, **kwargs):
        super(HashGenerator, self).__init__(*args, **kwargs)

    def get_hash(self, message):

        if (isinstance(message, Hashable)):

            return hash(message)

        elif (isinstance(message, dict)):
            listtosort = []
            for name in message:
                val = message[name]
                listtosort.append((name, val))

            listtosort.sort(key=lambda x: x[0])
            result = listtosort

            return (hash(str(result)))

        elif (isinstance(message, list)):

            return (hash(str(message)))

        else:

            return message

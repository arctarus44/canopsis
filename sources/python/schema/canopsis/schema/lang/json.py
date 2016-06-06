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

from __future__ import absolute_import

from json import load, dump
from jsonschema import validate
from canopsis.schema.core import Schema

class JsonSchema(Schema):

    def getresource(self, path):

        with open(path, "r") as f:
            _rsc = load(f)

        return _rsc
        
    def load(self, path):

        with open(path, "r") as f:
            result = load(f)

        return result

    def validate(self, data):

        return validate(data, self._rsc)

    #take key in argument and make Schema.get(key) dictionary methode
    def __getitem__(self, key):
        
        return self._rsc[key]

    #take key in argument and make Schema[key] = value dictionary methode
    def __setitem__(self, key, value):

        self._rsc[key] = value
        return self._rsc[key]

    #take key in argument and make del Schema[key] dictionary methode
    def __delitem__(self, key):

        del self._rsc[key]

    #save jsondata in the correct folder
    def save(self, data, output):

        with open(output, "w") as f:
            dump(data, f)

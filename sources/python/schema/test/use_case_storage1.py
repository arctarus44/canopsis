#!/usr/bin/python2.7
#Filename : use_case.py
#-*- coding: utf-8 -*-
#--------------------------------
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
# --------------------------------

from canopsis.middleware.core import Middleware
from canopsis.schema.core import Schema
from canopsis.storage.core import Storage

from b3j0f.utils.path import lookup
from b3j0f.conf import Configurable
import os


@Configurable(paths='script.conf')
class UseCase(object):

    @property
    def schema(self):
        if not hasattr(self, '_schema'):
            s_class = lookup(self.schema_class)
            self._schema = s_class(self.path_transfo)

        return self._schema

    @property
    def storage(self):
        if not hasattr(self, '_storage'):
            self._storage = Middleware.get_middleware_by_uri(self.URL)
            self._storage.connect()

        return self._storage

    @property
    def schema_transfo(self):
        if not hasattr(self, '_schema_transfo'):
            self._schema_transfo = self.schema.getresource(self.path_transfo)

        return self._schema_transfo

    @property
    def schemaV1(self):
        if not hasattr(self, '_schemaV1'):
            self._schemaV1 = self.schema.getresource(self.path_v1)

        return self._schemaV1

    @property
    def schemaV2(self):
        if not hasattr(self, '_schemaV2'):
            self._schemaV2 = self.schema.getresource(self.path_v2)

        return self._schemaV2

    def __init__(self, *args, **kwargs):
        super(UseCase, self).__init__(*args, **kwargs)

        self.inp = self._schema_transfo['input']
        self.query = self._schema_transfo['filter']
        self.inplace = self._schema_transfo['inplace']
        self.output = self._schema_transfo['output']

    def storage(self):

        dirs = os.listdir(self.inp)

        for files in dirs:

            pat = os.path.join(self.inp, files)
            element = self.schema.getresource(pat)

            storage.put_element(element)
            cursor = self.storage.find_elements(self.query)

            for data in cursor:

                self.schema.validate(data)

            name = data['name']

            result = self.schema.transfo.apply_patch(data)

            if inplace == True:

                self.output = os.path.expanduser(self.output)
                self.output = os.path.abspath(self.output)
                out = os.path.join(self.output, name)

                self.schema.save(result, out)

            else:

                self.output = os.path.expanduser(self.inp)
                self.output = os.path.abspath(self.inp)
                out = os.path.join(self.inp, name)

                self.schema.save(result, out)


if __name__ == '__main__':
    u = UseCase()
    u.storage()
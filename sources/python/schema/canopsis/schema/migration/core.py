z# -*- coding: utf-8 -*-
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

from canopsis.schema.core import Schema
from canopsis.schema.lang.json import JsonSchema
from canopsis.schema.transformation.core import Transformation
from canopsis.schema.migration import MigrationFactory, get_protocol
import os
import urlparse

def migrate(path_transfo):
    """the migrate function transform data and save them"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_transfo = schema.getresource(path_transfo)

    inp = schema_transfo['input']
    output = schema_transfo['output']
    path_v1 = schema_transfo['path_v1']
    path_v2 = schema_transfo['path_v2']
    inplace = schema_transfo['inplace']

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    #appeler le MigrationFactory.__getitem__(URL)
    myinp = MigrationFactory().__getitem__(inp)
    data = myinp.load(inp, schema_V1)
    result = myinp.transformation(data, schema_V2)

    myout = MigrationFactory().__getitem__(output)
    out = myout.save(result, output)


class FileFactory(MigrationFactory):
    def register(self, cls, URL):
        return cls(URL)


#définir l'interface de base
#propose des methodes utilisées par migration
class IOInterface(object):

    def load(self, URL):
        raise NotImplementedError()

    def transformation(self, data):
        raise NotImplementedError()

    def save(self, result, URL):
        raise NotImplementedError()


#Input File behavio class
class InputFile(IOInterface):

    def load(self, URL, schema_V1):

        data = schema.getresource(path)
        schema_V1.validate(data)

    def transformation(self, data, schema_V2):

        result = transfo.apply_patch(data)
        schema_V2.validate(result)


class OutputFile(IOInterface):

    def save(self, result, URL):

        schema.save(result, URL)


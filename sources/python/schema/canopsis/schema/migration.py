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

from canopsis.middleware.core import Middleware
from canopsis.schema.core import Schema
from canopsis.schema.lang.json import JsonSchema
from canopsis.storage.core import Storage
from canopsis.schema.transformation.core import Transformation

import os

_Schema = {}

def newschema(classchema, clas=None):

    def _recordschema(clas):

        _Schema[classchema] = clas

        return clas

    if clas is None:
        return _recordschema

    else:
        return _recordschema(clas)

@newschema(JsonSchema)
def migrate(path_transfo):
    """the migrate function transform data and save them in function of exit field"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_transfo = schema.getresource(path_transfo)

    inp = schema_transfo['input']
    query = schema_transfo['filter']
    inplace = schema_transfo['inplace']
    output = schema_transfo['output']
    path_v1 = schema_transfo['path_v1']
    path_v2 = schema_transfo['path_v2']
    URL = schema_transfo['URL']
    exit = schema_transfo['exit']

    if exit == 'file':

        fil(inp, output, path_v1, path_v2, path_transfo)

    elif exit == 'dictionary':

        dictionary(inp, path_v1, path_v2, path_transfo)

    elif exit == 'storage':

        storage(URL, path_v1, path_v2, inp, query, path_transfo)


def fil(inp, output, path_v1, path_v2, path_transfo):
    """treatment of the file case
    this function load the validation schema v1 and v2
    get the data and his name
    validate data
    apply the patch to transform data
    and save it in function of inplace field"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)
    data = schema.getresource(inp)
    name = data['name']

    schema.validate(data)

    result = transfo.apply_patch(data)
    schema.validate(result)

    if inplace == True:

        output = os.path.expanduser(output)
        output = os.path.abspath(output)
        out = os.path.join(output, name)

        schema.save(result, out)

    else:

        output = os.path.expanduser(inp)
        output = os.path.abspath(inp)
        out = os.path.join(inp, name)

        schema.save(result, out)


def dictionary(inp, path_v1, path_v2, path_transfo):
    """treatment of the python dictionary case
    load validation schema v1 and v2
    get the data, in this case data is a python dictionary
    apply the transformation patch on data
    print the result"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    data = schema.getresource(inp)
    schema.validate(data)

    result = transfo.apply_patch(data)
    schema.validate(result)

    print result


def storage(URL, path_v1, path_v2, inp, query, path_transfo):
    """treatment of the storage case
    instanciate a storage and connect it
    load validation schema v1 and v2
    put elements in the storage and get selected data
    apply transformation patch
    put the result in the storage to replace data"""

    mystorage = Middleware.get_middleware_by_uri(URL)
    mystorage.connect()

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    dirs = os.listdir(inp)

    for files in dirs:

        pat = os.path.join(inp, files)

        element = schema.getresource(pat)

        mystorage.put_element(element)

        cursor = mystorage.find_elements(query)

        for data in cursor:

            schema.validate(data)

        result = transfo.apply_patch(data)

        mystorage.put_element(result)


class Document(object):

    def __init__(self, document):

        self.document = document
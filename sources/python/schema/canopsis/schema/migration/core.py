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

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    if exit == 'file':

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

    elif exit == 'dictionary':

        data = schema.getresource(inp)
        schema.validate(data)

        result = transfo.apply_patch(data)
        schema.validate(result)

        print result

    elif exit == 'storage':

        mystorage = Middleware.get_middleware_by_uri(URL)
        mystorage.connect()

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

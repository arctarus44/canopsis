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
from canopsis.schema.lang.json import JsonSchema
from canopsis.schema.transformation.core import Transformation
from canopsis.storage.core import Storage

import os

class UseCase(Schema):

    path_transfo = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/transformation.json'
    path_v1 = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/V1_schema.json'
    path_v2 = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/V2_schema.json'

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    mystorage = Middleware.get_middleware_by_uri('mongodb-default-JsonSchema://')
    mystorage.connect()

    schema_transfo = schema.getresource(path_transfo)
    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    inp = schema_transfo['input']
    query = schema_transfo['filter']
    inplace = schema_transfo['inplace']
    output = schema_transfo['output']


    dirs = os.listdir(inp)

    for files in dirs:

        pat = os.path.join(inp, files)

        element = schema.getresource(pat)

        mystorage.put_element(element)

        cursor = mystorage.find_elements(query)

        for data in cursor:

            schema.validate(data)

        name = data['name']

        result = transfo.apply_patch(data)

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
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

import jsonpatch
import jsonschema
import json
import os

class UseCase(Schema):

    path_transfo = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/transformation.json'
    path_v1 = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/V1_schema.json'
    path_v2 = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/V2_schema.json'

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_transfo = schema.getresource(path_transfo)
    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    inp = schema_transfo['input']

    data = {'version':'1.0.0','info':{'eids':'blabla'}}

    schema.validate(data)

    output = schema_transfo['output']

    result = transfo.apply_patch(data)

    schema.validate(result)

    output = os.path.expanduser(output)
    output = os.path.abspath(output)

    schema.save(result, output)
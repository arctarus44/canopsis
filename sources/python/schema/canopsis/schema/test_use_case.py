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
# --------------------------------



from canopsis.middleware.core import Middleware
from canopsis.schema.core import Schema
from canopsis.schema.lang.json import JsonSchema
from canopsis.schema.transformation.core import Transformation

from unittest import main, TestCase, SkipTest
import jsonpatch
import jsonschema
import json


class TestUseCase(TestCase):

    schema_class = JsonSchema
    transformation_class = Transformation

    path = None

    def setUp(self):
        """parameters definition function"""
        
        if self.schema_class is None:
            raise SkipTest('Schema class is not given in {0}'.format(self))


        path_transfo = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/transformation_schema.json'
        path_v1 = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/V1_schema.json'
        path_v2 = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/V2_schema.json'

    def Test(TestUseCase):

        schema_transfo = self.schema.getresource(self.path_transfo)
        schemaV1 = self.schema.getresource(self.path_v1)
        schema_V2 = self.schema.getresource(self.path_v2)

        inp = schema_transfo['input']
        data = self.schema.getresource(inp)

        self.schema.validate(data)

        patch = schema_transfo['patch']
        output = schema_transfo['output']

        result = self.transfo.apply_patch(data)
        self.schema.save(data, output)


if __name__ == '__main__':
    main()
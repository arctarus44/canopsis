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

from canopsis.schema.data_migration.test_schema import TestLoadSchema, TestSchemaDict, TestValidateSchema, TestTransformation
from canopsis.schema.data_migration.lang.json import JsonSchema
from canopsis.schema.data_migration.transformation.core import Transformation
from unittest import main

class TestLoadJsonSchema(TestLoadSchema):
    """test to load a Jsonschema"""
    schema_class = JsonSchema

class TestJsonSchemaDict(TestSchemaDict):
    """test to check the code behavior is like a dict"""
    schema_class = JsonSchema

class TestValidateJsonSchema(TestValidateSchema):
    """test to validate loaded schema"""
    schema_class = JsonSchema

class TestJsonTransformation(TestTransformation):
    """test the data transformation for Json"""
    schema_class = JsonSchema
    transformation_class = Transformation


if __name__ == '__main__':
    main()
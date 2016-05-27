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

"""
test the correct running of Schema API
"""

from canopsis.middleware.core import Middleware
from canopsis.schema.transformation.core import Transformation
from canopsis.schema.core import Schema

from unittest import main, TestCase
import jsonpatch
import jsonschema
import json


class TestLoadSchema(TestCase):
    """schema are in a specific folder, we load it raise an error if schema does not exist"""

    schema_class = Schema

    def setUp(self):
        
        self.path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/base_schema.json'
        self.paths = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/json'
        self.schema = self.__class__.schema_class(self.path)

    def test_success(self):
        """API take a path, return a schema"""
        
        self.schema.getressource(self.schema, self.path)
        doc = self.schema.load(self.schema, self.path)

    def test_failed(self):
        """Api take a non existing path raise an error"""

        self.schema.getressource(self.schema, self.paths)
        with self.assertRaises(IOErros):
            self.schema.getressource(self.schema, self.paths)


class TestSchemaDict(TestCase):
    """test if returned schema can be used like a dictionary
    preciser dep"""

    schema_class = Schema

    def setUp(self):
        
        self.path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/base_schema.json'
        self.schema = self.__class__.schema_class(self.path)

    def test_modification(self):
        """get an item from the loaded schema
        set a value in the item
        del item
        raise an error if schema is not a dict"""

        element = self.schema['id']
        self.assertEqual(element, "http://canopsis.org/base_schema.json")

        self.schema['name'] = 'essai'
        self.assertEqual('essai', self.schema['name'])

        del self.schema['properties']
        with self.assertRaises(KeyError):
            self.schema['properties']


class TestValidateSchema(TestCase):
    """test schema validation"""

    schema_class = Schema

    def setUp(self):
        
        self.path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/base_schema.json'
        self.schema = self.__class__.schema_class(self.path)

        self.doc = {"version":"1.0.0"}

    def test_validation(self):
        """validate a schema return none"""

        self.assertEqual(self.schema.validate(self.doc), None)


    def test_validation_fail(self):
        """validate a schema raise a validationerror if data is invalid
        schemaerror if schema is invalid"""

        with self.assertRaises(ValidationError):
            self.schema.validate(self.doc)


class TestTransformation(TestCase):
    """to transform data we need to get informations from transformation schema
    raise errors if information doesn't exist"""

    schema_class = Schema
    transformation_class = Transformation

    def setUp(self):
        
        self.path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/patch.json'
        self.schema = self.__class__.schema_class(self.path)
        self.transfo = self.__class__.transformation_class(self.schema)

    def test_select_data(self):
        """test application of the filter for data selection"""

        self.schema.validate()

    def test_apply_patch(self):
        """take the selected data and apply patch process
        return the transform data"""

        pa = []
        data =  {   "version":"1.0.0",
                    "info":{
                        "eids":"bla"
                    }
                }

        result = self.transfo.apply_patch(data)

        self.assertEqual(result, {'info': {u'entity_id': 'bla'}, u'essai1': 'test1', 'version': '2.0.0'})

# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016"Capensis" [http://www.capensis.com]
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

from unittest import main, TestCase
from canopsis.schema.core import Schema
from canopsis.schema.transformation import Transformation
import jsonpatch
import jsonschema
import json

path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema'

class TestLoadSchema(TestCase):
    """schema are in a specific folder, we load it raise an error if schema does not exist"""

    def test_success(self):
        """API take a path, return a schema"""
        
        Schema.getressource(self, path)
        doc = Schema.load(self, path)

    def test_failed(self):
        """Api take a non existing path raise an error"""

        paths = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/json'
        Schema.getressource(self, paths)
        self.assertRaises(Schema.IOError, Schema.getressource(self, paths))


class TestSchemaDict(TestCase):
    """test if returned schema can be used like a dictionary
    preciser dep"""

    def test_modification(self):
        """get an item from the loaded schema
        set a value in the item
        del item
        raise an error if schema is not a dict"""

        schema = { "$schema": "http://json-schema.org/draft-04/schema#",
                      "id": "http://canopsis.org/base_schema.json",
                      "name": "base_schema",
                      "description": "base schema for canopsis",
                      "type": "object",
                      
                      "properties": {
                        "version": {
                          "type": "string",
                          "default": "1.0"
                        }
                      }
                    }

        element = schema['id']
        self.assertEqual(element, "http://canopsis.org/base_schema.json")

        schema['name'] = 'essai'
        self.assertEqual('essai', schema['name'])

        del schema['properties']
        with self.assertRaises(KeyError):
            schema['properties']


class TestValidateSchema(TestCase):
    """test schema validation"""

    def test_validation(self):
        """validate a schema return none"""

        schema = { "$schema": "http://json-schema.org/draft-04/schema#",
                            "id": "http://canopsis.org/base_schema.json",
                            "name": "base_schema",
                            "description": "base schema for canopsis",
                            "type": "object",
                          
                            "properties": {
                                "version": {
                                    "type": "string",
                                    "default": "1.0.0"
                                }
                            }
                        }

        valid = {   
                    "version":{"type":"string"}
                }

        assertEqual(jsonschema.validate(self.jsonschema, valid), None)


    def test_validation_fail(self):
        """validate a schema raise a validationerror if data is invalid
        schemaerror if schema is invalid"""

        schema = { "$schema": "http://json-schema.org/draft-04/schema#",
                            "id": "http://canopsis.org/base_schema.json",
                            "name": "base_schema",
                            "description": "base schema for canopsis",
                            "type": "object",
                          
                            "properties": {
                                "version": {
                                    "type": "string",
                                    "default": "1.0.0"
                                }
                            }
                        }

        valid = {   
                    "version":{"type":"number"}
                }

        self.assertRaises(jsonschema.ValidationError, jsonschema.validate(schema, valid))


class TestTransformation(TestCase):
    """to transform data we need to get informations from transformation schema
    raise errors if information doesn't exist"""

    def test_select_data(self):
        """test application of the filter for data selection"""


    def test_apply_patch(self):
        """take the selected data and apply patch process
        return the transform data"""

        patch = {   "add": {
                        "op": "add",
                        "path": "/essai1",
                        "value": "test1"
                    },

                    "replace": {
                        "op": "replace",
                        "path": "/version",
                        "value": "2.0.0"
                    },

                    "copy": {
                        "op": "copy",
                        "from": "/info/eids",
                        "path": "/info/entity_id"
                    },

                    "remove": {
                        "op": "remove",
                        "path": "/info/eids"
                    }
                }   

        data =  {   "version":"1.0.0",
                    "info":{
                        "eids":"bla"
                    }
                }

        
        for element in patch:
            pa.append(patch[element])

        p = jsonpatch.JsonPatch(pa)

        result = p.apply(data)
        
        self.assertEqual(result, {'info': {u'entity_id': 'bla'}, u'essai1': 'test1', 'version': '2.0.0'})



if __name__ == '__main__':
    main()
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

from unittest import main, TestCase
import jsonpatch
import jsonschema
import json

path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schemma'
pa = []
pat = []

class Testdemo(TestCase):

    def test_getressource(self):

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



if __name__ == '__main__':
    main()
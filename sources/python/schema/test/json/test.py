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

import glob
import os
import parse
import json
from jsonpath_rw import jsonpath, parse
import jsonschema
import jsonpatch
from unittest import main, TestCase

path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema'
pa = []
pat = []

class TestParse(TestCase):

    def test_load(self):

        directory = os.listdir(path)

        for files in directory:
            if files.startswith('patch'):
                path_patch = os.path.join(path, files)

                with open(path_patch, "r") as f:
                    patch = json.load(f)

        #print patch

        directo = os.listdir(path)

        for file in directo:
            if file.startswith('patch_schema'):
                path_schema_patch = os.path.join(path, file)

                with open(path_schema_patch, "r") as f:
                    schema_patch = json.load(f)

        #print schema_patch

        direct = os.listdir(path)

        for fil in direct:
            if fil.startswith('V1_schema'):
                path_data = os.path.join(path, fil)

                with open(path_data, "r") as f:
                    schema_data = json.load(f)

        #print schema_data

        if jsonschema.validate(schema_patch, patch) is None:
            
            for cle in patch:
                        
                if cle == 'remove':
                    pa.append(patch[cle])

                elif cle == 'replace':
                    pa.append(patch[cle])

                elif cle == 'move':
                    pa.append(patch[cle])

                elif cle == 'add':
                    pa.append(patch[cle])

                elif cle == 'copy':
                    pa.append(patch[cle])

        #print pa
        
        for element in pa:
            print element
            
            if isinstance(element, list):
                #print element
                pat.extend(element)
        
                #print pat
                pa.remove(element)
                #print pa

        pa.extend(pat)
        #print pa
        
        p = jsonpatch.JsonPatch(pa)
        #print p

        dirs = os.listdir(path)

        for fi in dirs:
            if fi.startswith('topo'):
                path_data = os.path.join(path, fi)

                with open(path_data, "r") as f:
                    data = json.load(f)

                    #print data
                    for cle in data:
                        if cle == 'info':
                            print data

                            result = p.apply(data)
                            #print result

                            with open(path_data, "w") as f:
                                json.dump(result, f, sort_keys = True, indent = 2, separators = (',', ':'))


if __name__ == '__main__':
    main()

#appliquer patch à plusieurs data proprement
#utiliser le schema_transformation -> ref resolver + filtre mongo
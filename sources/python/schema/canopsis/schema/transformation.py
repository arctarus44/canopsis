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
# ---------------------------------

from __future__ import absolute_import

import json
import jsonpatch
from ..lang import JsonSchema

pa = []

alias_data = []
sup_data = []
path_data = []
path_schema_data = []

path_output = []

op = []
value = []


class Transformation(object):

    def __init__(self, schema):
        
        super(Transformation, self).__init__(schema)
        self.schema = schema

    def get_patch(self, data):
        """extract transformation informations from the patch
            and stock them in a list which serve 
            to apply the transformation to data"""

        for cle in data:                
            if cle == 'remove':
                pa.append(data[cle])

            elif cle == 'replace':
                pa.append(data[cle])

            elif cle == 'move':
                pa.append(data[cle])

            elif cle == 'add':
                pa.append(data[cle])

            elif cle == 'copy':
                pa.append(data[cle])

        patch = jsonpatch.JsonPatch(pa)

        return patch

    def get_input(self, data):
        """extract input informations from the patch
            and stock them in different lists which serves 
            to locate datas"""

        for cle in data:
            if cle == 'data':
                
                temp = data['data']

                for cle in p:

                    if cle == 'alias':
                        alias_data.append(temp[cle])

                    elif cle == 'sup':
                        sup_data.append(temp[cle])

                    elif cle == 'path':
                        path_data.append(temp[cle])

            elif cle == 'schema':
                
                temp = data['schema']

                for cle in temp:

                    if cle == 'path':
                        path_schema_data.append(temp[cle])


    def get_output(self, data):
        """extract input informations from the patch
            and stock them in different lists which serves 
            to save new datas"""

        for cle in data:

            if cle == 'path':
                path_output.append(data[cle])

    def get_filter(self, data):
        """extract filter to apply it
            on data"""

        for cle in data:

            if cle == 'op':
                op.append(data[cle])

            elif cle == 'value':
                value.append(data[cle]) 
        

    def transformation(self):
        """ if sup_data = true, new data will be created old data will be deleted
        if sup = false, old data will not be deleted
        and apply patch on data to transform it"""

            if sup_data[0] == True:

                if path_output is not None:
                    path_new = os.path.join(path_output[0], alias_data[0])

                    result = p.apply(data)

                    with open(path_new, "w") as new:
                        json.dump(result, new)

                    os.remove(data)

                else:

                    path_new = os.path.join(path_sources[0], alias_data[0])

                    result = p.apply(data)

                    with open(path_new, "w") as new:
                        json.dump(result, new)

                    os.remove(data)

            elif sup_data[0] == False:

                if path_output is not None:
                    path_new = os.path.join(path_output[0], alias_data[0])

                    result = p.apply(data)

                    with open(path_new, "w") as new:
                        json.dump(result, new)

                else:

                    path_new = os.path.join(path_sources[0], alias_data[0])

                    result = p.apply(data)

                    with open(path_new, "w") as new:
                        json.dump(result, new)
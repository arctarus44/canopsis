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

from ..core import Patch, registerpatch

from ...lang.json import JsonSchema

from ..Transformation import patch, output, filtre

import jsonpatch
import json


@registerpatch(JsonSchema)
class JSONPatch(Patch):

    def process(self, data):
        """define the correct process to return the patch 
        in the correct form and apply it on data"""
        
        patch = self.patch(schema)
        pa = []
        pat = []

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

        for element in pa:
            print element
            
            if isinstance(element, list):
                #print element
                pat.extend(element)
        
                #print pat
                pa.remove(element)
                #print pa

        pa.extend(pat)

        p = jsonpatch.JsonPatch(pa)

        #traitement du filtre pour appliquer le patch 
        #uniquement aux data souhaitées

        filtre = self.filtre(schema)
        #utilisation de la fonction find_element du fichier ..mongo.core
        #on passe query = filtre[value]

        return result

    def save(self, data):
        inplace = self.JsonSchema['sup']

        if inplace == 'true':
            output = self.output(data)

            with open('output', "w") as f:
                jdon.dump(data, output, sort_keys = True, indent = 2, separators = (',', ':'))
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
from ..core import transformation
from ..lang import json

patch = []
inp = []
output = []
filtre = []


class JsonTransformation(Transformation):

    def __init__(self, data):
        
        super(JsonSchema, self).__init__(data)
        self.data = data


    def get_input(self, data, key):
        """extract input informations
        and stock them in different lists which serves 
        to locate data"""

        inp = self.get_item(data, key)
        return inp


    def get_output(self, data, key):
        """extract input informations 
        and stock them in different lists which serves 
        to save new data"""

        output = self.get_item(data, key)
        return output


    def get_filter(self, data, key):
        """extract filter to apply it
            on data"""

        filtre = self.get_item(data, key)
        return filtre


    def get_patch(self, data, key):
        """extract transformation informations from the patch
        and stock them in a list which serve 
        to apply the transformation to data"""

        patch = self.get_item(data, key)
        return patch


    def select_data(self, filter, input):
        """use filter information to select the right data"""

        #decode inp
        for cle in inp:
            if cle == 'path':
                path_data = inp[cle]

        #decode filtre
        recup filtre a aplliquer aux data pour les selctionner

        #search data correspunding to it
        appliquer le filtre et récuperer les data à traiter
        with open(path_data, "r") as f:
            data = json.load(f)
        #return the correct data
        return data


    def apply_patch(self, data):
        """ apply patch operation on data"""

        #decode patch
        p = jsonpatch.JsonPatch(patch)

        #apply it on data
        new_data = p.apply(data)

        #return the transform data
        for cle in inp:
            if cle == 'sup':
                sup = inp[cle]

        if sup[0] = True:
            save(new_data, output)
            os.remove(data)
        else:
            save(new_data, output)
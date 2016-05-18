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
from ..core import SchemaTr


class Transformation(object):

    def __init__(self, data):
        
        super(Schema, self).__init__(data)
        self.data = data


    def get_input(self, data, key):
        """extract input informations
        and stock them in different lists which serves 
        to locate data"""
        
        raise NotImplementedError()


    def get_output(self, data, key):
        """extract input informations 
        and stock them in different lists which serves 
        to save new data"""

        raise NotImplementedError()


    def get_filter(self, data, key):
        """extract filter to apply it
            on data"""

        raise NotImplementedError()


    def get_patch(self, data, key):
        """extract transformation informations from the patchs
        and stock them in a list which serve 
        to apply the transformation to data"""

        raise NotImplementedError()


    def select_data(self):
        """use filter information to select the right data"""
        
        raise NotImplementedError()


    def apply_patch(self):
        """ apply patch operation on data"""
        
        raise NotImplementedError()


    def save(self):
        """ save the new data in the chosen folder"""

        raise NotImplementedError()

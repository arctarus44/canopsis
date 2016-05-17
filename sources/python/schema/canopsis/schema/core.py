#!/usr/bin/env python
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

from b3j0f.conf import Configurable

@Configurable(paths = [])#décorateur qui permet de récupérer tous les chemins 
#définis dans les fichiers de conf(ils peuvent être dans différents dossiers)
class Schema(object):

    def __init__(self, path, *args, **kwargs):

        super(Schema, self).__init__(*args, **kwargs)
        self.path = path

    #valide les schema peut importe le langage
    #raise an exception when it require derived classes to override the method.
    def validate(self, data):

        raise NotImplementedError()
               
# -*- coding: utf-8 -*-
# ---------------------------------
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

import canopsis
import pip
import types

mandf = []

"""
previous version just to list all funcitons and method in canopsis
def parcour(module):
    for i in dir(module):
        try:
            tmp = getattr(module, i)
            if not isinstance(tmp, types.BuiltinFunctionType):
                if isinstance(tmp, types.ModuleType):
                    name =  getattr(tmp, '__name__')
                    if name.startswith('canopsis.'):
                        print name
                        parcour(tmp)
                elif isinstance(tmp, type):
                    for j in dir(tmp):
                        if isinstance(getattr(tmp, j), types.MethodType):
                            print 'method: {0}\n'.format(getattr(tmp, j))
                elif isinstance(tmp, types.FunctionType):
                    print 'function: {0}\n'.format(tmp)

                elif isinstance(tmp, types.MethodType):
                    print 'method: {0}\n'.format(tmp)
                else:
                    pass
        except:
            pass
"""
def parcour(module):
    for i in dir(module):
        try:
            tmp = getattr(module, i)
            if not isinstance(tmp, types.BuiltinFunctionType):
                if isinstance(tmp, types.ModuleType):
                    name =  getattr(tmp, '__name__')
                    if name.startswith('canopsis.'):
                        print name
                        parcour(tmp)
                elif isinstance(tmp, type):
                    for j in dir(tmp):
                        if isinstance(getattr(tmp, j), types.MethodType):
                            if getattr(tmpn, j).__name__ in mandf:
                                setattr(tmp, j, monitoring(j))
                elif isinstance(tmp, types.FunctionType):
                    print 'function: {0}\n'.format(tmp)
                    if tmp.__name__ in mandf:
                        setattr(module, tmp, monitoring(tmp))
        except:
            pass

def launch(maf):
    pkgs = [i.key for i in pip.get_installed_distributions() if i.key.startswith('canopsis.')]
    map(__import__, pkgs)
    mandf = maf
    parcour(canopsis)



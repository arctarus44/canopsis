# -*- coding:utf-8 -*-

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



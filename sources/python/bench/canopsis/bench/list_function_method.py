# -*- coding:utf-8 -*-

import canopsis
import pip
import types

dico = {}

def parcour(module):
    for i in dir(module):
        try:
            tmp = getattr(module, i)
            if not isinstance(tmp, types.BuiltinFunctionType):
                if isinstance(tmp, types.ModuleType):
                    name =  getattr(tmp, '__name__')
                    if name.startswith('canopsis.'):
                        print getattr(tmp, '__name__')
                        parcour(tmp)
                elif isinstance(tmp, type):
                    for j in dir(tmp):
                        if isinstance(getattr(tmp, j), types.MethodType):
                            print 'method: {0}\n'.format(j)
                elif isinstance(tmp, types.FunctionType):
                    print 'function: {0}\n'.format(tmp)

                elif isinstance(tmp, types.MethodType):
                    print 'method: {0}\n'.format(tmp)
                else:
                    pass
                    #print '{0}\n'.format(tmp)
        except:
            pass
            #print '{0}\n'.format(i)

pkgs = [i.key for i in pip.get_installed_distributions() if i.key.startswith('canopsis.')]
map(__import__, pkgs)
parcour(canopsis)

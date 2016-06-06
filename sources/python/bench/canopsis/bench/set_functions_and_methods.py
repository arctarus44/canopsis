# -*- coding:utf-8 -*-

import canopsis
import pip
import types

mandf = []

def parcour(module):
    for i in dir(module):
        try:
            tmp = getattr(module, i)
           # if not isinstance(tmp, types.BuiltinFunctionType):
            if isinstance(tmp, types.ModuleType):
                name =  getattr(tmp, '__name__')
                if name.startswith('canopsis.'):
                    print name
                    parcour(tmp)
            elif isinstance(tmp, type):
                print '{0} - {1}\n'.format(tmp, dir(tmp))
                for j in dir(tmp):
                    if isinstance(getattr(tmp, j), types.MethodType):
                        #print 'method: {0}\n'.format(getattr(tmp, j))
                        file = open('/home/tgosselin/fichierdelog', 'a')
                        file.write('method: {0}\n'.format(getattr(tmp, j)))
                        file.close()

                        if getattr(tmpn, j) in mandf:
                            print '\n\n----------lalalalalala------------\n\n'
                            setattr(tmp, j, monitoring(j))
            elif isinstance(tmp, types.FunctionType):
                    #print 'function: {0}\n'.format(tmp)
                file = open('/home/tgosselin/fichierdelog','a')
                file.write('function: {0}\n'.format(tmp))
                file.close()
                if tmp.__name__ in mandf:
                    setattr(module, tmp, monitoring(tmp))
        except:
            pass

def launch(maf):
    pkgs = [i.key for i in pip.get_installed_distributions() if i.key.startswith('canopsis.')]
    map(__import__, pkgs)
    mandf = maf
    parcour(canopsis)


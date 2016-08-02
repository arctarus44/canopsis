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

from canopsis.middleware.core import Middleware
from canopsis.schema.core import Schema
from canopsis.schema.lang.json import JsonSchema
from canopsis.storage.core import Storage
from canopsis.schema.transformation.core import Transformation

import os

def migrate(path_transfo):
    """the migrate function transform data and save them in function of exit field"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_transfo = schema.getresource(path_transfo)

    inp = schema_transfo['input']
    output = schema_transfo['output']
    path_v1 = schema_transfo['path_v1']
    path_v2 = schema_transfo['path_v2']
    inplace = schema_transfo['inplace']

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    #folder -> folder
    if isinstance(inp, unicode) and inp.startswith('/') and inp.endswith('/'):

        if isinstance(output, unicode):

            dirs = os.listdir(inp)
            for files in dirs:

                path = os.path.join(inp, files)
                data = schema.getresource(path)
                print 'Beware you are migrating '+inp+' do not use it before end of migration'

                result = transfo.apply_patch(data)
                schema.validate(result)

                if inplace == True :

                    schema.save(result, path)

                elif inplace == False and output.starswith('/') and output.endswith('/'):

                    out = os.path.join(output, name)

                    schema.save(result, out)

                elif inplace == False and output.starswith('/'):

                    output = os.path.expanduser(output)
                    output = os.path.abspath(output)
                    out = os.path.join(output, files)

                    schema.save(result, out)

                else :
                    raise(Exception('Invalid output'))

        elif isinstance(output, dict):
            print result

    #file -> storage
        elif isinstance(output, unicode) and output.endswith('//'):

            mystorage = Middleware.get_middleware_by_uri(output)
            mystorage.connect()
            mystorage.put_element(result)

        else:
            raise(Exception('Invalid output'))

    elif isinstance(inp, unicode) and inp.startswith('/'):

        data = schema.getresource(inp)
        name = data['name']
        print 'Beware you are migrating '+name+' do not use it before end of migration'

        schema.validate(data)

        result = transfo.apply_patch(data)
        schema.validate(result)

        #file -> file
        if inplace == True and output.startswith('/'):

            output = os.path.expanduser(output)
            output = os.path.abspath(output)
            out = os.path.join(output, name)

            schema.save(result, out)

        elif inplace == False and output.startswith('/'):

            output = os.path.expanduser(inp)
            output = os.path.abspath(inp)
            out = os.path.join(inp, name)

            schema.save(result, out)

    #file -> dict
        elif isinstance(output, dict):
            print result

    #file -> storage
        elif isinstance(output, unicode) and output.endswith('//'):

            mystorage = Middleware.get_middleware_by_uri(output)
            mystorage.connect()
            mystorage.put_element(result)

        else:
            raise(Exception('Invalid output'))

    #storage -> file
    elif isinstance(inp, unicode) and inp.endswith('//'):

        query = schema_transfo['filter']

        mystorage = Middleware.get_middleware_by_uri(inp)
        mystorage.connect()

        cursor = mystorage.find_elements(query)

        for data in cursor:
            schema.validate(data)

        print 'Beware you are migrating '+inp+' do not use it before end of migration'
        result = transfo.apply_patch(data)

        if isinstance(output, unicode):
            if output.startswith('/'):

                if inplace == True:

                    name = data['name']
                    output = os.path.expanduser(output)
                    output = os.path.abspath(output)
                    out = os.path.join(output, name)

                    schema.save(result, out)

                else:

                    name = data['name']
                    output = os.path.expanduser(inp)
                    output = os.path.abspath(inp)
                    out = os.path.join(inp, name)

                    schema.save(result, out)

            #storage -> storage
            if output.endswith('//'):

                mystorage.put_element(result)

        #storage -> dict
        elif isinstance(output, dict):
            print result

        else:
            raise(Exception('Invalid output'))

    elif isinstance(inp, dict):

        #dict -> file
        schema.validate(inp)
        name = inp['name']
        print 'Beware you are migrating '+name+' do not use it before end of migration'
        result = transfo.apply_patch(inp)

        if isinstance(output, unicode) and output.startswith('/'):

            output = os.path.expanduser(output)
            output = os.path.abspath(output)

            #print output

            schema.save(result, output)

            #dict -> storage
        elif isinstance(output, unicode) and output.endswith('//'):

                mystorage.put_element(result)

        #dict -> dict
        elif isinstance(output, dict):
            print result

        else:
            raise(Exception('Invalid output'))

    else:
        raise(Exception('Invalid input'))
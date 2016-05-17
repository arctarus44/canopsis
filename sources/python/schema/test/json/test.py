#/home/julie/Documents/canopsis/sources/python/simplepy/scripts/TestOutils.py/python2.7
# -*-coding:Utf-8 -*

import json
import collections
import os.path
import os
import jsl
import jsonschema
import copy
from jsonschema import validate
import jsonpatch
from unittest import TestCase, main

path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema'


alias_data = []
sup_data = []
path_sources = []
filter_sources = []
path_schema_data = []

path_output = []

op = []
value = []

pa = []



class TestCreation(TestCase):
    """
    Test event processing function.
    """

    def test_get_patch(self, patch = None):
        """extract transformation informations from the patch
            and stock them in a list which serve 
            to apply the transformation to datas"""

        if patch is not None and validate_schema(patch, schema_patch):

            for cle in patch:

                if cle == 'operations':
                    pat = patch['operations']

                    for cl in pat:
                        
                        if cl == 'remove':
                            pa.append(pat[cl])

                        elif cl == 'replace':
                            pa.append(pat[cl])

                        elif cl == 'move':
                            pa.append(pat[cl])

                        elif cl == 'add':
                            pa.append(pat[cl])

                        elif cl == 'copy':
                            pa.append(pat[cl])

        p = jsonpatch.JsonPatch(pa)

        return p

    def test_get_input(self, patch = None):
        """extract input informations from the patch
            and stock them in different lists which serves 
            to locate datas"""

        if patch is not None and validate_schema(patch, schema_patch):

            for cle in patch:
                if cle == 'input':
                    pat = patch['input']

                    for cle in pat:
                        if cle == 'data':
                            
                            p = pat['data']

                            for cle in p:

                                if cle == 'alias':
                                    alias_data.append(p[cle])

                                elif cle == 'sup':
                                    sup_data.append(p[cle])

                                elif cle == 'source':
                                
                                    sources = p['source']

                                    for cle in sources:

                                        if cle == 'path':
                                            path_sources.append(sources[cle])

                                        elif cle == 'filter':
                                            filter_sources.append(sources[cle])

                        elif cle == 'schema':
                            
                            p = pat['schema']

                            for cle in p:

                                if cle == 'path':
                                    path_schema_data.append(p[cle])


    def test_get_output(self, patch = None):
        """extract input informations from the patch
            and stock them in different lists which serves 
            to save new datas"""

        if patch is not None and validate_schema(patch, schema_patch):

            for cle in patch:
                if cle == 'output':

                    pat = patch['output']

                    for cle in pat:
                        if cle == 'source':
                            
                            pa = pat['source']

                            for cle in pa:

                                if cle == 'path':
                                    path_output.append(pa[cle])

    def test_get_filter(self, filter_sources = None):
        """extract filter to apply it
            on data"""

        if filter_sources:
            for cle in filter_sources:

                fil = cle
                for cle in fil:

                    if cle == 'op':
                        op.append(fil[cle])

                    if cle == 'value':
                        value.append(fil[cle]) 


    def test_transfo(self):
        
        directory = os.listdir(path)

        for files in directory:
            if files.startswith('patch'):
                path_patch = os.path.join(path, files)

                with open(path_patch, "r") as f:
                    patch = json.load(f)

        #print patch

        directo = os.listdir(path)

        for file in directo:
            if file.startswith('schema_transformation'):
                path_schema_patch = os.path.join(path, file)

                with open(path_schema_patch, "r") as f:
                    schema_patch = json.load(f)

        #print schema_patch

        direct = os.listdir(path)

        for fil in direct:
            if fil.startswith('schema_V1'):
                path_data = os.path.join(path, fil)

                with open(path_data, "r") as f:
                    data = json.load(f)

        dirs = os.listdir(path)

        for fi in dirs:
            if fi.startswith('schema_base'):
                path_base = os.path.join(path, fi)

                with open(path_base, "r") as f:
                    base = json.load(f)
        #print base

        if jsonschema.validate(base, data) is None:

            for cle in patch:

                if cle == 'operations':
                    pat = patch['operations']

                    for cl in pat:
                        
                        if cl == 'remove':
                            pa.append(pat[cl])

                        elif cl == 'replace':
                            pa.append(pat[cl])

                        elif cl == 'move':
                            pa.append(pat[cl])

                        elif cl == 'add':
                            pa.append(pat[cl])

                        elif cl == 'copy':
                            pa.append(pat[cl])

        p = jsonpatch.JsonPatch(pa)
        print p

        result = p.apply(data)
        print result

        path_essai = os.path.join(path, "essai.json")

        with open(path_essai, "w") as f:
            json.dump(result, f, sort_keys = True, indent = 2, separators = (',', ':'))


if __name__ == '__main__':
    main()

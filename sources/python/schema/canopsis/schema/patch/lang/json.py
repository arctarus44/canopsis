from ..core import Patch, registerpatch

from ...lang.json import JsonSchema

from ..Transformation import patch

import jsonpatch


@registerpatch(JsonSchema)
class JSONPatch(Patch):

    def process(self, data):
        """define the correct process to return the patch 
        in the correct form and apply it on data"""
        
        patch = self.patch(data)
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
        result = p.apply(data)

        return result

    def save(self, data):
        inplace = self.JsonSchema['sup']

        if inplace == 'true':
            output = self.output(data)

            with open('output', "w") as f:
                jdon.dump(data, output)
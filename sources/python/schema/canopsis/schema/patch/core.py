 _PATCHS = {}

def registerpatch(schemacls, cls=None):

    def _recordpatch(cls):

        _PATCHS[schemacls] = cls

        return cls

    if cls is None:
        return _recordpatch

    else:
        return _recordpatch(cls)


def getpatch(schema, patch):
    """return the type of the patch, take 2 parameters
    schema : to get the language 
    patch : to return is type"""

    result = None

    cls = None

    for schemacls in _PATCHS:

        if isinstance(schema, schemacls):
            cls = _PATCHS[schemacls]
            break

    if cls is not None:
        result = cls(patch)

    return result


class Patch(object):

    def __init__(self, patch):

        self.patch = patch

    def process(self, data):

        raise NotImplementedError()

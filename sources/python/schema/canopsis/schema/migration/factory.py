# -*- coding: utf-8 -*-

import urlparse


class MigrationFactory(object):
    """instanciate the behavior class with the URL protocol
    it's possible to override the __setitem__ and the __getitem__
    by the register"""

    """take URI in parameter
    URI = protocol(*://)domain name(*.*.com)path(/...)"""

    def __init__(self):
        self.URL = {}

    def get(self, URI):
        protocol = get_protocol(URI)
        return protocol

    #on retourne cls pour pouvoir utiliser register en tant que décorateur
    def register(self, protocol, cls):
        self.URL[protocol] = cls()
        return cls()


class MetaMigration(type):
    """Metaclasse pour les IOInterfaces.
    Elle va écrire dans le dictionnaire URL à chaque fois qu'une classe utilisant cette metaclasse sera créée"""

    def __init__(cls, protocol, bases, dict):
        type.__init__(cls, protocol, bases, dict)
        newfactory = MigrationFactory()
        newfactory.register(protocol, cls)


class IOInterface(object):
    """abstract class to describe behavior functions
    of the different Input and Output for migration"""

    __metaclass__ = MetaMigration

    def load(self, URL):
        raise NotImplementedError()

    def transformation(self, data):
        raise NotImplementedError()

    def save(self, result, URL):
        raise NotImplementedError()


#Input File behavior class
class File(IOInterface):

    def load(self, URL, schema):

        data = schema.getresource(get_path(URL))
        schema.validate(data)
        return data

    def transformation(self, data, transfo_cls, schema):

        result = transfo_cls.apply_patch(data)
        schema.validate(result)
        return result

    def save(self, result, URL, schema):

        schema.save(result, get_path(URL))


#Input Folder behavior class
class Folder(IOInterface):

    def load(self, URL, schema):

        dirs = os.path.listdir(get_path(URL))
        for files in dirs :

            if os.path.isfile(files):
                data = schema.getresource(get_path(URL))
                schema.validate(data)
                return data

            elif os.path.isdir(files):
                path = os.path.join(get_path(URL), files)
                return load(self, path, schema)

            else:
                raise Exception('No such file or directory')


    def transformation(self, data, transfo_cls, schema):

        result = transfo_cls.apply_patch(data)
        schema.validate(result)
        return result

    def save(self, result, URL, schema):

        name = result['name']
        path = os.path.join(URL, name)
        schema.save(result, path)


#Input Dict behavior class
class Dict(IOInterface):

    def load(self, URL, schema):
        data = schema.getresource(get_path(URL))
        schema.validate(data)
        return data

    def transformation(self, data, transfo_cls, schema):
        result = transfo_cls.apply_patch(data)
        schema.validate(result)
        print result


#Input Storage behavior class
class Storage(IOInterface):

    def load(self, URL):
        data = mystorage.getItem(URL)
        return data

    def transformation(self, transfo_cls, URL, query=None):
        result = transfo_cls.apply_patch(data)
        return result

    def save(self, result, URL):
        mystorage.setItem(URL, result)


def get_protocol(URI):
    """This function take the protocol of the URI in parameter
    and return it"""
    uri = urlparse.urlsplit(URI)
    protocol = uri[0]

    return protocol

def get_path(url):
    """This function take the path from uri in parameter
    and return it"""
    uri = urlparse.urlsplit(url)
    path = uri[2]

    return path
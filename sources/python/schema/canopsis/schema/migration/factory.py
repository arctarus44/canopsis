
import urlparse

class MigrationFactory(object):
    """instanciate the behavior class with the URL protocol
    it's possible to override the __setitem__ and the __getitem__
    by the register"""

    def __init__(self):
        self.URL = {}

    #récupère le protocol à partir de l'URL
    #renvoie l'instance de cls correspondante
    """take URL in parameter
    URL = protocol(*://)domain name(*.*.com)path(/...)"""
    def __getitem__(self, URL):
        protocol = get_protocol(URL)

        return self.register(self.URL[protocol], URL)

    #attribut la cls au protocol
    def __setitem__(self, protocol, cls):
        self.URL[protocol] = cls
        # self.URL.__setitem__(protocol, cls)

    #définir le register directement dans la factory permet d'overrider
    #le __getitem__ et le __setitem__
    def register(self, cls, URL):
        raise NotImplementedError()

    def get_protocol(URL):
        uri = urlparse.urlsplit(URL)
        protocol = uri[0]

        return protocol


#définir l'interface de base
#propose des methodes utilisées par migration
class IOInterface(object):

    def load(self, URL):
        raise NotImplementedError()

    def transformation(self, data):
        raise NotImplementedError()

    def save(self, result, URL):
        raise NotImplementedError()
# -*- coding: utf-8 -*-

import urlparse


class MigrationFactory(object):
    """instanciate the behavior class with the URL protocol
    it's possible to override the __setitem__ and the __getitem__
    by the register"""

    def __init__(self):
        self.URL = {}

    """take URI in parameter
    URI = protocol(*://)domain name(*.*.com)path(/...)"""
    def __getitem__(self, URI):
        protocol = get_protocol(URI)

        return self.register(self.URL[protocol], URI)

    #attribut la cls au protocol
    def __setitem__(self, protocol, cls):
        self.URL[protocol] = cls
        # self.URL.__setitem__(protocol, cls)

    def register(self, cls, uri):
        raise NotImplementedError()


def get_protocol(URI):
    uri = urlparse.urlsplit(URI)
    protocol = uri[0]

    return protocol

#définir l'interface de base
#propose des methodes utilisées par migration







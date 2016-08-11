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

from canopsis.schema.core import Schema
from canopsis.schema.lang.json import JsonSchema
from canopsis.schema.transformation.core import Transformation
import os
import urlparse

class IOInterface(object):

    def load(self, URL):
        raise NotImplementedError()

    def transformation(self, data):
        raise NotImplementedError()

    def save(self, result, URL):
        raise NotImplementedError()


#Input File behavio class
class File(IOInterface):

    def load(self, URL, schema):

        data = schema.getresource(URL)
        schema.validate(data)
        return data

    def transformation(self, data, transfo_cls, schema):

        result = transfo_cls.apply_patch(data)
        schema.validate(result)
        return result

    def save(self, result, URL, schema):

        schema.save(result, URL)

class Dict(IOInterface):

    def load(self, URL, schema):
        data = schema.getresource(URL)
        schema.validate(data)
        return data

    def transformation(self, data, transfo_cls, schema):
        result = transfo_cls.apply_patch(data)
        schema.validate(result)
        print result

class CanopsisStorage(IOInterface):

    def load(self, URL, query):
        mystorage = Middleware.get_middleware_by_uri(URL)
        mystorage.connect()

        cursor = mystorage.find(query)
        for data in cursor:
            return data

    def transformation(self, transfo_cls, URL, query):
        mystorage = Middleware.get_middleware_by_uri(URL)
        mystorage.connect()

        cursor = mystorage.find(query)
        for data in cursor:
            result = transfo_cls.apply_patch(data)

        return result

    def save(self, result, URL):
        mystorage = Middleware.get_middleware_by_uri(URL)
        mystorage.connect()
        mystorage.put_elements(result, URL)


class MigrationFactory(object):
    """instanciate the behavior class with the URL protocol
    it's possible to override the __setitem__ and the __getitem__
    by the register"""

    def __init__(self):
        self.URL = {'file':'File', 'dict':'Dict', 'mongodb-default':'CanopsisStorage'}

    """take URI in parameter
    URI = protocol(*://)domain name(*.*.com)path(/...)"""
    def get(self, URI):
        protocol = get_protocol(URI)

        if self.URL[protocol] == 'File':
            return File()
        elif self.URL[protocol] == 'Dict':
            return Dict()
        elif self.URL[protocol] == 'CanopsisStorage':
            return CanopsisStorage()

    def register(self, protocol, cls):

        self.URL[protocol] = cls


def get_protocol(URI):
    uri = urlparse.urlsplit(URI)
    protocol = uri[0]

    return protocol

def get_path(url):
    uri = urlparse.urlsplit(url)
    path = uri[2]

    return path


def migrate(path_transfo):
    """the migrate function transform data and save them"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_transfo = schema.getresource(path_transfo)

    inp = schema_transfo['input']
    output = schema_transfo['output']
    path_v1 = schema_transfo['path_v1']
    path_v2 = schema_transfo['path_v2']

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    myinp = MigrationFactory().get(inp)
    data = myinp.load(get_path(inp), schema)

    myout = MigrationFactory().get(output)
    result = myout.transformation(data, transfo, schema)
    myout.save(result, get_path(output), schema)

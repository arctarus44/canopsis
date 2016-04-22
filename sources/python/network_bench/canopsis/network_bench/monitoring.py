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
from client import Client
from functools import wraps
from utils import singleton_per_scope
from inspect import getcallargs


def Network_decorator_in(func):
    """
    decorator to send the object in the bench network system
    """
    @wraps(func)
    def monitor(*args, **kwargs):

        arguments = getcallargs(func, *args, **kwargs)
        event = arguments['event']

        file = open('/home/tgosselin/fichierdelog2', 'a')
        file.write('reception: {0}\n-----------------\n'.format(event))
        file.close()

        client = singleton_per_scope(Client)
        client.receive(event)

        result = func(event, *args, **kwargs)

        return result

    return monitor


def Network_decorator_out(func):
    """
    decorator to send the object in the bench network system
    """
    @wraps(func)
    def monitor(*args, **kwargs):

        arguments = getcallargs(func, *args, **kwargs)
        event = arguments['event']

        client = singleton_per_scope(Client)
        client.send(event)

        file = open('/home/tgosselin/fichierdelog2', 'a')
        file.write('envoi: {0}\n-----------------\n'.format(event))
        file.close()

        result = func(*args, **kwargs)

        return result

    return monitor

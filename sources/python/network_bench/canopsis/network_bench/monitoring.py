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


def Network_decorator(func):
    """
    decorator to send the object in the bench network system
    """
    @wraps(func)
    def monitor(event, *args, **kwargs):

        client = singleton_per_scope(Client)
        client.send_receive(event)

        result = func(event, *args, **kwargs)

        return result

    return monitor

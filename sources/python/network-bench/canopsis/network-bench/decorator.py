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


def Netork_decorator(func):
    """
    decorator to send the object in the bench network system
    """
    @wraps(func)
    def monitor(*args, **kwargs):

        result = func(*args, **kwargs)

        return result

    return monitor


@Configurable(paths='network-bench/network-bench.conf')
class Infos(object):

    def __init__(self,host=None, port=None, *args, **kwargs):
        super(Infos, self).__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def get_host(self):
        return str(self.host)

    def get_port(self):
        return int(self.port)

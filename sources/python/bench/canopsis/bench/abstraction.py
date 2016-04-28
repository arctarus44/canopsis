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

from manager import BenchPython
from b3j0f.conf import Category, Configurable
from monitoring import monitoring


@Configurable(paths='bench/bench.conf', conf=Category('BENCH'))
class Abstraction(object):

    def __init__(
            self,
            uri=None,
            metrics=None,
            params=None,
            frequecy=30,
            params=None,
            bounds=None,
            duration=None,
            * args,
            **kwargs):
        super(Abstraction, self).__init__(*args, **kwargs)
        b = benchpython(uri=uri)

    @monitoring
    def exec(self, params, *arg, **kwargs):
        pass

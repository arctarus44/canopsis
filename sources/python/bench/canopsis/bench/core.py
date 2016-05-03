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

from b3j0f.middleware.url import URLMiddleware


class Bench(URLMiddleware):

    __protocol__ = 'bench'

    def __init__(self, *args, **kwargs):
        super(Bench, self).__init__(*args, **kwargs)


class BenchPython(Bench):

    __scope__ = 'python'

    def __init__(self, scope, path, *args, **kwargs):
        super(BenchPython, self).__init__(*args, **kwargs)


class BenchMongo(Bench):

    __scope__ = 'mongo'

    def __init__(self, scope, path, *args, **kwargs):
        super(BenchPython, self).__init__(*args, **kwargs)

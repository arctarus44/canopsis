# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2015 "Capensis" [http://www.capensis.com]
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

from b3j0f.middleware import URLMiddleware
from monitoring import monitoring

class BenchMiddleware(URLMiddlware):
    """
    Middleware class to instance methods to bench
    """

    def __init__(self, *args, **kwargs):
        super(BenchMiddleware, self).__init__(*args, **kwargs)

    def instanciate(self):
        """
        method to instanciate functions to bench them
        """

    @monitoring
    def launch(self, func):
        """
        execute the method to bench it
        """

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

from __future__ import unicode_literals

from threading import Thread, Event
from time import sleep


class IOCounter(Thread):

    def __init__(self, process, *args, **kwargs):
        super(IOCounter, self).__init__(*args, **kwargs)
        self.process = process
        self.loop = Event()
        self.io = process.io_counters()

    def run(self):
        self.loop.set()
        while self.loop.is_set():
            self.io = self.process.io_counters()
            sleep(0.001)

    def stop(self):
        self.loop.clear()

    def get_io(self):
        return self.io

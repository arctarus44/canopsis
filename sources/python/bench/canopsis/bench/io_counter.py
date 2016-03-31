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

from threading import Thread
from time import sleep
from publisher import Publisher

from psutil import net_io_counters

from canopsis.common.utils import singleton_per_scope


class IOCounter(object):

    def __init__(self, engine, pid, *args, **kwargs):
        super(IOCounter, self).__init__(*args, **kwargs)

        self.publisher = singleton_per_scope(
            Publisher,
            scope='{0}-{1}'.format(engine.name, pid),
            kwargs={'engine': engine, 'pid': pid})

        self.io_in_before = net_io_counters().bytes_recv
        self.io_out_before = net_io_counters().bytes_sent

        periodical_counter = Periodical_counter(self)
        periodical_counter.start()

    def check_io(self):
        bytes_recv = net_io_counters().bytes_recv
        bytes_sent = net_io_counters().bytes_sent
        values = [
            bytes_recv - self.io_in_before,
            bytes_sent - self.io_out_before
        ]
        self.publisher.addio_array(values)
        self.io_in_before = bytes_recv
        self.io_out_before = bytes_sent


class Periodical_counter(Thread):

    def __init__(self, iocounter, *args, **kwargs):
        super(Periodical_counter, self).__init__(*args, **kwargs)
        self.iocounter = iocounter

    def run(self):
        sleep(15)
        self.iocounter.check_io()

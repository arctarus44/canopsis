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

from psutil import disk_io_counters
from canopsis.common.utils import singleton_per_scope


class DiksMonitor(object):

    def __init__(self, engine, pid, *args, **kwargs):
        super(DiksMonitor, self).__init__(*args, **kwargs)

        self.engine = engine

        self.publisher = singleton_per_scope(
            Publisher,
            scope='{0}-{4}'.format(engine.name, pid),
            kwargs={'engine': engine, 'pid': pid})

        self.read_before = disk_io_counters().read_bytes
        self.write_before = disk_io_counters().write_bytes
        self.read_time_before = disk_io_counters().read_time
        self.write_time_before = disk_io_counters().write_time

        periodical_counter = Periodical_counter(self)
        periodical_counter.start()

    def check_io(self):
        bytes_read = disk_io_counters().read_bytes
        bytes_write = disk_io_counters().write_bytes
        read_time = disk_io_counters().read_time
        write_time = disk_io_counters().write_time

        values = [
            bytes_read - self.read_before,
            bytes_write - self.write_before,
            read_time - self.read_time_before,
            write_time - self.write_time_before
        ]

        self.publisher.add_disk_info(values)

        self.read_before = bytes_read
        self.write_before = bytes_write
        self.read_time_before = read_time
        self.write_time_before = write_time


class Periodical_counter(Thread):

    def __init__(self, disk_monitor, *args, **kwargs):
        super(Periodical_counter, self).__init__(*args, **kwargs)
        self.disk_monitor = disk_monitor

    def run(self):
        sleep(15)
        self.disk_monitor.check_io()

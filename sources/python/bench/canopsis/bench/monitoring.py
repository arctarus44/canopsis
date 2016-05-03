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

from functools import wraps
from math import pow
from os import getpid
from threading import Thread, Event
from time import sleep, time
from b3j0f.conf import Configurable, Category
#from canopsis.common.utils import singleton_per_scope
from psutil import Process
#from publisher import Publisher


class Mem(Thread):

    """
    cpu and memory analysis while an engine's function is running
    """

    def __init__(self, process, *args, **kwargs):
        super(Mem, self).__init__(*args, **kwargs)
        self.process = process
        self.loop = Event()
        self.memory_percent = 0
        info = Info()
        self.memory = info.get_memory()

    def run(self):
        self.loop.set()
        while self.loop.is_set():
            self.memory_percent = self.process.memory_percent()
            sleep(0.0001)

    def stop(self):
        self.loop.clear()

    def get_memory(self):
        return ((self.memory_percent * self.memory) / 100)


@Configurable(paths='bench/bench.conf', conf=Category('BENCH'))
class Info(object):

    def get_cadence(self):
        return float(self.cadence) * pow(10, 9)

    def get_memory(self):
        return int(self.memory)

    def get_mode(self):
        return self.benchmode == 'True'


def monitoring(func):
    """
    engine's function decorator to analyze execution time.

    :param function: the decorated function
    """
    @wraps(func)
    def monitor(*args, **kwargs):

        result = None

        info = Info()

        cadence = info.get_cadence()

        pid = getpid()
        process = Process(pid)

        mem_thread = Mem(process)

        mem_thread.start()

        now = time()

        try:
            result = func(*args, **kwargs)

        except Exception:
            mem_thread.stop()

        else:
            elapsed_time = time() - now

            cpu_time = process.cpu_times()

            mem_thread.stop()
            mem_thread.join()

            memory = mem_thread.get_memory()

            statements = (cpu_time.user + cpu_time.system) * cadence

            file = open('/home/tgosselin/fichierdelog', 'a')
            file.write('time: {0}s, statements: {1}stmts, mem: {2}kb'.format(
                elapsed_time,
                statements,
                memory))
            file.close()

            """
            metric_array = [elapsed_time, memory, statements]
            publisher = singleton_per_scope(
                Publisher,
                scope='{0}-{1}'.format(engine.name, pid),
                kwargs={'engine': engine, 'pid': pid})

            publisher.addmetrics_array(metric_array)
            """
        return result

    return monitor

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
from time import time
from b3j0f.conf import Configurable, Category
from psutil import Process
from check_mem import Mem
from check_cpu import Cpu
from check_io import IOCounter


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

        pid = getpid()
        process = Process(pid)

        mem_thread = Mem(process, info.get_memory())
        mem_thread.start()

        io_thread = Cpu(process, info.get_cadence())
        io_thread.start()

        cpu_thread = IOCounter(process)
        cpu_thread.start()

        now = time()

        try:
            result = func(*args, **kwargs)

        except Exception:
            mem_thread.stop()
            io_thread.stop()
            cpu_thread.stop()

        else:
            elapsed_time = time() - now

            statements = cpu_thread.get_statements()
            memory = mem_thread.get_memory()
            io = io_thread.get_io()

            mem_thread.stop()
            mem_thread.join()

            cpu_thread.stop()
            cpu_thread.join()

            io_thread.stop()
            io_thread.join()

            file = open('/home/tgosselin/fichierdelog', 'a')
            file.write('time: {0}s, statements: {1}stmts, mem: {2}kb, io:{3}'.format(
                elapsed_time,
                statements,
                memory,
                io))
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

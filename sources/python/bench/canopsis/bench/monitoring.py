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

from time import sleep, time
from threading import Thread, Event
from psutil import Process
import os
from functools import wraps
from canopsis.engines.core import publish
from canopsis.event import forger
from re import sub


class ThreadCPU(Thread):
    """
    cpu and memory analysis while an engine's function is running
    """

    def __init__(self, pid, *args, **kwargs):
        super(ThreadCPU, self).__init__(*args, **kwargs)

        self.process = Process(pid)
        self.loop = Event()
        self.memory_percent = 0
        self.average_cpu_percent = 0

        infos = Info()
        self.cadence = infos.get_cadence()
        self.memory = infos.get_memory()

    def run(self):

        cpt = 0
        total_cpu_percent = 0

        self.loop.set()

        while self.loop.is_set():

            total_cpu_percent += self.process.cpu_percent()

            self.memory_percent = self.process.memory_percent()
            cpt += 1
            self.average_cpu_percent = total_cpu_percent / cpt
            sleep(0.0001)

    def stop(self):

        self.loop.clear()

    def get_average_cpu(self):

        return ((self.average_cpu_percent * self.cadence) / 100)

    def get_memory(self):

        return ((self.memory_percent * self.memory) / 100)


def monitoring(func):
    """
    engine's function decorator to analyze execution time.
    """
    @wraps(func)
    def monitor(engine, *args, **kwargs):

        result = None

        pid = os.getpid()

        cpu_thread = ThreadCPU(pid)

        cpu_thread.start()

        now = time()

        try:
            result = func(engine, *args, **kwargs)

        except Exception:
            cpu_thread.stop()

        else:
            elapsed_time = time() - now

            cpu_thread.stop()
            cpu_thread.join()

            memory = cpu_thread.get_memory()
            average_cpu = cpu_thread.get_average_cpu()

            perf_data_array = [
                {
                    'metric': 'elapsed_time',
                    'value': round(elapsed_time, 3),
                    'unit': 's'
                }, {
                    'metric': 'memory',
                    'value': memory,
                    'unit': 'kb'
                }, {
                    'metric': 'cpu',
                    'value': average_cpu,
                    'unit': 'Ghz'
                }
            ]

            msg = 'name: {0}, time :{1} s, memory: {2} kb, cpu {3} Ghz'.format(
                engine.name,
                elapsed_time,
                memory,
                average_cpu
            )

            event = forger(
                connector='Engine',
                connector_name='engine',
                event_type='check',
                source_type='resource',
                resource='{0}-{1}'.format(engine.name, cpu_thread.process.pid),
                state=0,
                state_type=1,
                output=msg,
                perf_data_array=perf_data_array
            )

            publish(event=event, publisher=engine.amqp)

        return result

    return monitor


class Info(object):
    """
    file parser to get architecture's informations
    """

    def __init__(self):
        self.file_info = open('/opt/canopsis/etc/bench/architecture.conf', 'r')
        self.memory = sub(r'[a-z     :A-Z]', '', self.file_info.readline())
        self.number_of_core = int(self.file_info.readline().split(':')[1])
        self.cadence = sub(r'[a-z    :A-Z]', '', self.file_info.readline())

    def get_memory(self):
        return int(self.memory)

    def get_number_of_core(self):
        return self.number_of_core

    def get_cadence(self):
        return float(self.cadence)

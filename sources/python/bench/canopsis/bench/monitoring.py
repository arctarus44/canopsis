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


class ThreadCPU(Thread):

    def __init__(self, pid, *args, **kwargs):
        super(ThreadCPU, self).__init__(*args, **kwargs)

        self.process = Process(pid)
        self.loop = Event()
        self.memory_percent = 0
        self.average_cpu_percent = 0

    def run(self):
        cpt = 0
        total_cpu_percent = 0

        self.loop.set()
        while self.loop.is_set():
            total_cpu_percent += self.process.cpu_percent(interval=0.001)
            self.memory_percent = self.process.memory_percent()
            cpt += 1
            self.average_cpu_percent = total_cpu_percent / cpt
            sleep(0.001)

    def stop(self):
        self.loop.clear()

    def get_average_cpu_percent(self):
        return self.average_cpu_percent

    def get_memory_percent(self):
        return self.memory_percent


def monitoring(func):
    @wraps(func)
    def monitor(engine, *args, **kwargs):

        pid = os.getpid()

        cpu_thread = ThreadCPU(pid)

        cpu_thread.start()

        now = time()
        result = func(*args, **kwargs)
        elapsed_time = time() - now

        cpu_thread.stop()
        cpu_thread.join()

        memory_percent = cpu_thread.get_memory_percent()
        average_cpu_percent = cpu_thread.get_average_cpu_percent()

        print('result: {0}'.format(result))
        print('elapsed time: {0}'.format(elapsed_time))
        print('memory percent: {0}'.format(memory_percent))
        print('average cpu percent: {0}'.format(average_cpu_percent))

        perf_data_array = [
            {
                'retention': engine.perfdata_retention,
                'metric': 'name',
                'value': engine.name},
            {
                'retention': engine.perfdata_retention,
                'metric': 'sec_per_evt',
                'value': round(elapsed_time, 3),
                'unit': 's'},
            {
                'retention': engine.perfdata_retention,
                'metric': 'memory_percent',
                'value': round(memory_percent, 2),
                'unit': 'percent'},
            {
                'retention': engine.perfdata_retention,
                'metric': 'cpu_percent',
                'value': round(average_cpu_percent, 1),
                'unit': 'percent'}
        ]

        msg = 'name: {0}, time :{1} s, memo"ry: {2} %%, cpu {3} %%'.format(
            engine.name,
            elapsed_time,
            memory_percent,
            average_cpu_percent
        )

        event = forger(
            connector='Engine',
            connector_name='engine',
            event_type='check',
            source_type='resource',
            resource=engine.amqp_queue,
            state=0,
            state_type=1,
            output=msg,
            perf_data_array=perf_data_array
        )

        publish(event=event, publisher=engine.amqp)

        return result

    return monitor

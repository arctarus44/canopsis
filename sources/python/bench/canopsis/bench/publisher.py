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

from time import sleep
from threading import Thread
from canopsis.event import forger
from canopsis.engines.core import publish


class Publisher(object):

    """
    this class publish engine's benchs results
    """

    def __init__(self, engine=None, pid=None, *args, **kwargs):
        super(Publisher, self).__init__(*args, **kwargs)

        self.metrics_array = []
        self.engine = engine
        self.pid = pid
        timer = ThreadTimer(self)
        timer.start()

    def addmetrics_array(self, metrics_array):
        self.metrics_array.append(metrics_array)

    def cleanmetrics_array(self):
        self.metrics_array = []

    def addList(self, metrics):
        self.metrics_array.append(metrics)

    def average(self):

        statements = 0
        memory = 0
        elapsed_time = 0
        io_in = 0
        io_out = 0
        cpt = 0

        for item in self.metrics_array:
            elapsed_time += item[0]
            memory += item[1]
            statements += item[2]
            io_in += item[3]
            io_out += item[4]
            cpt += 1

        return [elapsed_time / cpt,
                memory / cpt,
                (statements / cpt) / 1000,
                io_in / cpt,
                io_out / cpt]

    def publish_metrics(self):
        if len(self.metrics_array) > 0:
            values = self.average()

            perf_data_array = [
                {
                    'metric': 'elapsed_time',
                    'value': values[0],
                    'unit': 's'
                }, {
                    'metric': 'memory',
                    'value': values[1],
                    'unit': 'kb'
                }, {
                    'metric': 'cpu',
                    'value': values[2],
                    'unit': 'statements'
                }, {
                    'metric': 'in',
                    'value': values[3],
                    'unit': 'bytes'
                }, {
                    'metric': 'out',
                    'value': values[4],
                    'unit': 'bytes'
                }
            ]

            template = 'Time: {}s, RAM: {}kb, CPU: {}kstmts, in: {}B, out: {}B'
            msg = template.format(*values)

            event = forger(
                connector='Engine',
                connector_name='engine',
                event_type='check',
                source_type='resource',
                resource='{0}-{1}'.format(
                    self.engine.name,
                    self.pid
                ),
                state=0,
                state_type=1,
                output=msg,
                perf_data_array=perf_data_array
            )

            publish(event=event, publisher=self.engine.amqp)


class ThreadTimer(Thread):

    def __init__(self, publisher, *args, **kwargs):
        super(ThreadTimer, self).__init__(*args, **kwargs)
        self.publisher = publisher

    def run(self):
        while True:
            sleep(60)
            self.publisher.publish_metrics()
            self.publisher.cleanmetrics_array()

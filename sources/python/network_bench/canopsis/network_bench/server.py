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
import zmq
from threading import Thread, Event
from zmq import Context
from time import time, sleep
from b3j0f.conf import Configurable, Category
from publisher import Publisher


@Configurable(paths='network_bench/network_bench.conf', conf=Category('NETWORK'))
class Serv(Thread):

    def __init__(self, host='127.0.0.1', port=4242, *args, **kwargs):
        super(Serv, self).__init__(*args, **kwargs)

        self.host = host
        self.port = port

        self.loop = Event()

        self.context = Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind('tcp://{0}:{1}'.format(self.host, self.port))

        self.sent = []
        self.received = []

        self.times = []

        self.publisher = Publisher()

    def run(self):

        proc = Process(self)
        proc.start()

        self.loop.set()

        while self.loop.is_set():
            result = self.receiver.recv_pyobj()
            if result[2] == 'received':
                self.received.append(result)
            elif result[2] == 'sent':
                self.sent.append(result)

    def stop(self):
        self.loop.clear()

    def clean_list(self):
        now = time()
        cpt = 0
        for i in self.sent:
            if ((now - i[1]) > 30):
                self.sent.pop(cpt)
                cpt += 1

        print('{0} events deleted in sent\n--------\n'.format(cpt))

        cpt = 0
        for i in self.received:
            if ((now - i[1]) > 30):
                self.received.pop(cpt)
                cpt += 1

        print('{0} events deleted in received\n--------\n'.format(cpt))

    def gentimes(self):
        now = time()
        for i in self.sent:
            for j in self.received:
                if i[0] == j[0]:
                    self.times.append(float(j[1]) - float(i[1]))
        print('temps de calcul :{0} \n\n'.format(time() - now))

        self.publish(self.times)
        self.times = []

    def publish_message(self, message):
        self.publisher.message(message)

    def publish(self, times):
        self.publisher.get_time(time)


class Process(Thread):
    def __init__(self, server, *args, **kwargs):
        super(Process, self).__init__(*args, **kwargs)
        self.server = server
        self.loop = Event()

    def run(self):
        self.loop.set()
        while self.loop.is_set():
            sleep(30)
            self.server.gentimes()
            sleep(10)
            self.server.clean_list()

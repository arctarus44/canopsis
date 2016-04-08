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
from time import time
from b3j0f.conf import Configurable


@Configurable(paths='network_bench/network_bench.conf')
class Serv(Thread):
    def __init__(self, host=None, port=None, *args, **kwargs):
        super(Serv, self).__init__(*args, **kwargs)

        self.host = host
        self.port = port

        self.loop = Event()

        self.context = Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind('tcp://{0}:{1}'.format(self.host, self.port))

        self.tmp = []


    def run(self):

        self.loop.set()

        while self.loop.is_set():
            now = time()
            print('reception')
            result = self.receiver.recv_pyobj()
            print('reçu {0}'.format(result))
            self.processing(result)

            if (time() - now) > 300:
                self.clean_list()

    def processing(self, result):
        test = self.already_in(result[0])
        if (test == -1):
            self.tmp.append(result)
        else:
            print('temps d\'envoi: {0}'.format(
                float(result[1]) - float(test)))

    def already_in(self, obj):
        cpt = 0
        for i in self.tmp:
            if (i[0] == obj):
                time = i[1]
                self.tmp.pop(cpt)
                return time

            cpt += 1

        return -1

    def stop(self):
        self.loop.clear()

    def clean_list(self):
        now = time()
        cpt = 0
        for i in self.tmp:
            if ((i[1] - now) > 30):
                self.tmp.pop(cpt)
            else:
                cpt += 1

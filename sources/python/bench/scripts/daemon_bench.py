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

from b3j0f.conf import Configurable
from threading import Thread, Event
from zmq import Context, PULL
from canopsis.bench.set_functions_and_methods import launch

class DaemonBench(object):

    def __init__(self, *args, **kwargs):
        super(DaemonBench, self).__init__(*args, **kwargs)
        self.receiver = Receiver(self)
        self.receiver.start()

    def bench_maf(self, maf):
        """
            :arg list maf: list of methods and functions

           method to bench mathods and functions
        """
        launch(maf)


class Receiver(Thread):

    def __init__(self, daemon_bench, *args, **kwargs):
        super(Receiver, self).__init__(*args, **kwargs)
        self.loop = Event()
        self.daemon_bench = daemon_bench
        info = Info()

        self.context = Context()
        self.socket = self.context.socket(PULL)
        self.socket.bind('tcp://{0}:{1}'.format(info.ip, info.port))

    def run(self):
        self.loop.set()

        while self.loop.is_set():
            obj = self.socket.recv_pyobj()
            for maf in obj:
                self.daemon_bench.bench_maf(maf)

    def stop(self):
        self.loop.clear()


@Configurable(paths='/home/tgosselin/Documents/bordel/canopsis-propre/canopsis/sources/python/bench/etc/bench/daemon_bench.conf')
class Info(object):
    pass

if __name__ == '__main__':
    daemon_bench = DaemonBench()


# coding: utf-8
from __future__ import unicode_literals
import zmq
from threading import Thread, Event
from zmq import Context
from time import time
from pass_object import Object_pass
from b3j0f.conf import Configurable, Category


@Configurable(paths='network-bench/network-bench.conf')
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
            if ((i[1] - now) > 30) :
                self.tmp.pop(cpt)
            else:
                cpt += 1


# -*- coding:utf-8 -*-
from b3j0f.conf import Configurable
from zmq import Context, PUSH
import sys

@Configurable(paths='/opt/canopsis/etc/bench/bench.conf')
class Info(object):
    """
    class in charge to get information in configuration file
    """

class Connexion(object):
    def __init__(self, *args, **kwargs):
        info = Info()

        self.host = info.host
        self.hosts = self.host.split(';')

        self.port = info.port

        self.methodsandfunctions = info.methodsandfunctions
        self.methodsandfunctions_tab = self.methodsandfunctions.split(';')

        self.context = Context()

    def send_uri(self):
        for host in self.hosts:
            try:
                socket = self.context.socket(PUSH)
                socket.connect('tcp://{0}:{1}'.format(host, self.port))
                socket.send_pyobj(self.methodsandfunctions_tab)
                socket.close()
            except ImportError:
                print 'connexion to {0} impossible'.format(host)
        return 'conf diffused'


if __name__ == '__main__':
    co = Connexion()
    co.send_uri()
    print 'done'
    sys.exit(1)

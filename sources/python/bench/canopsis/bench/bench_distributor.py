# -*- coding:utf-8 -*-
from b3j0f.conf import Configurable
from zmq import Context, PUSH


@Configurable(paths='/home/tgosselin/Documents/bordel/canopsis-propre/canopsis/sources/python/bench/etc/bench/bench.conf')
class Info(object):
	"""
	class in charge to get information in configuration file
	"""

class Connexion(object):
	"""
	class in charge to distribute urls on each canopsis instances.
	"""
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
                socket.send_pyobj(self.uri_methodsandfunctions)
                socket.close()
            except ImportError:
                print 'connexion to {0} impossible'.format(host)
        return 'conf diffused'


co = Connexion()
print co.send_uri()

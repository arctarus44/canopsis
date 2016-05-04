from b3j0f.conf import Configurable
from zmq import Context, PUSH


@Configurable(paths='/home/tgosselin/Documents/bordel/canopsis-propre/canopsis/sources/python/bench/etc/bench/bench.conf')
class Info(object):
    pass


class Connexion(object):

    def __init__(self, *args, **kwargs):
        info = Info()

        self.host = info.host
        self.hosts = self.host.split(';')

        self.port = info.port

        self.uris = info.uri
        self.uri_tab = self.uris.split(';')

        self.context = Context()

    def send_uri(self):
        for host in self.hosts:
            try:
                socket = self.context.socket(PUSH)
                socket.connect('tcp://{0}:{1}'.format(host, self.port))
                socket.send_pyobj(self.uri_tab)
                socket.close()
            except ImportError:
                print 'connexion to {0} impossible'.format(host)
        return 'conf diffused'


co = Connexion()
print co.send_uri()

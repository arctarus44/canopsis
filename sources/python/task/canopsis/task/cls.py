from core import set_task, get_task  # , unset_task


class Cls(object):

    def __init__(self, *args, **kwargs):
        super(Cls, self).__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        if isinstance(value, basestring):
            try:
                set_task(self, value, '_beat_processing')
            except ImportError:
                self.logger.error('Impossible to load {0}'.format(value))

        else:
            if value is None:
                value = self.beat_processing

            self._beat_processing = value

    def _getattr__(self, attr):
        try:
            get_task(attr)
        except ImportError:
            self.logger.error('Impossible to load {0}'.format(attr))

    # def __delattr__(self, name):
    #    try:
    #        unset_task(self, attr)
    #    except ImportError:
    #        self.logger.error('Impossible to load {0}'.format(attr))

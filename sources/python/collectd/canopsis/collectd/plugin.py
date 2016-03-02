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
# --------------------------------

from canopsis.middleware.registry import MiddlewareRegistry
from canopsis.configuration.configurable.decorator import conf_paths
from canopsis.configuration.configurable.decorator import add_category
from canopsis.configuration.model import Configuration, Category, Parameter
from canopsis.common.utils import lookup

from six import string_types
import collectd


CONF_PATH = 'collectd/plugin.conf'
CATEGORY = 'COLLECTDPLUGIN'
CONTENT = [
    Parameter('interval', int),
    Parameter('init_callback'),
    Parameter('read_callback'),
    Parameter('shutdown_callback'),
    Parameter('write_callback'),
    Parameter('flush_callback'),
    Parameter('log_callback'),
    Parameter('notification_callback')
]


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class CollectDPlugin(MiddlewareRegistry):
    @property
    def interval(self):
        if not hasattr(self, '_interval'):
            self.interval = None

        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def init_callback(self):
        if not hasattr(self, '_init_callback'):
            self.init_callback = None

        return self._init_callback

    @init_callback.setter
    def init_callback(self, value):
        if value is None:
            value = init_callback

        if isinstance(value, string_types):
            value = lookup(value)

        self._init_callback = value

    @property
    def read_callback(self):
        if not hasattr(self, '_read_callback'):
            self.read_callback = None

        return self._read_callback

    @read_callback.setter
    def read_callback(self, value):
        if value is None:
            value = read_callback

        if isinstance(value, string_types):
            value = lookup(value)

        self._read_callback = value

    @property
    def shutdown_callback(self):
        if not hasattr(self, '_shutdown_callback'):
            self.shutdown_callback = None

        return self._shutdown_callback

    @shutdown_callback.setter
    def shutdown_callback(self, value):
        if value is None:
            value = shutdown_callback

        if isinstance(value, string_types):
            value = lookup(value)

        self._shutdown_callback = value

    @property
    def write_callback(self):
        if not hasattr(self, '_write_callback'):
            self.write_callback = None

        return self._write_callback

    @write_callback.setter
    def write_callback(self, value):
        if value is None:
            value = write_callback

        if isinstance(value, string_types):
            value = lookup(value)

        self._write_callback = value

    @property
    def flush_callback(self):
        if not hasattr(self, '_flush_callback'):
            self.flush_callback = None

        return self._flush_callback

    @flush_callback.setter
    def flush_callback(self, value):
        if value is None:
            value = flush_callback

        if isinstance(value, string_types):
            value = lookup(value)

        self._flush_callback = value

    @property
    def log_callback(self):
        if not hasattr(self, '_log_callback'):
            self.log_callback = None

        return self._log_callback

    @log_callback.setter
    def log_callback(self, value):
        if value is None:
            value = log_callback

        if isinstance(value, string_types):
            value = lookup(value)

        self._log_callback = value

    @property
    def notification_callback(self):
        if not hasattr(self, '_notification_callback'):
            self.notification_callback = None

        return self._notification_callback

    @notification_callback.setter
    def notification_callback(self, value):
        if value is None:
            value = notification_callback

        if isinstance(value, string_types):
            value = lookup(value)

        self._notification_callback = value

    def __init__(
        self,
        interval=None,
        init_callback=None,
        read_callback=None,
        shutdown_callback=None,
        write_callback=None,
        flush_callback=None,
        log_callback=None,
        notification_callback=None,
        *args, **kwargs
    ):
        super(CollectDPlugin, self).__init__(*args, **kwargs)

        if interval is not None:
            self.interval = interval

        if init_callback is not None:
            self.init_callback = init_callback

        if read_callback is not None:
            self.read_callback = read_callback

        if shutdown_callback is not None:
            self.shutdown_callback = shutdown_callback

        if write_callback is not None:
            self.write_callback = write_callback

        if flush_callback is not None:
            self.flush_callback = flush_callback

        if log_callback is not None:
            self.log_callback = log_callback

        if notification_callback is not None:
            self.notification_callback = notification_callback

    def register(self):
        collectd.register_config(self.on_config)
        collectd.register_init(self.on_init)
        collectd.register_read(self.on_read, self.on_interval)
        collectd.register_shutdown(self.on_shutdown)
        collectd.register_write(self.on_write)
        collectd.register_flush(self.on_flush)
        collectd.register_log(self.on_log)
        collectd.register_notification(self.on_notification)

    def parse_config(self, confobj):
        conf = {}

        for child in confobj.children:
            if len(child.children):
                conf[child.key] = self.parse_config(confobj)

            elif len(child.values) > 1:
                conf[child.key] = child.values

            else:
                conf[child.key] = child.values[0]

        return conf

    def on_config(self, confobj):
        conf = self.parse_config(confobj)

        params = [
            Parameter(key, value=conf[key])
            for key in conf
        ]

        conf = Configuration(
            Category(
                'collectd_config',
                *params
            )
        )

        self.apply_configuration(conf=conf)

    def on_init(self):
        self.init_callback(plugin=self)

    def on_read(self):
        self.read_callback(plugin=self)

    def on_shutdown(self):
        self.shutdown_callback(plugin=self)

    def on_write(self, values):
        self.write_callback(plugin=self, values=values)

    def on_flush(self, timeout, identifier):
        self.flush_callback(
            plugin=self,
            timeout=timeout,
            identifier=identifier
        )

    def on_log(self, severity, message):
        self.log_callback(plugin=self, severity=severity, message=message)

    def on_notification(self, notification):
        self.notification_callback(plugin=self, notification=notification)


def init_callback(plugin, **_):
    pass


def read_callback(plugin, **_):
    pass


def shutdown_callback(plugin, **_):
    pass


def write_callback(plugin, values, **_):
    pass


def flush_callback(plugin, timeout, identifier, **_):
    pass


def log_callback(plugin, severity, message, **_):
    pass


def notification_callback(plugin, notification, **_):
    pass


def init_collectd_plugin(confpath):
    decorator = conf_paths(confpath)
    cls = type('collectd_plugin', (CollectDPlugin,), {})
    cls = decorator(cls)

    obj = cls()
    obj.register()

    return obj

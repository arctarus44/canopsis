# -*- coding: utf-8 -*-

from time import time

from canopsis.middleware.registry import MiddlewareRegistry

from canopsis.configuration.configurable.decorator import (
    add_category, conf_paths
)
from canopsis.timeserie.timewindow import get_offset_timewindow, TimeWindow

CONF_PATH = 'baselin/manager.conf'
CATEGORY = 'BASELINE'

@conf_path(CONF_PATH)
@add_category(CATEGORY)
class Baseline(MiddlewareRegistry):
    """Baseline"""

    BASELINE_STORAGE = 'baseline_storage'
    CONTEXT_MANAGER = 'context'

    def __init__(self, *args, **kwargs):
        """__init__

        :param *args:
        :param **kwargs:
        """
        super(Baseline, self).__init__(self, *args, **kwargs)

    def get_baselines(self, baseline_name, timewindow=None):
        """get_baselines"""
        self[Baseline.STORAGE].get(self, baseline_name, timewindow=timewindow)

    def put(self, name, value):
        point = (time(), value)
        self[Baseline.STORAGE].put(name, point)



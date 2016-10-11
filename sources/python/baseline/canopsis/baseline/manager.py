# -*- coding: utf-8 -*-

from time import time

from canopsis.middleware.registry import MiddlewareRegistry

from canopsis.configuration.configurable.decorator import (
    add_category, conf_paths
)
from canopsis.timeserie.timewindow import get_offset_timewindow, TimeWindow
from canopsis.context.manager import Context

@conf_paths('baseline/baseline.conf')
@add_category('BASELINE')
class Baseline(MiddlewareRegistry):
    """Baseline"""

    STORAGE = 'baseline_storage'
    CONTEXT_MANAGER = 'context'

    def __init__(self, *args, **kwargs):
        """__init__

        :param *args:
        :param **kwargs:
        """
        super(Baseline, self).__init__(*args, **kwargs)

    def get_baselines(self, baseline_name, timewindow=None):
        """get_baselines"""
        if timewindow is None:

            _timewindow = TimeWindow(0,time())

        else:
            _timewindow = tw

        return self[Baseline.STORAGE].get(data_id=baseline_name, timewindow=_timewindow)


    def put(self, name, value):
        point = (time(), value)
        self[Baseline.STORAGE].put(data_id=name, points=[point])


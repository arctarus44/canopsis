# -*- coding: utf-8 -*-

from canopsis.common.ws import route
from canopsis.common.utils import singleton_per_scope
from canopsis.baseline.manager import Baseline
from canopsis.timeserie.timewindow import TimeWindow, Period


def exports(ws):
    manager = singleton_per_scope(Baseline)

    @route(ws.application.get, payload=['baseline_name', 'timewindow'])
    def baseline(baseline_name, timewindow=None):
        return manager.get_baselines(baseline_name, timewindow=None)

    @route(ws.application.put, payload=[
        'baseline_name',
        'mode',
        'value',
        'period',
        'margin',
        'component',
        'resource',
        'check_frequency'])
    def baselineconf(
            baseline_name,
            mode,
            period,
            margin,
            component,
            resource,
            check_frequency,
            value=None):
        return manager.add_baselineconf(
            baseline_name,
            mode,
            period,
            margin,
            component,
            resource,
            check_frequency,
            value=value
            )

    @route(ws.application.delete, payload=['baseline_name'])
    def baselineconf(baseline_name):
        return manager.remove_baselineconf(baseline_name)

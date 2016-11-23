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
        'entity',
        'resource',
        'check_frequency',
        'aggregation_method',
        'value_name',
        'state',
        'output'])
    def baselineconf(
            baseline_name,
            mode,
            period,
            margin,
            entity,
            resource,
            check_frequency,
            state,
            output,
            value=None,
            aggregation_method='sum',
            value_name=None,
            tw_start=-1,
            tw_stop=-1):
        return manager.add_baselineconf(
            baseline_name,
            mode,
            period,
            margin,
            entity,
            resource,
            check_frequency,
            state,
            output,
            value,
            aggregation_method,
            value_name,
            tw_start,
            tw_stop
            )

    @route(ws.application.delete, payload=['baseline_name'])
    def baselineconf(baseline_name):
        return manager.remove_baselineconf(baseline_name)

    @route(ws.application.put, payload=[
        'mode',
        'baseline_name',
        'check_frequency',
        'value_name'])
    def baselineconffeed(mode, baseline_name, check_frequency, value_name=None):
        return manager.add_baselineconffeed(mode, baseline_name, check_frequency, value_name);

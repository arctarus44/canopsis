# -*- coding: utf-8 -*-

from canopsis.common.ws import route
from canopsis.common.utils import singleton_per_scope
from canopsis.baseline.manager import Baseline
from canopsis.timeserie.timewindow import TimeWindow, Period

f = open('/home/tgosselin/fichierdelog3', 'a')
f.write('coucou \n')
f.close()

def exports(ws):
    manager = singleton_per_scope(Baseline)

    @route(ws.application.get, payload=['baseline_name', 'timewindow'])
    def baseline(baseline_name, timewindow=None):
        return manager.get_baselines(baseline_name, timewindow=None)

    @route(ws.application.post)
    def test():
        return '{"coucou":"voila"}'

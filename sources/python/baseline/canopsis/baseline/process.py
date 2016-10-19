# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from canopsis.common.utils import singleton_per_scope
from canopsis.task.core import register_task
from canopsis.context.manager import Context

from canopsis.baseline.manager import Baseline

baseline_manager = Baseline()

@register_task
def event_processing(engine, event, logger=None, **kwargs):

    manager = baseline_manager
    name = event['baseline_name']

    if manager.check_frequency(name):

        value = 1

        manager.put(name, value)

    else:

        if 'perf_data' in event:

            value = event['perf_data']
            manager.put(name, value)

        elif 'perf_data_array' in event:

            value_name = manager.get_value_name(name)
            value = None
            for i in event['perf_data_array']:
                if i['metric'] == value_name:
                    value = i['value']

            if value = None:
                print('bad baseline configuration')
                raise Exception

            manager.put(name, value)
        else:
            print('to build a baseline based on value, a perf_data event is needed')


@register_task
def beat_processing(engine, logger=None, **kwargs):

    baseline_manager.beat()

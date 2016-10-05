# -*- coding: utf-8 -*-

from canopsis.common.utils import singleton_per_scope
from canopsis.task.core import register_task

from canopsis.alerts.manager import Baseline

manager = Baseline()

@register_task
def event_processing(engine, event):

    name = event['baseline_name']
    value = 1

    manager.put(name, value)

@register_task
def beat_processing(engine):
    pass

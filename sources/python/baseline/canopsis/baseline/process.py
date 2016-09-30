# -*- coding: utf-8 -*-

from canopsis.common.utils import singleton_per_scope
from canopsis.task.core import register_task

from canopsis.alerts.manager import Baseline

@register_task
def event_processing(engine, event):

    manager = Baseline()

    if match_filter(event):
        manager.store(event)

@register_task
def beat_processing(engine):
    pass

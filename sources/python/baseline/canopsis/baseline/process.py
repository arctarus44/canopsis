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
    value = 1

    manager.put(name, value)

@register_task
def beat_processing(engine):
    pass

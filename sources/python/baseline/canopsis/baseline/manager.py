# -*- coding: utf-8 -*-

from time import time

from canopsis.middleware.registry import MiddlewareRegistry

from canopsis.configuration.configurable.decorator import (
    add_category, conf_paths
)
from canopsis.timeserie.timewindow import get_offset_timewindow, TimeWindow
from canopsis.context.manager import Context

from canopsis.engines.core import publish
from canopsis.old.rabbitmq import Amqp


@conf_paths('baseline/baseline.conf')
@add_category('BASELINE')
class Baseline(MiddlewareRegistry):
    """Baseline"""

    STORAGE = 'baseline_storage'
    CONFSTORAGE = 'baselineconf_storage'
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

            _timewindow = TimeWindow(0, time())

        else:
            _timewindow = timewindow

        return self[Baseline.STORAGE].get(
            data_id=baseline_name,
            timewindow=_timewindow)

    def put(self, name, value):
        point = (time(), value)
        self[Baseline.STORAGE].put(data_id=name, points=[point])

    def add_baselineconf(
        self,
        baseline_name,
        mode,
        period,
        margin,
        entity,
        resource,
        value=None
    ):
        element = {
            'baseline_name': baseline_name,
            'mode': mode,
            'value': value,
            'period': period,
            'margin': margin,
            'entity': entity,
            'resource': resource
        }

        result = self[Baseline.CONFSTORAGE].put_element(
            element,
            _id=baseline_name)

        self.manage_baselines_list(element)

        return result

    def manage_baselines_list(self, element):

        if not len(self[Baseline.CONFSTORAGE].get_elements(query={'_id': 'baselines'})) > 0:
            self[Baseline.CONFSTORAGE].put_element(
                {'_id': 'baselines', 'list': []})

        baselines = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': 'baselines'}):
            baselines = i

        l = baselines['list']
        index = -1
        for k, i in enumerate(l):
            if element['baseline_name'] in i:
                index = k
        if index == -1:
            if element['mode'] == 'floatting':
                period = 2 * element['period']
                l.append({element['baseline_name']: time() + period})
            else:
                l.append({element['baseline_name']: time() + element['period']})
        else:
            l[index][element['baseline_name']] = time() + element['period']

        baselines['list'] = l
        self[Baseline.CONFSTORAGE].put_element(baselines)

    def beat(self):
        now = time()
        baselines = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': 'baselines'}):
            baselines = i
        baseline_list = baselines['list']

        for i in baseline_list:
            if now > i.items()[0][1]:
                self.reset_timestamp(i.items()[0][0])
                self.check_baseline(i.items()[0][0], i.items()[0][1])

    def reset_timestamp(self, baseline_name):
        baseline = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': baseline_name}):
            baseline = i
        period = baseline['period']

        baselines = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': 'baselines'}):
            baselines = i
        baseline_list = baselines['list']

        index = -1
        for k, i in enumerate(baseline_list):
            if baseline_name in i:
                index = k

        baseline_list[index][baseline_name] = baseline_list[
            index][baseline_name] + period
        baselines['list'] = baseline_list
        self[Baseline.CONFSTORAGE].put_element(baselines)

    def check_baseline(self, baseline_name, timestamp):

        baseline_conf = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': baseline_name}):
            baseline_conf = i

        tw = TimeWindow(start=timestamp -
                        baseline_conf['period'], stop=timestamp)
        values = self.get_baselines(baseline_name, tw)

        reference = []

        tw_start = 0
        tw_stop = 0

        if baseline_conf['mode'] == 'static':

            reference_value = baseline_conf['value']
            margin_up = float(
                baseline_conf['value'] + baseline_conf['value'] * baseline_conf['margin'] / 100)
            margin_down = float(
                baseline_conf['value'] - baseline_conf['value'] * baseline_conf['margin'] / 100)

            if len(values) > margin_up or len(values) < margin_down:
                self.send_alarm(
                    baseline_conf['entity'], baseline_conf['resource'])
            return

        elif baseline_conf['mode'] == 'floatting':

            tw_start = timestamp - 2 * baseline_conf['period']
            tw_stop = timestamp - baseline_conf['period']

        elif baseline_conf['mode'] == 'fix_last':

            tw_start = baseline_conf['tw_start']
            tw_stop = baseline_conf['tw_stop']

        elif baseline_conf['mode'] == 'fix':

            tw_start = baseline_conf['tw_start']
            tw_stop = baseline_conf['tw_stop']

        tw = TimeWindow(start=tw_start, stop=tw_stop)
        reference = self.get_baselines(baseline_name, timewindow=tw)

        margin_up = float(
            len(reference) + len(reference) * baseline_conf['margin'] / 100)
        margin_down = float(
            len(reference) - len(reference) * baseline_conf['margin'] / 100)

        if len(values) > margin_up or len(values) < margin_down:
            self.send_alarm(baseline_conf['entity'], baseline_conf['resource'])
        elif baseline_conf['mode'] == 'fix_last':
            baseline_conf['tw_start'] = timestamp - baseline_conf['period']
            baseline_conf['tw_stop'] = time_stamp
            self[Baseline.CONFSTORAGE].put_element(baseline_conf)

    def send_alarm(self, entity, resource):
        self.logger.error('alarm alarm alarm alarm!!!\n')
        alarm_event = {
            "component": "test",
            "resource": "rfeeder",
            "source_type": "resource",
            "event_type": "check",
            "connector": "feeder",
            "connector_name": "namefeeder",
            "output": "output",
            "state": 3
        }

        publish(alarm_event, Amqp())

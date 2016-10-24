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
        """get_baselines

        get list of values, timestamp in database

        :param baseline_name:
        :param timewindow: a time window
        """
        if timewindow is None:

            _timewindow = TimeWindow(0, time())

        else:
            _timewindow = timewindow

        return self[Baseline.STORAGE].get(
            data_id=baseline_name,
            timewindow=_timewindow)

    def get_value_name(self, baseline_name):
        """get_value_name

        get in database the value name to check for the baseline

        :param baseline_name:
        """
        baseline_conf = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': baseline_name}):
            baseline_conf = i
        return baseline_conf['value_name']

    def check_frequency(self, baseline_name):
        """check_frequency

         check in baseline conf if baseline is based on frequency or values of events

        :param baseline_name:
        """
        baseline_conf = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': baseline_name}):
            baseline_conf = i

        return baseline_conf['check_frequency'] == 'true'

    def put(self, name, value):
        """put

        :param name:  baseline name
        :param value:
        """
        point = (time(), value)
        self[Baseline.STORAGE].put(data_id=name, points=[point])

    def add_baselineconf(
        self,
        baseline_name,
        mode,
        period,
        margin,
        component,
        resource,
        check_frequency,
        value,
        aggregation_method='sum',
        value_name=None
    ):
        """add_baselineconf

        :param baseline_name:
        :param mode:
        :param period:
        :param margin:
        :param component:
        :param resource:
        :param check_frequency:
        :param value:
        :param aggregation_method:
        :param value_name:
        """
        element = {
            'baseline_name': baseline_name,
            'mode': mode,
            'value': value,
            'period': period,
            'margin': margin,
            'component': component,
            'resource': resource,
            'check_frequency': check_frequency,
            'aggregation_method': aggregation_method,
            'value_name': value_name
        }

        result = self[Baseline.CONFSTORAGE].put_element(
            element,
            _id=baseline_name)

        self.manage_baselines_list(element)

        return result

    def remove_baselineconf(self, baseline_name):
        """remove_baselineconf

        remove baseline conf in database

        :param baseline_name:
        """

        baselines = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': 'baselines'}):
            baselines = i

        l = baselines['list']
        index = -1
        for k, i in enumerate(l):
            if baseline_name in i:
                index = k

        l.pop(index)
        baselines['list'] = l
        self[Baseline.CONFSTORAGE].put_element(baselines)

        return self[Baseline.CONFSTORAGE].remove_elements(ids=baseline_name)

    def manage_baselines_list(self, element):
        """manage_baselines_list

        manage in database the list of running baselines with end period timestamp

        :param element: a baseline conf element
        """

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
                l.append({element['baseline_name']
                         : time() + element['period']})
        else:
            l[index][element['baseline_name']] = time() + element['period']

        baselines['list'] = l
        self[Baseline.CONFSTORAGE].put_element(baselines)

    def beat(self):
        """beat"""

        now = time()
        baselines = {}
        baseline_list = []
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': 'baselines'}):
            baselines = i
        if not baselines == {}:
            baseline_list = baselines['list']

        for i in baseline_list:
            if now > i.items()[0][1]:
                self.reset_timestamp(i.items()[0][0])
                self.check_baseline(i.items()[0][0], i.items()[0][1])

    def reset_timestamp(self, baseline_name):
        """reset_timestamp

        set timestamp in database to define the end of the next period

        :param baseline_name:
        """
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
        """check_baseline

        check if the baseline is ok or not

        :param baseline_name:
        :param timestamp: end period timestamp
        """

        baseline_conf = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id': baseline_name}):
            baseline_conf = i

        aggregation_method = 'sum'
        if 'aggregation_method' in baseline_conf:
            aggregation_method = baseline_conf['aggregation_method']

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

            if self.aggregation(values, aggregation_method) > margin_up or self.aggregation(values, aggregation_method) < margin_down:
                self.send_alarm(
                    baseline_conf['component'], baseline_conf['resource'])
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
            self.aggregation(reference, aggregation_method) + self.aggregation(reference, aggregation_method) * baseline_conf['margin'] / 100)
        margin_down = float(
            self.aggregation(reference, aggregation_method) - self.aggregation(reference, aggregation_method) * baseline_conf['margin'] / 100)

        if self.aggregation(values, aggregation_method) > margin_up or self.aggregation(values, aggregation_method) < margin_down:
            self.send_alarm(
                baseline_conf['component'], baseline_conf['resource'])

        elif baseline_conf['mode'] == 'fix_last':
            baseline_conf['tw_start'] = timestamp - baseline_conf['period']
            baseline_conf['tw_stop'] = time_stamp
            self[Baseline.CONFSTORAGE].put_element(baseline_conf)

    def send_alarm(self, component, resource):
        """send_alarm

        send an alarm if the baseline is not normal

        :param component: alarm's component
        :param resource: alarm's resource
        """
        alarm_event = {
            "component": component,
            "resource": resource,
            "source_type": "resource",
            "event_type": "check",
            "connector": "baseline_engine",
            "connector_name": "baseline",
            "state": 3
        }

        publish(alarm_event, Amqp())

    def values_sum(self, values):
        """values_sum

        :param values: values list
        :return: the sum of values list
        :rtype: float
        """
        ret_val = 0
        for i in values:
            ret_val = ret_val + i[1]
        return ret_val

    def value_average(self, values):
        """value_average

        :param values: value list
        :return: the avergae of  list values
        :rtype: float
        """
        ret_val = 0
        k = 0
        for k, i in enumerate(values):
            ret_val = ret_val + i[1]
        return ret_val / k

    def value_max(self, values):
        """value_max

        :param values: values list
        :return: the max values of the list
        :rtype: float
        """
        ret_val = 0
        for i in values:
            if i[1] > ret_val:
                ret_val = i[1]
        return ret_val

    def value_min(self, values):
        """value_min

        :param values:list
        :return: the min value of the list
        :rtype: float
        """
        ret_val = values[0][1]
        for i in values:
            if i[1] < ret_val:
                ret_val = i[1]
        return ret_val

    def aggregation(self, values, aggregation_method):
        """aggregation

        :param values: list of values and timestamp from baseline events
        :param aggregation_method: str 

        :return: aggregated values
        :rtype: float
        """

        ret_val = 0
        if aggregation_method == 'sum':
            return self.values_sum(values)

        elif aggregation_method == 'average':
            return self.value_average(values)

        elif aggregation_method == 'min':
            return self.value_min(values)

        elif aggregation_method == 'max':
            return self.value_max(values)

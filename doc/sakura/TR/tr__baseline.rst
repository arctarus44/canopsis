.. _TR__Alarm:

==========
Base lines
==========

This document specifies baselines in Canopsis, and its implementation.

.. contents::
   :depth: 3


Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Thomas Gosselin", "2016/10/03", "0.1", "Document creation", ""

Contents
========

Baseline
--------

 -  

Frontend Baseline

in the canopsis ui, there is a configuration menu to configure baseline options:
    - filter(base line configuration for event_filter)
    - static or learning
    - period and period type(floating, fix_last, time_period)
    - number of event or expected value
    - margin
    - aggregation method
    - entity and component(alarm)

Backend Baseline

Baseline engine
---------------

Base line engine received events from an event_filter and store them into Influxdb with a time stamp, a metric (1 if we want events frequency) and the baseline_id(filter_name).

for each steps of baseline, the engine will generate metrics with stored events. 

 the manager generate metrics with events in influxdb, those methods can be used by the web server to get informations and put them in the ui

manager
-------

.. code-block:: python

    def get_baselines(self, baseline_name, timewindow=None):
        """get_baselines
        get list of values, timestamp in database
        :param baseline_name:
        :param timewindow: a time window
        """

    def get_value_name(self, baseline_name):
        """get_value_name
        get in database the value name to check for the baseline
        :param baseline_name:
        """

    def check_frequency(self, baseline_name):
        """check_frequency
         check in baseline conf if baseline is based on frequency or values of events
        :param baseline_name:
        """

    def put(self, name, value):
        """put
        :param name:  baseline name
        :param value:
        """

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

    def remove_baselineconf(self, baseline_name):
        """remove_baselineconf
        remove baseline conf in database
        :param baseline_name:
        """

    def manage_baselines_list(self, element):
        """manage_baselines_list
        manage in database the list of running baselines with end period timestamp
        :param element: a baseline conf element
        """

    def beat(self):
        """beat"""

    def reset_timestamp(self, baseline_name):
        """reset_timestamp
        set timestamp in database to define the end of the next period
        :param baseline_name:
        """

    def check_baseline(self, baseline_name, timestamp):
        """check_baseline
        check if the baseline is ok or not
        :param baseline_name:
        :param timestamp: end period timestamp
        """

    def send_alarm(self, component, resource):
        """send_alarm
        send an alarm if the baseline is not normal
        :param component: alarm's component
        :param resource: alarm's resource
        """

    def values_sum(self, values):
        """values_sum

        :param values: values list
        :return: the sum of values list
        :rtype: float
        """

    def value_average(self, values):
        """value_average

        :param values: value list
        :return: the avergae of  list values
        :rtype: float
        """

    def value_max(self, values):
        """value_max

        :param values: values list
        :return: the max values of the list
        :rtype: float
        """

    def value_min(self, values):
        """value_min

        :param values:list
        :return: the min value of the list
        :rtype: float
        """

    def aggregation(self, values, aggregation_method):
        """aggregation

        :param values: list of values and timestamp from baseline events
        :param aggregation_method: str

        :return: aggregated values
        :rtype: float
        """

Baseline Storage
----------------

in influxdb, the engine will store every events who arrive from the event filter, with a time stamp , a value and the baseline id

with the manager we will interact with influx to have average sum...

the manager will remove useless events 

Baseline web service
--------------------

the baseline webservice can put baseline configurations  and get baseline informations to draw baselines in ui

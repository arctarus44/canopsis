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
    - threshold
    - aggregation method
    - entity (for the alarm)

Backend Baseline

Baseline engine
---------------

Base line engine received events from an event_filter and store them into Influxdb with a time stamp, a metric (1 if we want events frequency) and the baseline_id(filter_name).

for each steps of baseline, the engine will generate metrics with stored events. 

there is methods in the manager to generate metrics with events in influxdb, those methods can be used by the web server to get informations and put them in the ui




Baseline Storage
----------------

in influxdb, the engine will store every events who arrive from the event filter, with a time stamp , a value and the baseline id

with the manager we will interact with influx to have average sum...

the manager will remove useless events 

Baseline web service
--------------------

the baseline webservice can put baseline configurations  and get baseline informations to draw baselines in ui

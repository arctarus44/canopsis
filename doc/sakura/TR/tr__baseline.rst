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

Base line engine received events from an event_filter and store them into Influxdb.



Baseline Storage
----------------

Baseline web service
--------------------

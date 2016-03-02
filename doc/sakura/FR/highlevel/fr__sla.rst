.. _FR__SLA:

=======================
Service Level Agreement
=======================

This document describes the SLA process in Canopsis.

.. contents::
   :depth: 3

References
==========

List of referenced functional requirements:

 - :ref:`FR::Context <FR__Context>`
 - :ref:`FR::Alarm <FR__Alarm>`
 - :ref:`FR::Selector <FR__Selector>`
 - :ref:`FR::Engine <FR__Engine>`
 - :ref:`FR::Event <FR__Event>`
 - :ref:`FR::Metric <FR__Metric>`

Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "David Delassus", "2016/02/15", "0.1", "Document creation", ""

Contents
========

.. _FR__SLA__Desc:

Description
-----------

In Canopsis, there is two use cases of SLA:

 - :ref:`alarms <FR__Alarm>` management (acknowledgment and resolution) duration
 - availability

.. _FR__SLA__Contract:

Contract
--------

For each type of SLA, there is a type of contract with the following informations:

 - a name: will be used to associate the contract to an :ref:`entity <FR__Context__Entity>`
 - warning thresholds: will be used to create an alarm (in **MINOR** state) when the contract is not fulfilled
 - critical thresholds: will be used to create an alarm (in **MAJOR** state) when the contract is not fulfilled

A specific permission **MUST** exist to allow users to create, edit or remove contracts.

.. _FR__SLA__AlarmsManagement:

Alarms Management
-----------------

The following :ref:`metrics <FR__Metric>` **MUST** be produced:

 - duration between alarm apparition and its acknowledgment
 - duration between alarm apparition and its resolution

The associated contract **MUST** provide two warning/critical thresholds, one for
each one of those metrics.

.. _FR__SLA__Availability:

Availability
------------

When a :ref:`selector <FR__Selector>` is computed, its alarm history is explored
on a time window (specified in the selector).

For each state the selector went through, the cumulative duration is computed, and
the following :ref:`metrics <FR__Metric>` **MUST** be produced:

  - ``cps_pct_info``: percentage of time window in **INFO** state
  - ``cps_pct_minor``: percentage of time window in **MINOR** state
  - ``cps_pct_major``: percentage of time window in **MAJOR** state
  - ``cps_pct_critical``: percentage of time window in **CRITICAL** state
  - ``cps_availability_percent``: synonym of ``cps_pct_info``
  - ``cps_availability_duration``: total availability duration
  - ``cps_alerts_percent``: sum of ``cps_pct_minor``, ``cps_pct_major``, and ``cps_pct_critical``
  - ``cps_alerts_duration``: total alerts duration

The associated contract **MUST** provide a warning/critical threshold for the ``cps_availability_percent`` metric.

.. _FR__SLA__Engine:

Engine
------

The selector :ref:`engine <FR__Engine>` **SHOULD** send the processed selector to
the SLA engine in order to compute its availability SLA.

The SLA engine **MUST** fetch the :ref:`metrics <FR__Metric>` produced for in order to compute the *alarms management* SLA.

The computed SLA **MUST** be produced as a :ref:`SLA event <FR__Event__Sla>`.

.. _FR__SLA__Association:

Contract association to entities
--------------------------------

The engine ``event_filter`` **SHOULD** provide an ``assocContract`` action, allowing
the linking between an entity and a SLA contract.

After this association, the user must fulfill the contract for this entity.
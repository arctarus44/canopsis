.. _FR__Bench:

=====
Bench
=====

information about how canopsis is running with statistics and metrics.

.. contents::
   :depth: 2

References
==========

List of referenced functional requirements...

- :ref:`FR::Other-Title <FR__Other_Title>`

Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Thomas Gosselin", "2016/03/10", "1.0", "Creation", " "

Contents
========

.. _FR__Bench__Desc:

Description
-----------

The bench system will analyze methods and functions describes in a configuration file with uri and parameters.

It will analyze 4 differents points:
	- How many operations Canopsis can process each seconds.
	- How many space Canopsis use on hard drive.
	- The RAM quantity needed by Canopsis.
	- The processing time by tasks.


.. _FR__Bench__Example:

Example
-------

as example: cleaner

the cleaner is an engine who check each event incoming in Canopsis.

If you want to bench the event_processing function from alert engine, you can write an uri in the configuration file:

bench://python/canopsis/alerts/process/event_processing?...

cleaner uses two software bricks:
	- engine
	- rabbit

let see all points for the cleaner example:
	- operations/seconds: number of events each seconds by cleaner engine while the engine is running.
	- cleaner engine not need storage space.
	- the RAM quantity used by the engine while running.
	- the time needed by the cleaner engine to check an event.

once informations recovered, Canopsis will process them and save them in the database.

.. _FR__bench__Metrics:

Metrics
-------

.. csv-table::
	:header:"metric", "unit", "Description"
	"op_per_second", "operation/second", "number of operation"
	"roù", "Mo, "the memory space"
	"ram", "Mo", "RAM used"
	"time_processing", "s", "processing time by task"

.. _FR__bench_Usage:

Usage
-----

We can use the bench system to estimate the power needed for canopsis.

In the pre-production phase, we can estimate the power based on users and needs.

With the bench system we can adapt canopsis to needs.

The system can be use to do monitoring of canopsis.

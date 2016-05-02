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

It will analyze differents points:
	- How many statements benched functions use.
	- How many space functions write on the hard drive.
	- The RAM quantity needed by functions.
	- The processing time.
        - I/O quantity received and send by functions. 

.. _FR__Bench__Example:

Example
-------

as example I can take the example of bench the engine alerts:

The alerts engine is an engine who check each event incoming in Canopsis and drop them if the event is invalid.

If you want to bench the event_processing function from alerts-engine, you can write this uri in the configuration file:

.. code-block:: text

    bench://python/canopsis/alerts/process/event_processing

On this uri, you can add parameters:
   
    - param: Parameters to execute the function
    - metrics: Metrics you want, you can choose to check just the RAM consumption  you can just choose this metric..
    - duration: The bench duration, if you want to bench the function for 10 minutes, you can define it in parameters.
    - iteration: Or you can define how many times you want to execute the function, for example execute 1000 times the bench function.
    - frequency: You can define a frequency to publish bench result for example publish results every 10 seconds.
    - bound: You can define a bound to trigger an alert for example.

The alerts engine uses two software bricks:
	- engine
	- rabbit

let see all points for the cleaner example:
	- operations/seconds: number of events each seconds by alerts engine while the engine is running.
	- alerts engine not need storage space.
	- the RAM quantity used by the engine while running.
	- the time needed by the cleaner engine to check an event.
        - I/O send and received by the alers engine.


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

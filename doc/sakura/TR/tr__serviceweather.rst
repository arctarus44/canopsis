TR Service Weather
------------------

.. contents:: Table of contents


Context
=======

Introduction
^^^^^^^^^^^^

A new widget serviceweather was made. It was done with a static dataset that aggregates several types of data in Canopsis.
The goal of this backend project is to implement the webservice that will provide the data to the frontend instead of the current dataset.

Work
^^^^
Your work has to be done in the weather project in Python directory

* Write a webservice that provide the dataset given below --> create the route /weather/get-serviceweather.
* A manager exist but could be completed.
* Test the manager with unittest.
* The webservice will be tested by ourselves with the frontend widget.


Backend
=======

Dataset
^^^^^^^

The returned dataset is a list of selectors that also contain details about entities they aggregate.
Here is an the wanted data model that the webservice has to send to the frontend:

.. code-block::

 {
    "status": {
      "a": "engine.selector",
      "_t": "statusinc",
      "m": "Application 0 in status 1",
      "t": 1476883468,
      "val": 1
    },
    "entity_id": "/selector/canopsis/engine/app1",
    "sla_text": "7j-24h/24h",
    "criticity": "standard",
    "snooze": {
      "a": "engine.alerts",
      "_t": "snooze",
      "m": "Application 1 is snoozed for 600s",
      "t": 1476857157,
      "val": 1476857757
    },
    "org": "org3",
    "display_name": "Application 1",
    "name": "app1",
    "pbehavior": [
      {
        "isActive": false,
        "dtend": 1476885600,
        "dtstart": 1476878400,
        "rrule": {
          "text": "Every Week",
          "rule": "FREQ=WEEKLY"
        },
        "behavior": "maintenance"
      }
    ],
    "ack": {
      "a": "weatherdev",
      "_t": "ack",
      "m": "Ack de weatherdev",
      "t": 1476841146,
      "val": null
    },
    "linklist": [],
    "entities": [
      {
        "status": {
          "a": "engine.selector",
          "_t": "statusdec",
          "m": "Component 3 in status 1",
          "t": 1476857970,
          "val": 1
        },
        "linklist": [
          {
            "url": "http://urltoticket.local/?id=38",
            "category": "incident",
            "label": "ticket"
          }
        ],
        "entity_id": "/component/testconn/testconn1/comp3",
        "display_name": "Component 3",
        "name": "ent3",
        "pbehavior": [
          {
            "dtend": 1476885600,
            "dtstart": 1476878400,
            "rrule": {
              "text": "Every Week",
              "rule": "FREQ=WEEKLY"
            },
            "isActive": false,
            "behavior": "robotko"
          },
          {
            "dtend": 1476885600,
            "dtstart": 1476878400,
            "rrule": {
              "text": "Every Week",
              "rule": "FREQ=WEEKLY"
            },
            "isActive": true,
            "behavior": "maintenance"
          }
        ],
        "ack": {
          "a": "fde",
          "_t": "ack",
          "m": "Ack de fde",
          "t": 1476861402,
          "val": null
        },
        "sla_text": "5j-7h30/18h15",
        "criticity": "sensitive",
        "state": {
          "a": "root",
          "_t": "changestate",
          "m": "Component 3 in state 0",
          "t": 1476844046,
          "val": 0
        },
        "snooze": {
          "a": "root",
          "_t": "snooze",
          "m": "Component 3 is snoozed for 600s",
          "t": 1476801235,
          "val": 1476801835
        },
        "org": "org1"
      }
    ],
    "state": {
      "a": "root",
      "_t": "stateinc",
      "m": "Application 0 in state 0",
      "t": 1476839340,
      "val": 0
    }
 }

* entity_id : Selector id, built with resource, component, connector and connector_name
* status : Selector status. Computed with entities status
* state : Selector state. Computed with entities state
* sla_text: String sla output
* name: Application name
* display_name: Application display name
* linklist: Linklist related to the selector
* criticity: String that indicates the selector criticity level
* pbehavior: Selector periodic behavior
* snooze: Selector snooze
* ack: Selector ack, computed with entities ack
* entities: List of entities aggregated by the selector. They have the same attributes than selectors


Manager
^^^^^^^

.. csv-table:: Methods
   :header: "#", "Name", "Args", "Comments"
   :widths: 5, 40, 80, 80

* The manager has to aggregate all needed data for building the dataset to send to the frontend
* Method: get_dataset()

Selectors
^^^^^^^^^

This feature aims to display filtered selectors with all information you can give (including related entities).
So that's why you first have to get some information in selector project. Selectors are stored in the ``object``.
You can find them with this filter: ``db.object.find({'crecord_type': 'selector'})``

pbehavior
^^^^^^^^^

Information related to the periodic behaviors are in ``pbehaviors`` project

.. code-block::

    {
      "event_type": "pbehavior",
      "pbehavior_name": "downtime",
      "start": ts,
      "end": ts,
      "duration": ts,
      + classic event fields
    }


Alarms
^^^^^^

Some fields needed for building the dataset can be found in ``periodical-alarm`` collection:

* entity_id : Selector id, built with resource, component, connector and connector_name
* status : Selector status. Computed with entities status
* state : Selector state. Computed with entities state
* snooze: Selector snooze
* ack: Selector ack, computed with entities ack


Linklist
^^^^^^^^

Concerning the linklist attribute, you can find information about it on the linklist project.
The rules concerning the linklists are stored in the ``default_linklist`` collection and the computed links are store in the ``default_entitylink`` collection.

Getting started
^^^^^^^^^^^^^^^

Sources
~~~~~~~

Changes must be commited in a new branch `feature-weather`. This branch must
contains :

* serviceweather manager in
  ``sources/python/weather/canopsis/weather/manager.py``.
* serviceweather webservice in
  ``sources/python/webcore/canopsis/webcore/services/weather.py``. This file
  contains proxy functions that must rely on the manager. Routes should be
  requestable : <ip>:<port>/serviceweather

Environment
~~~~~~~~~~~

The development environment could be the same as for pbehavior project.

You should work with local sources and push your modifications on the
environment to test. Here at capensis we tend to use ``rsync``.

Once you changed some code, you can reload it with :

  * ``service amqp2engines* mrestart`` for the engine
  * or ``service webserver restart``

Logs
~~~~

Log files that should be used are :

  * /opt/canopsis/var/log/serviceweathermanager.log
  * /opt/canopsis/var/log/webserver.log

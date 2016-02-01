.. _FR__Context:

=======
Context
=======

This document describes the Context requirements of Canopsis.

.. contents::
   :depth: 3

References
==========

List of referenced functional requirements:

Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "David Delassus", "2016/01/21", "0.2", "Context v2 Draft 01", ""
   "David Delassus", "2015/09/01", "0.1", "Document creation", ""

Contents
========

.. _FR__Context__Desc:

Description
-----------

All data published in Canopsis are (or can be) related to a contextual entity.
For example:

 * alerts on a host or service are related to the host/service entity
 * perfdata published by a metric are related to the metric entity
 * downtimes (and other behaviors) are set on host/service entities
 * ...

Starting from an entity, we **MUST** be able to access all data related to it.

.. _FR__Context__Entity:

Entity
------

An entity is composed of:

 * a name
 * a type, amongst the following types:
    * ``typed_connector``: describing the class of connector used to produce data
    * ``named_connector``: describing the specific connector used to produce data
    * ``component``: in *supervision*, it is the host, in *EUE* it is the application
    * ``resource``: in *supervision*, it is the service, in *EUE* it is the feature
    * ``metric``: describing performance data with its metadata
    * ``system``: describing another system storing data in Canopsis, like:
       * alerting
       * periodic storage used for perfdata
       * key/value storage used for metadata
       * periodic behaviors
       * ...
 * a unique identifier

It is linked to other entities in a HyperGraph model where edges describe the
entity's composition.

Entities can be linked together with other edges, like:

 * correlation edges: determining the impact of one entity over others (useful for root cause/consequence analysis)
 * indexing edges: link the entity to one or more ``system`` entity

.. _FR__Context__Request:

Requesting
----------

There is two entry points for requesting the context:

 * a system, registered in the context hypergraph as a ``system`` entity
 * an entity

This allows to do complex queries like:

 * querying entities with a filter on data managed by the system
 * querying data on multiple systems with a filter on entities

We can define 4 types of query:

 * CREATE: create entities and/or data in one or more systems
 * READ: querying entities and/or data from on or more systems
 * UPDATE: update entities and/or data in one or more systems
 * DELETE: delete entities and/or data in one or more systems

Each query can possess one or more conditions:

 * time condition: will filter data according to the last modified time
 * entity condition: will filter data according to an entity filter
 * system condition: will filter entities according to a filter on system's data

For example (pseudo-code):

.. code-block:: python

    q = Query(type=CREATE)
    q += SystemCondition(unique_id == 'pbehavior')
    q += EntityCondition(unique_id == :entity_id)
    q.execute(pbehavior = :data)

    q = Query(type=UPDATE)
    q += SystemCondition(unique_id == 'pbehavior')
    q += EntityCondition(unique_id == :entity_id)
    q.execute(pbehavior = :data)

    q = Query(type=READ)
    q += TimeCondition(last_modified >= :timestamp)
    q += EntityCondition(name == 'foo')
    result = q.execute()
    # result.entities is a list containing all matching entities
    # result.systems is a dict containing key:data with:
    #  - key being the system's name
    #  - data being the related data

    q = Query(type=DELETE)
    q += TimeCondition(last_modified <= :timestamp)
    q.execute()

.. _FR__Context__WebService:

Context WebService
------------------

Requesting over HTTP
~~~~~~~~~~~~~~~~~~~~

Requesting the context via HTTP is done with ``POST`` verbs with a JSON formatted body:

.. code-block:: javascript

    POST /context/<request type>
    {
        "system": [...],
        "entity": [...],
        "time": [...],
        "data": {
            ...
        }
    }

The response is also formatted in JSON:

.. code-block:: javascript

    {
        "entities": [...],
        "systems": {
            ...
        }
    }

Filters
~~~~~~~

A filter is built as a dictionary where each keys correspond to a criteria and each
values is a dictionary containing the operators and conditions:

Example for a ``system`` filter:

.. code-block:: javascript

    {
        "unique_id": {"==": "pbehavior"}
    }

Example for an ``entity`` filter:

.. code-block:: javascript

    {
        "name": {"regex": "cpu-*"}
    }


Example for a ``time`` filter:

.. code-block:: javascript

    {
        "last_modified": {">=": ":timestamp"}
    }


The complete request
~~~~~~~~~~~~~~~~~~~~

Examples used for API translated to HTTP:

.. code-block:: javascript

    Request:
        POST /context/create
        {
            "system": [
                {
                    "unique_id": {"==": "pbehavior"}
                }
            ],
            "entity": [
                {
                    "unique_id": {"==": ":entity_id"}
                }
            ],
            "data": {
                "pbehavior": ...
            }
        }

    Response:

.. code-block:: javascript

    Request:
        POST /context/update
        {
            "system": [
                {
                    "unique_id": {"==": "pbehavior"}
                }
            ],
            "entity": [
                {
                    "unique_id": {"==": ":entity_id"}
                }
            ],
            "data": {
                "pbehavior": ...
            }
        }

    Response:

.. code-block:: javascript

    Request:
        POST /context/read
        {
            "entity": [
                {
                    "name": {"==": "foo"}
                }
            ],
            "time": [
                {
                    "last_modified": {">=": ":timestamp"}
                }
            ]
        }

    Response:
        {
            "entities": [
                {"name": "foo", ...}
            ]
        }

.. code-block:: javascript

    Request:
        POST /context/delete
        {
            "time": [
                {
                    "last_modified": {"<=": ":timestamp"}
                }
            ]
        }

    Response:

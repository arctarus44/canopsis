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
    * ``connector``: describing the class of connector used to produce data
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
    * ``datatype``: describing a type of data manipulated by one or more systems
    * ``datafield``: describing a data-type field (linked to the ``datatype`` entity with a composition edge)
    * ``datarole``: describing the role of a data-type field (used to render or edit the data field)
    * ...
 * a unique identifier

It is linked to other entities in a HyperGraph model where edges describe the
entity's composition.

Entities can be linked together with other edges, like:

 * correlation edges: determining the impact of one entity over others (useful for root cause/consequence analysis)
 * referring edges: link the entity to one or more entities (generally ``system`` entities, but not only)

.. _FR__Context__Request:

Requesting
----------

Performing a request is done by walking through the graph and querying systems:

 * walking through the graph, to understand the request:
    * the entry point of **every** request is the ``context`` system (registered in the
    context hypergraph)
    * the targeted system is extracted from the request
    * the involved systems are extracted from the request
    * conditions are applied on fields manipulated by systems (this is resolved using ``datafield`` entities)
 * querying systems:
    * we reduce the number of entities that will be requested from other systems:
        * this is done by applying conditions on the ``Context`` system first
        * then those entities are passed to involved systems and the conditions are used to filter once again
    * finally, we send the set of entities to the targeted system, in order to fetch data

This allows to do complex queries like:

 * querying entities with a filter on data managed by the system
 * querying data on multiple systems with a filter on entities

--------

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

    q = Query(type=CREATE, target=PBehaviorSystem)

    q += EntityCondition(unique_id == :entity_id)
    q += SystemCondition(involved=PBehaviorSystem)
    q.execute(:data)

    q = Query(type=UPDATE, target=PBehaviorSystem)
    q += EntityCondition(unique_id == :entity_id)
    q.execute(:data)

    q = Query(type=READ)
    q += TimeCondition(last_modified >= :timestamp)
    q += EntityCondition(name == 'foo')
    q += SystemCondition(unique_id == ''
    result = q.execute()

    q = Query(type=DELETE)
    q += TimeCondition(last_modified <= :timestamp)
    q.execute()


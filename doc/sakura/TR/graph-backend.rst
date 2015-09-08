.. _TR__Graph_backend:

=====
Graph
=====

Project ``canopsis.graph`` description.

.. contents::
   :depth: 2

----------
References
----------

- :ref:`FR::graph <FR__Graph>`

-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Jonathan Labéjof", "27/08/2015", "0.1", "Creation", ""
   "David Delassus", "01/09/2015", "0.2", "Rename document", ""
   "David Delassus", "01/09/2015", "0.3", "Update references", ""

--------
Contents
--------

canopsis.graph.elements
=======================

Module which contains all graph elements

.. _TR__Graph_backend__Element:

Graph Element
-------------

Base object for all other graph objects.

Contains:

- uid: str.
- types: str(s).
- info: dict.

.. _TR__Graph_backend__Vertice:

Vertice
-------

Inherits from the :ref:`Vertice <FR__Graph__vertice>`.

.. _TR__Graph_backend__Edge:

Edge
----

Inherits from the :ref:`Edge <FR__Graph__edge>`.

Contains:

- sources: str(s).
- targets: str(s).
- oriented: bool.

.. _TR__Graph_backend__Graph:

Graph
-----

Inherits from the :ref:`Graph <FR__Graph__graph>`.

Contains:

- elts: str(s)

canopsis.graph.manager
======================

.. _TR__Graph_backend__Manager:

GraphManager
------------

Manages graph storing and analyzing fonctions.

get_elts
>>>>>>>>

UTs
<<<

put_elt
>>>>>>>

UTs
<<<

put_elts
>>>>>>>>

UTs
<<<

remove_elts
>>>>>>>>>>>

UTs
<<<

del_edge_refs
>>>>>>>>>>>>>

UTs
<<<

update_elts
>>>>>>>>>>>

UTs
<<<

get_vertices
>>>>>>>>>>>>

UTs
<<<

get_edges
>>>>>>>>>

UTs
<<<

get_neighbourhood
>>>>>>>>>>>>>>>>>

UTs
<<<

get_sources
>>>>>>>>>>>

UTs
<<<

get_targets
>>>>>>>>>>>

UTs
<<<

get_orphans
>>>>>>>>>>>

UTs
<<<

get_graphs
>>>>>>>>>>

UTs
<<<

canopsis.graph.factory
======================

GraphFactory
------------

Instantiate a graph from a simple serialized format.

load
>>>>

UTs
<<<

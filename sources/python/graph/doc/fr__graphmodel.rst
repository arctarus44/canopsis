.. _FR__GraphModel:

====================
Canopsis Graph Model
====================

This document describes the requirements of the Canopsis graph model.

.. contents::
   :depth: 3

References
==========

List of referenced functional requirements:

Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "David Delassus", "2016/05/25", "0.1", "Document creation", ""

Contents
========

.. _FR__GraphModel__Desc:

Description
-----------

All data in Canopsis **MUST** be modeled into a graph (including the graph itself),
in order to make the user able to query them just by walking the graph.

.. _FR__GraphModel__Meta:

Meta model
----------

.. figure:: _static/images/graph/metamodel.png

.. _FR__GraphModel__POV:

Point of View
-------------

The *Complex Relationship* gives the ability to walk through the graph with multiple point of views.

For example:

 - we have 3 machines
 - the 3 machines provide a clustered service
 - on each of these machines, there is a process providing a cluster node

.. figure:: _static/images/graph/pov.png

In this example we have:

 - a virtual node representing the clustered service
 - 3 nodes representing the physical machines
 - 3 complex relationships (in blue) where the inner node describes the cluster node (the process)
 - those relationships link together the clustered service to the physical machines

We can identify two possible point of view:

 - we are interested about the machines providing the clustered service
 - we are interested about what processes are running on a physical machine

.. _FR__GraphMode__Walk:

Walking through the graph
-------------------------


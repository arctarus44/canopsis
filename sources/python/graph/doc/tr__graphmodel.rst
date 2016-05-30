.. _TR__GraphModel:

====================
Canopsis Graph Model
====================

This document describes the technical requirements of the Canopsis graph model.

.. contents::
   :depth: 2

References
==========

List of referenced functional requirements:

 - :ref:`FR::Graph Model <FR__GraphModel>`

Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "David Delassus", "2016/05/30", "0.1", "Document creation", ""

Contents
========

.. _TR__GraphModel__Meta:

Meta model
----------

The storage API **MUST** provice *CRUD* access to:

 - graph elements:
    - included elements **SHOULD** be returned upon a **R** ead
 - relationship elements:
    - source and target elements **SHOULD** be returned upon a **R** ead
 - complex relationship elements:
    - source, target and content elements **SHOULD** be returned upon a **R** ead
 - node elements:
    - from and to elements **SHOULD** be returned upon a **R** ead

If the API respects the **RESTful** architectural constraints, then reads can return
hypertext links to elements instead of elements themselves.

Each element **MUST** typed via a ``type`` field.

.. _TR__GraphModel__Request:

Requesting data
---------------

**C** reate operations are simple push into the storage.

**R** ead, **U** pdate and **D** elete operations are performed by walking the graph.

Those operations are selecting relationships and/or nodes for:

 - reading: elements **MUST** be returned after the walk through
 - modifying: elements **MUST** be modified during the walk through, and **SHOULD** be returned
 - deletion: elements **MUST** be deleted after the walk through

.. _TR__GraphModel__Constraints:

Constraints module
------------------

Each call to the storage API **MUST** have *before* and *after* hooks, allowing
the implementation of constraints able to act on each call.

The constraints **SHOULD** be stored in a key/value storage with:

 - the ``filter`` field being a *MongoDB* filter
 - the ``rule`` field pointing to a *Python* function with the following prototype:
    - the element as argument
    - returning ``True`` or ``False`` whether the constraint is respected or not

.. _FR__Context:

===========================
Canopsis Executable Context
===========================

This document describes the requirements of the Canopsis executable context.

.. contents::
   :depth: 3

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

.. _FR__Context__Desc:

Description
-----------

.. _FR__Context__Desc__Context:

Context
~~~~~~~

Every data in Canopsis is associated to an entity:

 - events provide data about component, resource and metric
 - the user interface provide data about user, view and widget
 - there is data about configuration resource and configurable feature
 - ...

Entities are linked together:

 - a resource belongs to a component
 - a metric is produced by a component or resource
 - a widget belongs to a view
 - a user can create, access, edit or delete a view
 - a configuration resource belongs to a configurable feature
 - a configurable feature produces a component
 - ...

In order to model those entities, we use the :ref:`graph meta model <FR__Context__Meta>`.

.. _FR__Context__Desc__Executable:

Executable
~~~~~~~~~~

Because features are modeled into the graph, when walking through it in order to
fetch data, we can identify which code shall be executed.

.. _FR__Context__DSL:

Domain Specific Language
------------------------

A DSL **MUST** be written in order to generate a query to the graph model.

.. _FR__Context__Simulation:

Simulation and impact analysis
------------------------------

By walking through the graph, we are able to:

 - identify which code is susceptible to have an impact on the entity
 - identify what is the impact of an entity on the rest of the system
 - simulates what could happen if an entity were deleted
 - simulates what could happen if some code where deleted

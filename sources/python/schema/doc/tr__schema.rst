.. _TR__Schema:

========
Schema
========

Project ``canopsis.schema`` description.

.. contents::
   :depth: 3

----------
References
----------

- :ref:` tr__schema <tr__Schema>`

-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Julie Vanglabeke", "17/05/2016", "0.1", "schema project", ""

--------
Contents
--------

core
====

.. _TR__Schema_core:

In core is write an abstract class, "Schema", which is used by lang programmes. This function defines the load and the validate methodes.


lang
====

.. _TR__Schema_lang:

Sub-folder which contains load and validate function write for specifique language.
Those files inherit of Schema class in core.


patch
=====

.. _TR__Shema_lang:



transformation
==============

.. _TR__Schema_transformation:

Describes transformations to apply on data. 
.. _TR__Schema:

========
Schema
========

Project ``canopsis.schema`` description.

.. contents::
   :depth: 2

----------
References
----------

- :ref:` tr__schema <tr__Schema>`

-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Julie Vanglabeke", "17/05/2016", "0.1", "creation", ""

--------
Contents
--------

core
====

.. _TR__Schema_core:

In core is define an abstract class, Schema, which is used by lang programmes. This function define the load and the validate methodes.


lang
====

.. _TR__Schema_lang:

sub-folder which contains load and validate funtion write for specifique language.
those files inherit of Schema class in core.


transformation
==============

.. _TR__Schema_transformation:

Describes transformations to apply on data spécified in input schema. Transformation is write in specifique language, it refer to lang file.
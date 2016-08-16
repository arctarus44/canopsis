.. _FR__Schema:

===============
Canopsis Schema
===============

This document describes the solution to the interoperability problem

.. contents::
   :depth: 4

----------
References
----------

 - :ref:`FR::Storage <FR__Storage>`

-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "David Delassus", "2015/10/06", "0.1", "Document creation", ""
   "Gwenael Pluchon", "2015/11/02", "0.2", "Add meta-schema", ""
   "Gwenael Pluchon", "2015/11/02", "0.3", "remove meta-schema", ""
   "Julie Vaglabeke", "2016/08/08", "0.4", "adaptation to migration module"

-------
Content
-------

Objective
=========

Canopsis is a Hypervision solution, it is based on the schema notion to define the structure of data and their treatment.
After taken schema to Canopsis, the tool will generate code to warranty maximum reliability and it maintain.

With the evolution of the system problematic, we bring many features based on schema, data migration is an important part of it.


Description
===========

A schema is used to describe:

 - data: how data is structured, in order to generate models for it
 - transformation: how data can be turned into another data
 - components: how Canopsis components interact with data (chaining, ...)

.. _FR__Data_Schema:

Data Schema
-----------

This schema **MUST** describe the structure of data:

 - what fields are provided
 - how to interpret those fields (string, timestamp, ...)


.. _FR__Schema_Transformation_Schema:

Transformation Schema
---------------------

This schema **MUST** contain a reference to:

 - the input :ref:`data schema <FR__Data_Schema>`
 - the output :ref:`data schema <FR__Data_Schema>`

And it **MUST** contain a mapping of:

 - fields used in output, from input
 - transformation operator to apply on fields (concatenate, split, integer to string, ...)

.. _FR__Schema_Component:

Component Schema
----------------

TODO
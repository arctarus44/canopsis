.. _FR_Schema:

===============
Canopsis Schema
===============

This document describes the solution to the interopérability problem

.. contents::
   :depth: 4

----------
References
----------

- :ref:` fr__schema <fr__Schema>`

-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Julie Vanglabeke", "29/04/2016", "0.1", "schema projet", ""

-------
Content
-------

Objective
=========

Canopsis is a Hypervision solution, it is based on the schema notion to define the structure of data and their treatment. 
After taken schema to Canopsis, the tool will generate code to warranty maximum reliability and it maintain.

With the evolution of the system problematic, we bring many feature based on schema, datas migration is an importante part.


Description
===========

.. _FR__Schema__Description:

A schema is a document in Json or XML or anyother language which describe the sctructure of data.
The structure of the data must respect what it describe in the schema to be validated.

A schema is used to describe:

 - data: how data is structured, in order to generate models for it
 - transformations: how data can be turned into another data

the following picture is a class diagram.

.. image:: ../_static/images/schema/Diagramme.png


The JsonSchema class inherit of Schema class


Schema
------

.. _FR__Schema:

abstract class which introduce validate, load, get_item, set_item, del_item, and save methodes.
Base of the different schema classes


JsonSchema
----------

.. _FR__Schema__JsonSchema:

specific class for JSON language
translate Schema methodes for Json.


Transformation
--------------

.. _FR__Schema__Transformation:

take a schema in parameter which inherit of Schema class.
implement get_input, get_output, get_patch, get_filter, select_data, apply_patch and save methodes to transform data.


JsonTransformation
------------------

.. _FR__Schema__JsonTransformation:

specific class for JSON language
translate Transformation methodes for Json.
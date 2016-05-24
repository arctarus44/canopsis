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

   "Julie Vanglabeke", "29/04/2016", "0.1", "Document creation", ""

-------
Content
-------

Objective
=========

Canopsis is a Hypervision solution, it is based on the schema notion to define the structure of data and their treatment. 
After taken schema to Canopsis, the tool will generate code to warranty maximum reliability and it maintain.

With the evolution of the system problematic, we bring many feature based on schema, data migration is an important part of it.
 
  
Description
===========

.. _FR__Schema__Description:

A **schema** is a document in Json or XML or anyother language.

It is used to describe:

 - data: how data is structured, in order to generate models for it
 - transformations: how data can be turned into another data

The following picture is a class diagram to illustrate the running of different classes of this project.

.. image:: ../_static/images/schema/Diagramme.png
 
   
Schema
------

.. _FR__Schema:

*Abstract class* which introduce *validate, load, __getitem__, __setitem__, __delitem__, getressource and save* methodes.
Base of the different schema classes.
This class ease schema **CRUD** operations.


JsonSchema
----------

.. _FR__Schema__JsonSchema:

Specific class for *JSON* language.
Translate Schema methodes for Json.
This class inherit of **Schema**.


Transformation
--------------

.. _FR__Schema__Transformation:

Take a schema in parameter which inherit of **Schema**.
Implement *input, output, patch, filtre, select_data, apply_patch and save* methodes to transform data.


Patch
-----

.. _FR__Schema__Patch:

Take a patch in parameter which inherit of **Schema**.

Define a decorator (recordpatch) to get the correct type of the patch in *Transformation*, it can be used as a function too.
Get type *patch* and implement the process method which describe how apply patch according on is type (JSON, UML, xslt, ...)


JsonPatch
---------

.. _FR__Schema__JsonPatch:

Specific class for *JSON* language.
Translate Patch methodes for Json.
This class inherit of **Patch**.
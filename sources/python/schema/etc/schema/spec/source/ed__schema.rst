.. _ED_Schema:

===============
Canopsis Schema
===============

This document describes the solution to the intercompatibility problem

.. contents::
   :depth: 4


----------
References
----------

- :ref:` ed__schema <ed__Schema>`


-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Julie Vanglabeke", "29/04/2016", "0.1", "schema projet", ""


-------
Content
-------

core
====

.. _TR__Schema_core:

class Schema is an abstract class which describes :
 - load : describes in "__init__" function, this methode load a data from a path. The path is refered in schema_conf file
 - validate : valid a data with a structural schema


lang
====

.. _TR__Schema_lang:

contains files which describes how translate the programme in different languages

 - json : class JsonSchema which inherit of Schema in core and contains load and validate methode for json language

transformation
==============

.. _TR__Schema_transformation:

class transformation inherit of JsonSchema.
this class define all methodes to transm json data


get_patch : 
 - extract operations to apply on data from the patch and stock them in a list


get_input :
 - extract input informations from input document to locate data


get_output : 
 - get output informations from output document to know where save new data


get_filter : 
 - extract filter to select loaded data


transfromation :

 - apply patch on filtered data
 - if sup_data = true, new data will be created and old data will be deleted
   if sup = false, old data will keep
.. _ED__Migration:

=========
Migration
=========

This document describes how use the solution to the interopérability problem

.. contents::
   :depth: 3

----------
References
----------

 - :ref:`FR::Schema <FR__Schema>`
 - :ref:`FR::Schema <FR__Data_Schema>`
 - :ref:`FR::Schema <FR__Schema_Transformation_Schema>`


-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Julie Vanglabeke", "30/06/2016", "0.1", "Document creation", ""
   "Julie Vanglabeke", "09/08/2016", "0.2", "Document update", ""


--------
Contents
--------


 .. _ED__Migration__Installation:

Installation
------------

The migration can be use in canopsis.
To use the migration you **SHOULD** launch a script which describes different operations.


 .. _ED__Migration__Use:

Use
---

The migration is describes in the migrate function.
You can call it or launch it with a script wich will describe your preferences.
In the script you can call migrate() and the edition module to write your own transformation patch.


 .. _ED__Migration__Requirement:

Requirement
-----------

You **MUST** write 3 documents before launch the migration :

 - :ref:`FR::Schema <FR__Data_Schema>` to validate the selected data
 - :ref:`FR::Schema <FR__Data_Schema>` to validate the structure of the migrated data
 - transformation document which will be validate by the :ref:`FR::Schema <FR__Schema_Transformation_Schema>`,
 it describes the operations for the migration.

You **MUST** launch the migration with the migrate function.
This function have the path to the transformation document in parameter.


 .. _ED__Migration__JSON:

JSON
----

In the transformation document you **MUST** write :

 - **input** : URI to the data to migrate (ex: file uri)
 - **output** : URI to the migrated data folder (ex: file uri)
 - **filter** : mongodb query to select data in the storage
 - **inplace** : boolean to precise if you want to replace the initial data by the migrated data
 - **path_V1** : path to the validation schema of the first data version
 - **path_V2** : path to the validation schema of the second data version
 - **schema_class** : the good  type class(JsonSchema, XML, ...)


construction of URI
-------------------

for migration tool, URI are on standard format
URL = protocol(*://)domain name(*.*.com)path(/...)"""

You can create your own protocol
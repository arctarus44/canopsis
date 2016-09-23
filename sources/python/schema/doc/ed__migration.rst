.. _ED__Migration:

=========
Migration
=========

This document describes how to use the solution to the interoperability problem

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

The migration can be used in canopsis and without it.
To use the migration you **COULD** launch a script which describes different operations or call the migrate() function.
This function take the path to the transformation document in parameter.


 .. _ED__Migration__Use:

Use
---

The migration is describes in the migrate function.
You can call it or launch it with a script wich will describe your preferences.
In the script you can call migrate().


 .. _ED__Migration__Requirement:

Requirement
-----------

You **MUST** write 3 documents before launching the migration :

 - :ref:`FR::Schema <FR__Data_Schema>` to validate the selected data
 - :ref:`FR::Schema <FR__Data_Schema>` to validate the structure of the migrated data
 - transformation document which will be validated by the :ref:`FR::Schema <FR__Schema_Transformation_Schema>`,
 it describes the operations for the migration.

You **MUST** launch the migration with the migrate function.
This function have the path to the transformation document in parameter.


 .. _ED__Migration__JSON:

JSON
----

In the transformation document you **MUST** write :

 - **input** : URI to the data to migrate (ex: file uri)
 - **output** : URI to the migrated data folder (ex: file uri)
 - **path_V1** : path to the validation schema of the first data version
 - **path_V2** : path to the validation schema of the second data version
 - **schema_class** : the good  type class(JsonSchema, XML, ...)
 - **patch** : the patch **MUST** contain operation to apply on data to transform them


construction of URI
-------------------

for migration tool, URI are on standard format
URL = protocol(*://)domain name(*.*.com)path(/...)"""


 .. _ED__Migration__How_To:

How To
------

To migrate your data you **MUST** import the library and use the migrate function as following

.. code-block:: python

	from migration import core

	path_transfo = '/home/user/myfolder/data_migration/etc/schema/my_transformation_document.json'

	core.migrate(path_transfo)
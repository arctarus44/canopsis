.. _ED__Migration:

=========
Migration
=========

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


--------
Contents
--------


 .. _ED__Migration__Location:

Location
--------

All libraries are in canopsis.
You **MUST** be in the canopsis environnement and start it to launch the script.


 .. _ED__Migration__Installation:

Installation
------------

The migration can be use in canopsis.
To use the migration you **MUST** write a script to describe different operations.
Run canopsis and mongodb, open the folder where you have save the migration script.
To launch the script execute the following command line : 'python script_name.py'.


 .. _ED__Migration__Use:

Use
---

You can use the migration to change your data version or to move data from a storage to another
with a simple script.

 .. _ED__Migration__Requirement:

Requirement
-----------

You **MUST** write 3 documents before launch the migration script :

 - :ref:`FR::Schema <FR__Data_Schema>` to validate the selected data
 - :ref:`FR::Schema <FR__Data_Schema>` to validate the structure of the migrated data
 - transformation document which will be validate by the :ref:`FR::Schema <FR__Schema_Transformation_Schema>`,
 it describe the operations for the migration.

In the transformation document you **MUST** write :

 - input : path to the data to migrate
 - output : path to the migrated data folder
 - filter : mongodb query to select data in the storage
 - inplace : boolean to precise if you want to replace the initial data by the migrated data


 .. _ED__Migration__Errors:

Errors
------

If you have a storage error see the help.
You **MUST** attribute a name to your data to precise it in the output path.
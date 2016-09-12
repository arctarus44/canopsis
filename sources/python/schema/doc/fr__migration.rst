.. _FR__Migration:

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

   "Julie Vanglabeke", "25/05/2016", "0.1", "Document creation", ""

--------
Contents
--------


 .. _FR__Migration__Description:

Description
-----------

Migration is specific type of data transformation.
The migration turn all data from a source into new data to use them with another system.


 .. _FR__Migration__Process:

Process
-------

To proceed we use a :ref:`FR::Schema <FR__Schema_Transformation_Schema>` to transform data from a :ref:`FR::Storage <FR__Storage>` to another.

The :ref:`FR::Schema <FR__Data_Schema>` will validate data to migrate and API will apply transformation to pass data from a version to another.


.. _FR__Migration__Data__Upgrading:

Data Upgrading
--------------

You can transfert data from a :ref:`FR::Storage <FR__Storage>` to itself to upgraded them or to replace older version by the new version of the same data.


.. _FR__Migration__Data__Upgrading:

Moving data
-----------

You can move your data from a system to another
ex: data from github to gitlab, data from gmail to canopsis, ...
To do this move just write input/output, schemaclass, schema v1, schema v2.
You don't need to write the patch for a simple moving.

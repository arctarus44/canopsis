.. _TR__Schema:

======
Schema
======

Project ``canopsis.schema``

.. contents::
   :depth: 3

----------
References
----------

 - :ref:`FR::Schema <FR__Schema>`

-------
Updates
-------

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "Julie Vanglabeke", "24/05/2016", "0.1", "Document creation", ""

--------
Contents
--------

.. _TR__Schema_Description:

Description
===========

This feature **MUST** have a configuration file.

The configuration file providing:

 - where are stored the schema (ex: storage URI)

Schema **MUST** have a unique identifier.

The different classes of the project interact as the following diagram:

.. image:: /canopsis/sources/python/schema/doc/_static/Diagramme1.png


.. _TR__Schema_Schema_loading:

Schema loading
==============

To load schema API looks into the configuration file and return a schema.
It identify schema by their unique id (ex: name, key, ...).
Raise an error if non existing document.


.. _TR__Schema_Dictionary_Schema:

Dictionary Schema
=================

Schema **SHOULD** be used like a dictionary, it depends on Schema loading.

It possible to use dictionary methodes on it:

 - get an item from the loaded schema
 - set a value in the item
 - delete an item
 - save modifications effected on dictionary

It **MUST** raise an error if schema is not a dictionary.


.. _TR__Schema_Schema_Validation:

Schema Validation
=================

A methode to validate data **MUST**:

 - do nothing if data is valid
 - raise a ValidationError if data is invalid
 - raise a SchemaError if the schema itself is invalid

This function validate the structure of data by a schema but not his contain.


.. _TR__Schema_Transformation:

Transformation
==============

The transformation schema **MUST** provide:

 - input field to know where are stored data (ex: storage URI)
 - output field to know where will be stored new data (ex: storage URI)
 - a filter field to tell what are the selected data to the API
 - inplace : an option to remove old data after transformation or not
 - The data schema identifier for selected data
 - The data schema identifier for transform data


filter
------

Filter is used to choose data to transform.
Raise an error if filter is invalid or if data does not exist.


inplace
-------

 - set to True if you want to remove old data after transformation
 - set to False otherwise

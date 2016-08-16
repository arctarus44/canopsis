.. _TR__edition_patch:

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

   "Julie Vanglabeke", "09/08/2016", "0.1", "Document creation", ""

--------
Contents
--------

.. _TR__edition_patch_Description:

Description
===========

This module is used to edit a transformation patch in JSON format.


.. _TR__edition_patch_Function:

Function
========

You can use differnt function to write your own transformation patch.

 - **Add** : write the add operation into the transformation patch, take the path to the transformation document, the path field, value field and new field in parameter.
 - **Copy** : write the add operation into the transformation patch, take the path to the transformation document, the path field, fr field and new field in parameter.
 - **Remove** : write the add operation into the transformation patch, take the path to the transformation document, the path field and new field in parameter.
 - **Move** : write the add operation into the transformation patch, take the path to the transformation document, the path field, fr field and new field in parameter.
 - **Replace** : write the add operation into the transformation patch, take the path to the transformation document, the path field, value field and new field in parameter.


Parameters
----------

 - **path_transfo** : path to the transformation document
 - **path** : indicate the name of the concerned field (ex: '/property_name/new_field_name')
 - **fr** : indicate the initial point of the move or copy function (ex: '/property_name/new_field_name')
 - **value** : set the new field to the value you want
 - **new** : default: name of the function (ex: 'add')

You **SHOULD** ommit the 'new' parameter but all other are necessary to write the patch correctly

.. _TR__edition_patch_How_to_use:


How to use
==========

You **MUST** import the edit module
Call the different function with the correct parameters to write your transformation patch

exemple of use
--------------

edit.add(path_transfo, path, value)
.. _ED__Edition:

=======
Edition
=======

This document describes how to use the edition_patch module to write transformation patches with simple command lines.

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

   "Julie Vanglabeke", "08/09/2016", "0.1", "Document creation", ""


--------
Contents
--------


 .. _ED__Edition__Use:

Use
---

To use this module :
 - load the module and its functions (from schema.edit import add, move, remove, replace, copy)
 - call the function with correct parameters

You **SHOULD** write a script to join different operations and write the transformation patch in only one time.


 .. _ED__Edition__Add:

Add
---

Function to add a field in the transformation patch

Parameters :
 - path_transfo : path to the transformation document
 - path : /property_name/field_name_to_create
 - value : value to set the field to create
 - new : default = 'function name', use it to write several operations 'add'


 .. _ED__Edition__Copy:

Copy
----

Function to copy a field in the transformation patch

Parameters :
 - path_transfo : path to the transformation document
 - fr : /property_name/field_name_to_copy
 - path : /property_name/field_name_where_copy
 - new : default = 'function name', use it to write several operations 'copy'


 .. _ED__Edition__Remove:

Remove
------

Function to remove a field in the transformation patch

Parameters :
 - path_transfo : path to the transformation document
 - path : "to" /property_name/field_name_to_delete
 - new : default = 'function name', use it to write several operations 'remove'


 .. _ED__Edition__Move:

Move
----

Function to remove a field in the transformation patch

Parameters :
 - path_transfo : path to the transformation document
 - fr : /property_name/field_name_to_move
 - path : /property_name/field_name_where_move
 - new : default = 'function name', use it to write several operations 'move'


 .. _ED__Edition__Replace:

Replace
-------

Function to replace a field by another in the transformation patch

Parameters :
 - path_transfo : path to the transformation document
 - path : /property_name/field_name_to_replace
 - value : value to set the field to replace
 - new : default = 'function name', use it to write several operations 'replace'


 .. _ED__Edition__Add_query:

Add query
---------

Function to add a field in the transformation patch

Parameters :
 - path_transfo : path to the transformation document
 - query : value of the requeste


  .. _ED__Edition__Add_entry:

Add entry
---------

Function to add a field in the transformation patch

Parameters :
 - path_transfo : path to the transformation document
 - type : precise if you want to write input, output, path, ...
 - value : value to set the field to create


 .. _ED__Edition__How_To:

How To
------

Before write into your transformation document, you **MUST** create it

To write add patch operation:
add('/home/myfolder/mydocument.json', '/field-to-add', 'myvalue', add)

To write copy patch operation:
copy('/home/myfolder/mydocument.json', '/field-from_copy', '/field-to-copy', copy)

To write move patch operation:
add('/home/myfolder/mydocument.json', '/field-to-remove', remove)

To write remove patch operation:
add('/home/myfolder/mydocument.json', '/field-from-move', '/field-to-move', move)

To write replace patch operation:
add('/home/myfolder/mydocument.json', '/field', 'myvalue', replace)
this command replace the value of the field in parameter

To add a query:
add_query('/home/myfolder/mydocument.json', 'query-value')

To add a field:
add_entry('/home/myfolder/mydocument.json', 'field_name', 'field_value')
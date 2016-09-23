.. _ED__Edition:

=======
Edition
=======

This document describes how to use the schema_generation library to generate schema from your data automatically.

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

   "Julie Vanglabeke", "20/09/2016", "0.1", "Document creation", ""


--------
Contents
--------


 .. _ED__Edition__Use:

Use
---

To use this module :
 - load the module and his functions (from data_migration.schema_generation import generateSchemaJson)
 - call the function with correct parameters


 .. _ED__schema_generation_generateSchemaJson:

generateSchemaJson
------------------

This function generate a json schema from data.

parameters:
 - title : title of the output schema
 - data : data to generate the schema, **MAY** be the path to you data

You **MUST** call the function with all parameters.

quick exemple :
output = generateSchemaJson(title, data)

You **COULD** serialized 'output' to use the new generated schema.


 .. _ED__schema_generation_How_to:

How To
------

to use this library proceed as following:

.. code-block:: python

	import schema_generation
	import json

	schema = schema_generation.generateSchemaJson('data2', {"patch":[{
            "path": "/test",
            "value": "TT",
            "op": "add"
        }]})

	path = '/home/julie/Documents/dm/etc/schema/new_generate.json'

	#this line serialize the new document in json format file
	with open(path, "w") as f:
    	json.dump(schema, f, indent=4)


	#The new_generate file is:

	{
	    "$schema": "http://json-schema.org/draft-04/schema#",
	    "type": "object",
	    "properties": {
	        "patch": {
	            "items": {
	                "type": "object",
	                "properties": {
	                    "path": {
	                        "type": "string"
	                    },
	                    "value": {
	                        "type": "string"
	                    },
	                    "op": {
	                        "type": "string"
	                    }
	                }
	            },
	            "type": "array"
	        }
	    },
	    "title": "data2"
	}
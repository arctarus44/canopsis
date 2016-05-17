.. _FR_Schema:

===============
Canopsis Schema
===============

This document describes the solution to the intercompatibility problem

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

   "Julie Vanglabeke", "29/04/2016", "0.1", "schema projet", ""

-------
Content
-------


Context
=======

This project is based on one problem:
    incompatibility of programmation languages

Many languages mean:
 - adaptability difficulties
 - reserved to "aficionados" of developpement
 - for bigger project, a software configuration training is needed for the staff

In addition, an IT staff is needed to be in touch with the customer to maintain the project and his adaptation.


Objective
=========

Canopsis is a Hypervision/Supervision tool, it is based on the schema notion to define the structure and data treatment. 
After taken schema to Canopsis, the tool will generate code to warranty maximum reliability and maintain of the tool easely.

With the evolution of the system problematic, we bring many feature based on schema, datas migration is an importante part.


Description
===========

.. _FR__Schema__Description:

A schema is a document in Json or XML or anyother language which describe the sctructure of an other document or a data.
The structure of the data/document must respect what it describe in the schema to be validated.

A schema is used to describe:

 - data: how data is structured, in order to generate models for it
 - transformations: how data can be turned into another data

the following picture describe how schemas interact to migrate data in new data. 

.. image:: ../_static/images/schema/Diagramme.png

All schema in Canopsis inherit of Schema_Base
Patch is created with Schema_patch, is apply on data.
The association of Patch and Data create New Data

1 Patch can be apply on many Data and many Patch or Data are validate by Schema_Transformation and Schema_Data.


Data Schema
-----------

.. _FR__Schema__Data:

The data schema describes how must be the structure of the data:

 - what fields are provided
 - how to interpret those fields (string, timestamp, ...)


Transformation Schema
---------------------

.. _FR__Schema__Transform:

This schema contain a reference to:

 - the input_schema : reference path to data and the schema which describe it, a 
 - the patch_schema : describe operation(s) which will be apply on data to transform it
 - the output_schema : reference path to the output folder
 - the filter_schema : describe the filter for choose the data to transform it
.. _FR__Schema:

===============
Canopsis Schema
===============

This document describes the concept of schema in Canopsis.

.. contents::
   :depth: 2

References
==========

Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "David Delassus", "2015/10/06", "0.1", "Document creation", ""

Contents
========

Description
-----------

A schema is used to describe:

 - data: how data is structured, in order to generate models for it
 - transformation: how data can be turned into another data
 - components: how Canopsis components interact (chaining, ...)

.. _FR__Schema__Data:

Data Schema
-----------

This schema **MUST** describe the structure of data:

 - what fields are provided
 - how to interpret those fields (string, timestamp, ...)

.. _FR__Schema__Transform:

Transformation Schema
---------------------

This schema **MUST** contain a reference to:

 - the source :ref:`data schema <FR__Schema__Data>`
 - the output :ref:`data schema <FR__Schema__Data>`

And it **MUST** contain a mapping of:

 - fields used in output, from source
 - transformation operator to apply on fields (concatenate, split, integer to string, ...)

.. _FR__Schema__Component:

Component Schema
----------------

This schema describe the configuration of Canopsis components, for example:

 - what storage to use
 - what other components to chain data to
 - ...

.. _FR__DSL:

===
DSL
===

This document describes the DSL requirements of Canopsis.

.. contents::
   :depth: 3

References
==========

List of referenced functional requirements:

 - :ref:`FR::Context <FR__Context>`

Updates
=======

.. csv-table::
   :header: "Author(s)", "Date", "Version", "Summary", "Accepted by"

   "David Delassus", "2016/02/22", "0.1", "Document creation", ""

Contents
========

.. _FR__DSL__Desc:

Description
-----------

Based on **SQL**, the Canopsis DSL allows performing complex request on the
:ref:`context <FR__Context__Desc>` and its systems.

.. _FR__DSL__Grammar:

DSL Grammar
-----------

.. code-block:: text

   <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
   <letter> ::=  "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
       | "c" | "d" | "e" | "f" | "g" | "h" | "i"
       | "j" | "k" | "l" | "m" | "n" | "o" | "p"
       | "q" | "r" | "s" | "t" | "u" | "v" | "w"
       | "x" | "y" | "z" ;

   <identifier> ::= <letter> { <letter> | <digit> | "_" } ;

   <request> ::= <request-type> <request-target> <request-conditions> ;

   <request-type> ::= "SELECT" <aggregation> "FROM" | "INSERT INTO" | "UPDATE" | "DELETE FROM" ;

   <aggregation> ::= "*" | <function> "(" <aggregation> ")" ;
   <function> ::= "COUNT" | "MAX" | "MIN" | "AVERAGE" | "SUM" ;

   <request-target> ::= <target> { <opt-request-target> } ;
   <opt-request-target> ::= "," <request-target> ;
   <target> ::= <identifier> ;

   <request-conditions> ::= "WHERE" <request-condition> ;
   <request-condition> ::= <request-field> <comparison> <value> { <opt-request-condition> } ;
   <opt-request-condition> ::= "AND" <request-condition> | "OR" <request-condition> ;

   <request-field> ::= <request-system> "." <system-field> | <system-field> ;
   <request-system> ::= <identifier> ;
   <system-field> ::= <identifier> ;

   <comparison> ::= "<" | "<=" | "=" | "!=" | ">=" | ">" | "LIKE" ;
   <value> ::= <digit> { <digit> } | "'" { <letter> | <digit> } "'" | <typed-value> ;
   <typed-value> ::= <value-time> | <value-timestamp> ;

   <value-time> ::= "TIME" "'" <digit> { <digit> } ":" <digit> { <digit> } ":" <digit> { <digit> } "'" ;
   <value-timestamp> ::= "TIMESTAMP" "'" <digit> { <digit> } ":" <digit> { <digit> } ":" <digit> { <digit> } "'" ;

.. _FR__DSL__Request:

Requesting
----------

.. _FR__DSL__Request__Read:

Reading
-------

.. code-block:: text

   SELECT <aggregation>
   FROM <targets>
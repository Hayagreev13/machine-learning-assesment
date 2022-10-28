# Testing the solution

A total of 31 tests have been conducted to check the behaviour of the model developed and to get a sense of accuracy for the classfied labels: PER, LOC, ORG, MISC, DATE. The python module unittest has not been used due to its limited functionality. All tests have been aimed to invoke certain functions relating to particular labels to check their functionality.

The tests have been categorized into 5 categories namely:

## General tests

General tests are conducted to check the functionality of utility fucntions and general cases not realting to the classified labels.
These include the folowing cases:

* Artist not present in database
* Same artist with different spelling
* Same name meaning multiple things
* Same first name, different last name for artists
* Ensure update_db function works properly
* Ensure clean_sentence function works properly

## PER tests

PER tests are conducted to understand probability of an entity with label PER being classified properly.
These include the folowing cases:

* Persons present in database with method=='present'.
* Persons present in database with method=='distance'.
* Presons not present in database.
* Persons with high confidence scores.
* When persons are unclassified.

## LOC tests

LOC tests are conducted to understand probability of an entity with label LOC being classified properly.
These include the folowing cases:

* Behaviour when `word_to_event_title` ratio is high.
* Confidence score is high.
* Entity's name resembles an artist but is actually a location.
* Is an artist with a location as thier name.
* Location present in database with method=='distance'.
* When locations are unclassified.

## ORG tests

ORG tests are conducted to understand probability of an entity with label ORG being classified properly.
These include the folowing cases:

* Organisations present in database with method=='present'.
* Organisations present in database with method=='distance'.
* Organisations not present in database.
* Behaviour when `word_to_event_title` ratio is high.
* When organisations are unclassified.

## MISC tests

MISC tests are conducted to understand probability of an entity with label MISC being classified properly.
These include the folowing cases:

* Misc present in database with method=='present'.
* Misc present in database with method=='distance'.
* When misc is classified as `event_info`.
* Behaviour when `word_to_event_title` ratio is high but new entities have been found.
* Behaviour when `word_to_event_title` ratio is high and new entities have been found.
* When confidence score is high.
* When misc are unclassified.

## DATE tests

DATE tests are conducted to understand probability of an entity with label DATE being classified properly.
These include the folowing cases:

* Whether dates and time are getting classified.
* Whether months are getting classified.

## Scoring System

A scoring system has been devised to measure the performance of the algorithm. It is as follows,

* 0 - no entity recognition or weird entity recognition (taking parts of words as an entity)
* 0.5 - entity recognition and wrong classification
* 1 - entity recognition and correct classification

In the end for a given `event_title`, the score is given as (sum of scores received by the entities)/(total number of entities present).
Each of the test cases has 5 event titles. The cummulative sum of all the fractions for a test category is taken as its accuracy.

The scores for `update_db` and `clean_sentence` are either 0 for not expected output and 0.5 for expected output to avoid bias to the whole calculation.
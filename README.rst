Final Project for CS 5260
==========================================

Overview
--------

This repository is for the final project for CS 5260. More info to come.

Usage
------------

The easiest way to run the program is from the cs5260 directory run:

``python3 country_scheduler.py``

NOTE: Currently to change settings for the search, manually change the following line in country_scheduler.py:

country_scheduler("Atlantis", "Inputs/resources.csv", "Inputs/states.csv", "outputs/output.txt", 1, 3, 10)


Info
------------
country_scheduler.py - This file calls country_scheduler which builds the initial environment and calls the search.

scheduler.py - This file does the search and contains all Expected Utility functions.

read_files.py - This file has code from John Ford for reading in and parsing files.

Node.py - Modified from the sample code to handle this stuff.

PriorityQueue.py - Modified form the sample code to handle this stuff.

Inputs\ - This folder contains the input files.

Archive\ - This folder contains archived versions of input files


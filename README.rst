Final Project for CS 5260
==========================================

Overview
--------
git repository:
https://github.com/bdg221/CS5260

This repository is for the final project for CS 5260. The files are all stored inside of the CS5260 directory.

country_scheduler.py - This is the main file used for running the search. When called this file calls the country_scheduler method which in turn runs the search, saves the output files, and saves images of the plots.

scheduler.py - This is the main search file. It also contains all expected utility related functions.

PriorityQueue.py - This is the priority queue code from the sample provided.

Node.py - This is the node code from the sample provided, but updated to include state, schedule, and eu.

read_files.py - This is a utiltity file with code from John Ford for reading and parsing the information from csv files.

Inputs\ - This folder contains the input files.

Archive\ - This folder contains archived versions of input files


Usage
------------

The easiest way to run the program is from the cs5260 directory run:

``python3 country_scheduler.py``

NOTE: Currently to change settings for the search, manually change the following line in country_scheduler.py:

country_scheduler("Atlantis", "Inputs/resources.csv", "Inputs/states.csv", "outputs/output.txt", 5, 5, 10000)
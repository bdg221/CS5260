#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from .DataTypes import Action, Heuristic, State, Node
from .ProblemFormulations import ExplicitGraph
from .SearchStrategies import BreadthFirstSearch, DepthFirstSearch, HeuristicDepthFirstSearch
from .SearchStrategies import GreedyBestFirstSearch, UniformCostSearch
from .Utilities import read_files

import sys

def country_scheduler(your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                      num_output_schedules, depth_bound, frontier_max_size):
    # 1. Initialize Environment
    # a. read resources file
    # b. read templates for operations
    # c. read initial state file
    init_state = read_files.read_csv(initial_state_filename)
    resources = read_files.read_csv(resources_filename)
    transforms = read_files.init_transforms("./src/cs5260/Inputs")
    print(Node.state_quality(init_state, your_country_name, resources))
    # 2. build graph
    #
    # 3. perform search
    # 4 . write out returned schedules to file


# Test
country_scheduler("Atlantis", "src/cs5260/Inputs/resources.csv", "./src/cs5260/Inputs/states.csv", "outputs/output.txt", 1, 1, 1)

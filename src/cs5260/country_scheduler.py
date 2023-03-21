#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from .DataTypes import Action, Heuristic, State, Node
from .ProblemFormulations import ExplicitGraph
from .SearchStrategies import scheduler
from .SearchStrategies import GreedyBestFirstSearch, UniformCostSearch
from .Utilities import read_files, expected_util

import sys

def country_scheduler(your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                      num_output_schedules, depth_bound, frontier_max_size):
    init_state = read_files.read_csv(initial_state_filename)
    resources = read_files.read_csv(resources_filename)
    transforms = read_files.init_transforms("./src/cs5260/Inputs")
    sched = scheduler.scheduler(your_country_name, resources, init_state, transforms, frontier_max_size)
    print(sched.search(depth=depth_bound, num_schedules=num_output_schedules))


    #ted_util.state_quality(init_state, your_country_name, resources))
    # 2. build graph
    #
    # 3. perform search
    # 4 . write out returned schedules to file
# Test
country_scheduler("Atlantis", "src/cs5260/Inputs/resources.csv", "./src/cs5260/Inputs/states.csv", "outputs/output.txt", 1, 2, 1)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import scheduler
import read_files

import time

def country_scheduler(your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                      num_output_schedules, depth_bound, frontier_max_size):
    init_state = read_files.read_csv(initial_state_filename)
    resources = read_files.read_csv(resources_filename)
    transforms = read_files.init_transforms("Inputs")


    start_time = time.time()
    sched = scheduler.scheduler(your_country_name, resources, init_state, transforms, frontier_max_size)
    end_time = time.time()
    results = sched.search(depth=depth_bound, num_schedules=num_output_schedules)
    print(end_time-start_time)
    print(results)
    for schedule in results:
        print("#################################")
        for action in schedule:
            if action['Action']['name'] != "TRANSFER":
                for i in range(len(action['Action']['outputs'])):
                    if action['Action']['outputs'][i]['name'] == action['Action']['name']:
                        print("TRANSFORM of "+ action['Action']['name'] + " with quantity "+str(action['Action']['outputs'][i]['quantity'])+" and EU "+str(action['EU']))
            else:
                print("TRANSFER "+action['Country'][0]+"")
        print("#################################")


# Test command   my_country    resource file           initial state          not used :-)   num_sched, depth, max size
country_scheduler("Atlantis", "Inputs/resources.csv", "Inputs/states.csv", "outputs/output.txt", 3, 5, 100000)

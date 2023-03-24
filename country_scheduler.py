#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import scheduler
import read_files

import datetime

def country_scheduler(your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                      num_output_schedules, depth_bound, frontier_max_size):
    init_state = read_files.read_csv(initial_state_filename)
    resources = read_files.read_csv(resources_filename)
    transforms = read_files.init_transforms("Inputs")


    print(datetime.datetime.now().strftime("%H:%M:%S"))
    sched = scheduler.scheduler(your_country_name, resources, init_state, transforms, frontier_max_size)

    results = sched.search(depth=depth_bound, num_schedules=num_output_schedules)
    print(results)
    print(datetime.datetime.now().strftime("%H:%M:%S"))

    sched_results = ""

    for schedule in results:
        final_sched = "[ "
        # print("#################################")
        for action in schedule:

            if action['Action']['name'] != "TRANSFER":
                final_sched += "(TRANSFORM self (INPUTS "
                for i in range(len(action['Action']['inputs'])):
                    final_sched += "(" + action['Action']['inputs'][i]['name'] + " " + str(action['Action']['inputs'][i]['quantity']) + ")"
                final_sched += ") (OUTPUTS "
                for i in range(len(action['Action']['outputs'])):
                    final_sched += "(" + action['Action']['outputs'][i]['name'] + " " + str(action['Action']['outputs'][i]['quantity']) + ")"
                    if action['Action']['outputs'][i]['name'] == action['Action']['name']:
                        pass
                        # print("TRANSFORM of "+ action['Action']['name'] + " with quantity "+str(action['Action']['outputs'][i]['quantity'])+" and EU "+str(action['EU']))
                final_sched += ") EU: " + str(action['EU']) + "\n"
            else:
                final_sched += "(TRANSFER "+action['Country'][0]+" "+action['Country'][1]+" ("+action['Action']['resource']+" "+str(action['Action']['quantity'])+")) EU: "+str(action['EU']) + "\n"
                # print("TRANSFER "+action['Country'][0]+"")
        final_sched += "]"
        print(final_sched)
        sched_results += final_sched + "\n"
        # print("#################################")
    file1 = open(output_schedule_filename, "w")
    file1. write(sched_results)
    file1.close()


# Test command   my_country    resource file           initial state          not used :-)   num_sched, depth, max size
country_scheduler("Atlantis", "Inputs/resources.csv", "Inputs/states.csv", "Outputs/output1.txt", 3, 10, 10000)

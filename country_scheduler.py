#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import scheduler
import read_files

import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

# The country_scheduler function is the main method to enter the scheduler. It creates the initial state by
# reading from the provided initial_state_filename. Also, the resources and transforms are read in from the
# corresponding files as well. Next the scheduler object is created and the search is run with the provided
# depth and number of output schedules.
def country_scheduler(your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                      num_output_schedules, depth_bound, frontier_max_size):

    # initialize the state, resources, and transforms
    init_state = read_files.read_csv(initial_state_filename)
    resources = read_files.read_csv(resources_filename)
    transforms = read_files.init_transforms("Inputs")

    # for debugging print the start time
    print(datetime.datetime.now().strftime("%H:%M:%S"))

    # create the scheduler object with the passed in information and initialized state
    sched = scheduler.scheduler(your_country_name, resources, init_state, transforms, frontier_max_size)

    # call the search function on the scheduler to do the search
    results = sched.search(depth=depth_bound, num_schedules=num_output_schedules)

    # print the resulting schedules of actions taken along with their Expected Utility values
    print(results)
    # for debugging print the end time
    print(datetime.datetime.now().strftime("%H:%M:%S"))

    sched_results = ""
    num_schedules = 1
    for schedule in results:
        final_sched = "[ "
        # print("#################################")
        print_plot(schedule, num_schedules)
        num_schedules += 1
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

def print_plot(output, file_num: int):
    qualityplotx = []
    qualityploty = []
    EUploty = []
    t = 0
    for action in output:
        # print(str(action['EU'])+ " - "+str(action['TIME']))
        EUploty.append(action['EU'])
        qualityplotx.append(action['TIME'])
        t += 1

    # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
    fig, ax = plt.subplots(figsize=(10, 5.4), layout='constrained')
    ax.plot(qualityplotx, EUploty, label='EU', color='blue')  # Plot some more data on the axes.
    ax.set_ylabel('EU')
    ax.set_xlabel('TIME (in seconds)')  # Add an x-label to the axes.
    ax.set_title("EU over TIME")  # Add a title to the axes.
    ax.legend(loc='lower right')  # Add a legend.
    fig.tight_layout()

    plt.savefig("best_solution_"+str(file_num)+".png")
    plt.show()

# Test command   my_country    resource file           initial state          not used :-)   num_sched, depth, max size
country_scheduler("Atlantis", "Inputs/resources.csv", "Inputs/states.csv", "Outputs/output1.txt", 10, 5, 1000000)

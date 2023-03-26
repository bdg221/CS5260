#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import random

from PriorityQueue import PriorityQueue
from Node import Node
import math, copy, time

class scheduler:

    INIT_STATES: dict[dict]
    RESOURCES: dict[dict]
    COUNTRY: str
    TRANSFORMS: dict[dict]
    FRONTIER_SIZE: int

    def __init__(self, country: str, resources: dict[dict], init_state: dict[dict], transforms: dict[dict], frontier_size: int) -> None:
        self.INIT_STATES = init_state
        self.RESOURCES = resources
        self.COUNTRY = country
        self.TRANSFORMS = transforms
        self.FRONTIER_SIZE = frontier_size

    # This is the main search function that first builds the frontier, then expands the successors adding the successful
    # schedules to a list and returning it.
    def search(self, depth: int, num_schedules: int) -> []:
        final_schedules = []
        schedule = []
        start_time = time.time()
        transform_count = 0
        transfer_count = 0

        debug_count = 0

        # initialize a priority queue for the ret_schedules
        ret_schedules = PriorityQueue(lambda node: self.expected_utility(node.STATE, node.SCHEDULE), False, num_schedules)

        # initialize the root node and add it to the priority queue
        node = Node(self.INIT_STATES, schedule, 0)
        frontier = PriorityQueue(lambda node: self.expected_utility(node.STATE, node.SCHEDULE), False, self.FRONTIER_SIZE).add(node)

        # search the frontier while it is not empty
        while not frontier.is_empty():

            # pop the node with the large EU
            node = frontier.pop()
            temp_actions = []
            # if reached depth_bound then save it to the final_schedules list
            if (len(node.SCHEDULE) >= depth):
                ret_schedules.add(node)
                debug_count += 1

            # otherwise generate successors
            else:

                # start with transforms
                for transform in self.TRANSFORMS:
                    # check that inputs are valid for up to multiples of 499
                    for i in range(1,500):

                        flag = False
                        temp_state = copy.deepcopy(node.STATE)
                        # check inputs to see if the schedule can reach the new node
                        for input_val in self.TRANSFORMS[transform]['inputs']:
                            # if the values are too low to do the transform set the flag and break
                            if int(node.STATE[self.COUNTRY][input_val['name']]) < i * input_val['quantity']:
                                flag = True
                                break
                            # otherwise update input values in temp_state
                            temp_state[self.COUNTRY][input_val['name']] = int(temp_state[self.COUNTRY][input_val['name']]) - i * int(input_val['quantity'])

                        # flag is false so the transform is viable
                        if flag == False:
                            # update temp_state with correct output variables
                            for output in self.TRANSFORMS[transform]['outputs']:
                                temp_state[self.COUNTRY][output['name']] = int(temp_state[self.COUNTRY][output['name']]) + i*int(output['quantity'])
                            # set action to be saved in new schedule
                            action = copy.deepcopy(self.TRANSFORMS[transform])
                            for index in range(len(action['inputs'])):
                                action['inputs'][index]['quantity'] = action['inputs'][index]['quantity'] * i
                            for index in range(len(action['outputs'])):
                                action['outputs'][index]['quantity'] = action['outputs'][index]['quantity'] * i
                            temp_schedule = copy.deepcopy(node.SCHEDULE)
                            temp_schedule.append({"Action": action, "Country": ['self'], "EU": 0, "TIME": time.time()-start_time})
                            temp_eu = self.expected_utility(temp_state, temp_schedule)
                            temp_schedule[len(temp_schedule)-1]['EU'] = temp_eu
                            # if(transform == 'Housing' or transform == 'Electronics'):
                            #     print("!!!!!!!!!!!!!!!!!!!!!!!!!")
                            #     print(temp_schedule)
                            #     print(temp_state)
                            #     print(temp_eu)
                            #     print(self.state_quality(temp_state, self.COUNTRY))
                            #     print("!!!!!!!!!!!!!!!!!!!!!!!!!")
                            transform_count += 1
                            temp_actions.append({'state': temp_state, 'schedule': temp_schedule, 'eu': temp_eu})

                        else:
                            break

                # print("node depth " + str(len(node.SCHEDULE)) + " EU " +str(node.EU))

                # now with transfers
                for country in self.INIT_STATES.keys():
                # while False:
                    # no trading with yourself
                    if (country != self.COUNTRY):
                        for resource in self.RESOURCES.keys():
                            temp_state = copy.deepcopy(node.STATE)
                            min_transfer = {}
                            max_transfer = {}
                            # changed range from int(temp_state[country][resource]) to just 5

                            if (int(temp_state[country][resource]) >= 1 and resource != "Population"):
                                temp_state[self.COUNTRY][resource] = int(temp_state[self.COUNTRY][resource]) + 1
                                temp_state[country][resource] = int(temp_state[country][resource]) - 1
                                temp_schedule = copy.deepcopy(node.SCHEDULE)
                                temp_schedule.append({"Action": {"name": "TRANSFER", "resource":resource, "quantity":1}, "Country": [country, 'self'], "EU": 0, "TIME": time.time()-start_time})
                                temp_eu = self.expected_utility(temp_state, temp_schedule)
                                temp_schedule[len(temp_schedule) - 1]['EU'] = temp_eu
                                temp_actions.append({'state': temp_state, 'schedule': temp_schedule, 'eu': temp_eu})
                                temp_state = copy.deepcopy(node.STATE)
                                if (int(temp_state[country][resource]) > 1):
                                    temp_state[self.COUNTRY][resource] = int(temp_state[self.COUNTRY][resource]) + int(temp_state[country][resource])
                                    temp_state[country][resource] = int(temp_state[country][resource]) - int(temp_state[country][resource])
                                    temp_schedule = copy.deepcopy(node.SCHEDULE)
                                    temp_schedule.append(
                                        {"Action": {"name": "TRANSFER", "resource": resource, "quantity": int(temp_state[country][resource])},
                                         "Country": [country, 'self'], "EU": 0, "TIME": time.time() - start_time})
                                    temp_eu = self.expected_utility(temp_state, temp_schedule)
                                    temp_schedule[len(temp_schedule) - 1]['EU'] = temp_eu
                                    temp_actions.append({'state': temp_state, 'schedule': temp_schedule, 'eu': temp_eu})

                    # should my country trade to others?
                    else:
                        # loop through resources
                        for resource in self.RESOURCES.keys():
                            # loop through countries to trade to
                            for trade_country in self.INIT_STATES.keys():
                                min_transfer = {}
                                max_transfer = {}
                                if trade_country != country:
                                    # changed range from int(temp_state[country][resource]) to just 5
                                    if (int(temp_state[country][resource]) >= 1 and resource != "Population"):
                                        # print(country + " has " + str(temp_state[country][resource]) + " of "+ resource)
                                        temp_state = copy.deepcopy(node.STATE)
                                        temp_state[trade_country][resource] = int(temp_state[trade_country][resource]) + 1
                                        temp_state[country][resource] = int(temp_state[country][resource]) - 1
                                        temp_schedule = copy.deepcopy(node.SCHEDULE)
                                        temp_schedule.append({"Action": {"name": "TRANSFER", "resource":resource, "quantity":1}, "Country": ['self', trade_country], "EU": 0, "TIME": time.time()-start_time})
                                        temp_eu = self.expected_utility(temp_state, temp_schedule)
                                        temp_schedule[len(temp_schedule) - 1]['EU'] = temp_eu
                                        temp_actions.append({'state': temp_state, 'schedule': temp_schedule, 'eu': temp_eu})
                                        temp_state = copy.deepcopy(node.STATE)
                                        if (int(temp_state[country][resource]) > 1):
                                            temp_state[trade_country][resource] = int(
                                                temp_state[trade_country][resource]) + int(temp_state[country][resource])
                                            temp_state[country][resource] = int(temp_state[country][resource]) - int(temp_state[country][resource])
                                            temp_schedule = copy.deepcopy(node.SCHEDULE)
                                            temp_schedule.append({"Action": {"name": "TRANSFER", "resource": resource,
                                                                             "quantity": int(temp_state[country][resource])},
                                                                  "Country": ['self', trade_country], "EU": 0,
                                                                  "TIME": time.time() - start_time})
                                            temp_eu = self.expected_utility(temp_state, temp_schedule)
                                            temp_schedule[len(temp_schedule) - 1]['EU'] = temp_eu
                                            temp_actions.append(
                                                {'state': temp_state, 'schedule': temp_schedule, 'eu': temp_eu})
                # loop through temp_actions to randomly look to add to the frontier
                random.shuffle(temp_actions)
                for actions_index in range(len(temp_actions)):
                    frontier.add(Node(temp_actions[actions_index]['state'], temp_actions[actions_index]['schedule'], temp_actions[actions_index]['eu']))



        # print("Transforms: "+str(transform_count)+ " - Transfers: "+str(transfer_count)+" - Total: "+str(transform_count+transfer_count) )
        # print("Total schedules found: "+ str(debug_count))
        while not ret_schedules.is_empty():

            # pop the node with the large EU and save schedule in list to return
            node = ret_schedules.pop()
            final_schedules.append(node.SCHEDULE)

        return final_schedules




    # The state_quality method gets the state quality of a particular country given a state
    def state_quality(self, states: dict[dict], country: str):
        ret_value = 0

        # loop through the resources
        for resource in self.RESOURCES:

            # check if this is a tiered weight/factor resource
            # if so then use the appropriate tiered weight
            if (self.RESOURCES[resource]['Weight'].count(';') > 0):
                temp_weights = self.RESOURCES[resource]['Weight'].split(';')
                temp_factors = self.RESOURCES[resource]['Factor'].split(';')

                # check either tier to see if the resource/population ratio matches the factor
                for index in range(len(temp_factors)):
                    # DEBUGGING TEST
                    x = float(states[country][resource]) / float(states[country]['Population'])
                    if x > 0.5:
                        pass
                    if (float(states[country][resource]) / float(states[country]['Population']) < float(temp_factors[index])):
                        break
                # print(str(states[country][resource]) + " of " + resource + " is " + str(float(states[country][resource])* float(temp_weights[index])))
                # use the appropriate weight from the index with the matching factor
                ret_value += float(states[country][resource])/ float(states[country]['Population']) * float(temp_weights[index]) * 1000

            # default value: resource/popultation * weight
            else:
                # print(str(states[country][resource]) + " of " + resource + " is " + str(
                #     float(states[country][resource]) * float(self.RESOURCES[resource]['Weight'])))
                ret_value += float(states[country][resource])/ float(states[country]['Population']) * float(self.RESOURCES[resource]['Weight']) * 1000
        return ret_value

    # The undiscounted reward is the state_quality of a state minus the state_quality of the inital state
    def undiscounted_reward(self, state_quality1: float, state_quality2: float) -> float:
        # current node's state quality - initial_state_quality
        return state_quality2 - state_quality1

    # The discounted reward is the undiscounted_reward * gammaa^depth
    def discounted_reward(self, reward: float, N: int) -> float:
        # start with gamma of 0.5 since gamma needs to be 0<=gamma<1
        gamma = 0.5
        return gamma**N * reward

    # The country_accept method checks the probability that a country involved in
    # a transfer will accept the transfer.
    def country_accept(self, country: str, state: dict[dict], depth) -> float:
        k = 1
        x = 0

        # state quality of country
        sq = self.state_quality(state, country)
        # original state quality of country
        og_sq = self.state_quality(self.INIT_STATES, country)

        # undiscounted reward
        ur = self.undiscounted_reward(og_sq, sq)

        # discounted reward
        dr = self.discounted_reward(ur, depth)

        expon = -k * (dr - x)
        return (1 / (1 + math.exp(expon)))

    # The success_probability method uses the product of the probability of a country
    # accepting a transfer to determine the probability of a transfer (really the
    # complete schedule up to that point) is accepted by all involved countries
    def success_probability(self, state: dict[dict], depth, schedule) -> float:
        ret_val = 1
        # get the countries involved in the action(transfer) and call prob_accept
        for index in range(len(schedule[len(schedule) - 1]['Country'])):
            if schedule[len(schedule) - 1]['Country'][index] == 'self':
                temp_country = self.COUNTRY
            else:
                temp_country = schedule[len(schedule) - 1]['Country'][index]
            prob_accept = self.country_accept(temp_country, state, depth)
            ret_val *= prob_accept
        return ret_val

    # The expected_utility combines the above methods to provide the complete
    # expected utility of a particular schedule given a particular state
    def expected_utility(self, state: dict[dict], schedule: list[dict]) -> float:

        # negative constant for failure case
        # starting with -0.5 to see results
        neg_C = -0.25

        # get the depth since it is used in the discounted reward
        depth = len(schedule)

        # state quality of country
        sq = self.state_quality(state, self.COUNTRY)
        # original state quality of country
        og_sq = self.state_quality(self.INIT_STATES, self.COUNTRY)
        # undiscounted reward
        ur = self.undiscounted_reward(og_sq, sq)
            #og_sq, sq)

        # discounted reward
        dr = self.discounted_reward(ur, depth)

        # check if the latest Action is a (transfOrm or transfEr
        # if TRANSFORM then send back self discounted reward
        # print("#####################")
        # print("original state quality: "+str(og_sq))
        # print("new state quality: "+str(sq))
        # print("Undiscounted Reward: "+str(ur))
        # print("Discounted Reward: "+str(dr))
        # print(schedule)
        # print("#####################")

        # The root node has an EU of zero
        if (len(schedule) == 0):
            return 0

        # if this is a transform then the probability of success is 1
        # therefore just use the discounted reward
        if schedule[len(schedule) - 1]['Action']['name'] != 'TRANSFER':
            return dr
        # if this is a transfer perform the full EU
        else:
            prob_success = self.success_probability(state, depth, schedule)
            eu = (prob_success * dr) + ((1 - prob_success) * neg_C)
            return eu
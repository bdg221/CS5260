#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Union
from ..DataTypes import Action, Heuristic, Node, PriorityQueue, Solution, State

import math, copy

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

    def search(self, depth: int, num_schedules: int) -> []:
        final_schedules = []
        schedule = []
        node = Node(self.INIT_STATES, schedule, 0)
        frontier = PriorityQueue(lambda node: self.expected_utility(node.STATE, node.SCHEDULE), False).add(node)

        while not frontier.is_empty():

            node = frontier.pop()
            # if reached depth_bound
            if (len(node.SCHEDULE) >= depth):
                final_schedules.append(node.SCHEDULE)
                if len(final_schedules) >= num_schedules:
                    print(len(frontier.as_list()))
                    return final_schedules
            else:
                # generate successors

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
                            temp_schedule.append({"Action": action, "EU": 0})
                            temp_eu = self.expected_utility(temp_state, temp_schedule)
                            temp_schedule.pop()
                            temp_schedule.append({"Action": action, "Country": ['self'], "EU": temp_eu})
                            frontier.add(Node(temp_state, temp_schedule, temp_eu))

                        else:
                            break

                # next is transfers



    def state_quality(self, states: dict[dict], country: str):
        ret_value = 0
        for resource in self.RESOURCES:

            # check if this is a tiered weight/factor resource
            # if so then use the appropriate tiered weight
            if (self.RESOURCES[resource]['Weight'].count(';') > 0):
                temp_weights = self.RESOURCES[resource]['Weight'].split(';')
                temp_factors = self.RESOURCES[resource]['Factor'].split(';')
                for index in range(len(temp_factors)):
                    if (float(states[country][resource]) / float(states[country]['Population']) < float(
                            temp_factors[index])):
                        break
                ret_value += float(states[country][resource]) / float(states[country]['Population']) * float(
                    temp_weights[index])

            # default value: resource/popultation * weight
            else:
                ret_value += float(states[country][resource]) / float(states[country]['Population']) * float(
                    self.RESOURCES[resource]['Weight'])
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

    def success_probability(self, state: dict[dict], depth) -> float:
        ret_val = 1
        for country in state:
            ret_val *= self.country_accept(country, state, depth)
        return ret_val

    def expected_utility(self, state: dict[dict], schedule: list[dict]) -> float:

        # negative constant for failure case
        # starting with -0.5 to see results
        neg_C = -0.5

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

        if (len(schedule) == 0):
            return 0
        if schedule[len(schedule) - 1]['Action']['name'] != 'TRANSFER':
            return dr
        else:
            prob_success = self.success_probability(state, depth)
            eu = (prob_success * dr) + ((1 - prob_success) * neg_C)
            return eu



#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from .Action import Action
from .State import State
from uuid import UUID, uuid4

class Node(object):

   ID: UUID
   STATE: dict[dict]
   SCHEDULE: []
   EU: float
   PARENT: Node

   def __init__(self, state: dict[dict], parent: Node, eu: float) -> None:
      super().__init__()
      self.ID = uuid4()
      self.STATE = state
      self.PARENT = parent
      self.PARENT_ACTION = parent_action
      self.PATH_COST = path_cost

   def __eq__(self, other: Node) -> bool:
      return self.ID == other.ID

   def __hash__(self) -> int:
      return hash(self.ID)

   def state_quality(states: dict[dict], country: str, resources: dict[dict]):
      ret_value = 0
      for resource in resources:

         # check if this is a tiered weight/factor resource
         # if so then use the appropriate tiered weight
         if (resources[resource]['Weight'].count(';') > 0) :
            temp_weights = resources[resource]['Weight'].split(';')
            temp_factors = resources[resource]['Factor'].split(';')
            for index in range(len(temp_factors)):
               if ( float(states[country][resource])/float(states[country]['Population']) < float(temp_factors[index])):
                  break
            print(resource + " - " + str(float(states[country][resource]) / float(states[country]['Population']) * float(temp_weights[index])))
            ret_value += float(states[country][resource]) / float(states[country]['Population']) * float(temp_weights[index])

         # default value: resource/popultation * weight
         else:
            print(resource + " - " + str(
               float(states[country][resource])/float(states[country]['Population']) * float(resources[resource]['Weight'])))
            ret_value += float(states[country][resource])/float(states[country]['Population']) * float(resources[resource]['Weight'])
      return ret_value

   # The undiscounted reward is the state_quality of a state minus the state_quality of the inital state
   def undiscounted_reward(self, state_quality1: float, state_quality2: float) -> float:
      # current node's state quality - initial_state_quality
      return state_quality2 - state_quality1

   # The discounted reward is the undiscounted_reward * gammaa^depth
   def discounted_reward(self, reward: float, N: int) -> float:
      # start with gamma of 0.5 since gamma needs to be 0<=gamma<1
      gamma = 0.5
      return 0.5^N * reward

   def country_accept(self, country: str, state: dict[dict]) -> float:
      k = 1
      x = 0

      # state quality of country
      sq = self.state_quality(state, country)
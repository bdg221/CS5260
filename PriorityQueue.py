#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Callable, List, Tuple
from Node import Node
import operator

class PriorityQueue(object):

   queue: List[Tuple[Node, float]]
   evaluation_function: Callable[[Node], float]
   priority_operator: bool
   max_size: int

   def __init__(self, eval_fn: Callable[[Node], float], ascending: bool, max_size: int) -> None:
      super().__init__()
      self.queue = []
      self.evaluation_function = eval_fn
      self.priority_operator = operator.gt if ascending else operator.lt
      self.max_size = max_size

   def add(self, node: Node) -> PriorityQueue:
      cost = node.EU
      for idx, node_and_cost in enumerate(self.queue):
         if self.priority_operator(cost, node_and_cost[1]):
            self.queue.insert(idx, (node, cost))
            if (len(self.queue) > self.max_size):
               self.queue.pop(0)
            return self
      self.queue.append((node, cost))
      if (len(self.queue) > self.max_size):
         self.queue.pop(0)
      return self

   def is_empty(self) -> bool:
      return len(self.queue) == 0

   def pop(self) -> Node:
      return self.queue.pop()[0]

   def as_list(self) -> List[Node]:
      return [item for item, _ in self.queue][::-1]

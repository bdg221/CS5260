#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

class Node(object):

   STATE: dict[dict]
   SCHEDULE: []
   EU: float

   def __init__(self, state: dict[dict], schedule, eu: float) -> None:
      super().__init__()
      self.STATE = state
      self.SCHEDULE = schedule
      self.EU = eu

   def __eq__(self, other: Node) -> bool:
      return self.SCHEDULE == other.SCHEDULE


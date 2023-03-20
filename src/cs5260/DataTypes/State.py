#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from src.cs5260.Utilities.read_files import read_csv


class State(object):



   def __init__(self, values: dict[dict]) -> None:
      super().__init__()
      self.schedule = []
      self.values = values


   def __eq__(self, other: State) -> bool:
      return self.ID == other.ID

   def __hash__(self) -> int:
      return hash(self.ID)

   def __repr__(self) -> dict:
      return self.values

from typing import Dict, List
from utilities import select_action


class Edge:

	def __init__(self, s: int, t: int, letter: str, p: float):
		self.s = s; self.t = t; self.letter = letter; self.p = p

	def __repr__(self):
		return '{}->{} {}/{}'.format(self.s,self.t,self.letter,self.p)


class Graph:

	def __init__(self, start: int, transitions: Dict[int, List[Edge]]):
		self.start = start
		self.transitions = transitions

	def pick_edge(self, v):
		actions = [(e.p, e) for e in self.transitions[v]]
		return select_action(actions)[0]

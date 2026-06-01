from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .diagram import GridDiagram
from .rectangles import Rectangle, RectangleFinder
from .state import State

StateElement = Dict[State, int]

@dataclass(frozen=True)
class DifferentialContribution:
	target: State
	rectangle: Rectangle


@dataclass
class DifferentialBuilder:
	grid: GridDiagram
	_states: Tuple[State, ...] = field(init=False, repr=False)
	_finder: RectangleFinder = field(init=False, repr=False)
	
	def __post_init__(self) -> None:
		self._states = tuple(self.grid.all_states())
		self._finder = RectangleFinder(self.grid)
		
	@property
	def states(self) -> Tuple[State, ...]:
		return self._states
		
	def _validate_state(self, state: State) -> None:
		if state.n != self.grid.n:
			raise ValueError("State size must match grid size")
	
	def _fully_blocked_rectangles_between(self, x: State, y: State) -> List[Rectangle]:
		self._validate_state(x)
		self._validate_state(y)
		
		return self._finder.fully_blocked_rectangles_between(x, y)
		
	def contributions_between(self, x: State, y: State) -> List[DifferentialContribution]:
		return [
			DifferentialContribution(target=y, rectangle=rect)
			for rect in self._fully_blocked_rectangles_between(x,y)
		]
	
	def contributions_from(self, x: State)-> List[DifferentialContribution]:
		self._validate_state(x)
		out: List[DifferentialContribution] = []
		for y in self._states:
			if y == x:
				continue
			out.extend(self.contributions_between(x,y))
		return out

	@staticmethod
	def add_state_mod_2(element: StateElement, state: State) -> None:
		element[state] = (element.get(state, 0) +1) %2
		if element[state] == 0:
			del element[state]
			
	def differential_of_state(self, x: State) -> StateElement:
		out: StateElement={}
		for contribution in self.contributions_from(x):
			self.add_state_mod_2(out, contribution.target)
		return out
	
	__call__ = differential_of_state
	def matrix(self) -> List[List[int]]:
		index = {state: i for i, state in enumerate(self._states)}
		matrix = [[0 for _ in self._states] for _ in self._states]
		for j,x in enumerate(self._states):
			dx = self.differential_of_state(x)
			for y, coeff in dx.items():
				matrix[index[y]][j] = coeff %2
		return matrix
	
	
	
	

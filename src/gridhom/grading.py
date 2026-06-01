from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Iterable, Tuple

from .diagram import GridDiagram
from .state import State

Point = Tuple[float, float]
GradingFunction = Callable[[State], int]

@dataclass(frozen=True)
class GridGrading:
	grid: GridDiagram
	
	def _validate_state(self, state: State) -> None:
		if state.n != self.grid.n:
			raise ValueError("State size must match grid size")
	
	@staticmethod
	def _I(points_p: Iterable[Point], points_q: Iterable[Point]) -> int:
		p_tuple = tuple(points_p)
		q_tuple = tuple(points_q)
		return sum(
			1
			for p in p_tuple
			for q in q_tuple
			if p[0] < q[0] and p[1] < q[1]
		)
	
	@classmethod
	def _J(cls, points_p: Iterable[Point], points_q: Iterable[Point]) -> Fraction:
		p_tuple = tuple(points_p)
		q_tuple = tuple(points_q)
		return Fraction(cls._I(p_tuple, q_tuple) + cls._I(q_tuple, p_tuple), 2)
	
	def _maslov_from_markings(
		self,
		state: State,
		markings: Iterable[Point],
	) -> int:
		
		self._validate_state(state)
		state_points = state.points
		marking_points = tuple(markings)
		
		value = (
			self._J(state_points, state_points)
			- 2*self._J(state_points, marking_points)
			+ self._J(marking_points, marking_points)
			+1
		)
		
		if value.denominator != 1:
			raise ValueError("Maslov grading should be integral")
		return int(value)
	
	#M_O
	def maslov_o(self, state: State) -> int:
		return self._maslov_from_markings(state, self.grid.o_positions)
	
	#M_X
	def maslov_x(self, state: State) -> int:
		return self._maslov_from_markings(state, self.grid.x_positions)
		
	#Maslov 
	def maslov(self, state: State) -> int:
		return self.maslov_o(state)
	
	#Alexander
	def alexander(self, state: State) -> int:
		mo = self.maslov_o(state)
		mx = self.maslov_x(state)
		value = Fraction(mo-mx-self.grid.n + 1, 2)
		
		if value.denominator != 1:
			raise ValueError(
				"Alexander grading should be integral for knot grid diagrams"
			)
		return value
	
	def functions(self) -> Tuple[GradingFunction, GradingFunction]:
		return self.maslov, self.alexander
		
	
	

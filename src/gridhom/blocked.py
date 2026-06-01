from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Tuple
from sympy import Integer, Symbol, expand, pprint, simplify

from .diagram import GridDiagram
from .differential import DifferentialBuilder, StateElement
from .state import State

Bigrading = Tuple[int, int]
HomologyDimensions = Dict[Bigrading, int]
GradingFunction = Callable[[State], int]

@dataclass
class FullyBlockedComplex:
	grid: GridDiagram
	differential_builder: DifferentialBuilder = field(init=False, repr=False)
	
	def __post_init__(self) -> None:
		self.differential_builder = DifferentialBuilder(self.grid)
	
	@property
	def  states(self) -> Tuple[State, ...]:
		return self.differential_builder.states
	
	def differential_of_state(self, state: State) -> StateElement:
		return self.differential_builder.differential_of_state(state)
		
	def differential_matrix(self) -> List[List[int]]:
		return self.differential_builder.matrix()
	
	#group states by bigrading
	def graded_states(
		self,
		maslov: GradingFunction,
		alexander: GradingFunction
	) -> Dict[Bigrading, Tuple[State, ...]]:
		graded: Dict[Bigrading, List[State]] = {}
		for state in self.states:
			key = (maslov(state), alexander(state))
			graded.setdefault(key, []).append(state)
		return {key: tuple(states) for key, states in graded.items()}
		
	#differential matrix restricted to bigrading (d,s) -> (d-1,s)
	def differential_matrix_in_bigrading(
		self,
		d: int,
		s: int,
		maslov: GradingFunction,
		alexander: GradingFunction,
	) -> Tuple[Tuple[State, ...], Tuple[State, ...], List[List[int]]]:
		
		source = tuple(
			state for state in self.states
			if maslov(state)==d and alexander(state)==s
		)
		
		target = tuple(
		state
		for state in self.states
		if maslov(state) == d-1 and alexander(state) == s
		)
		
		target_index = {state: i for i,state in enumerate(target)}
		
		matrix = [[0 for _ in source] for _ in target]
		
		for j, state in enumerate(source):
			image = self.differential_of_state(state)
			for out_state, coeff in image.items():
				i = target_index.get(out_state)
				if i is not None and coeff % 2:
					matrix[i][j] ^= 1
		return source, target, matrix
		
	@staticmethod
	def rank_mod_2(matrix: List[List[int]]) -> int:
		if not matrix: #empty list amounts to 0
			return 0
		if not matrix[0]:
			return 0
		reduced = [row[:] for row in matrix]
		row_count = len(reduced)
		col_count = len(reduced[0])
		pivot_row = 0
		
		for col in range(col_count):
			pivot = None
			for row in range(pivot_row, row_count):
				if reduced[row][col] & 1:
					pivot = row
					break
			if pivot is None:
					continue
					
			reduced[pivot_row], reduced[pivot] = reduced[pivot], reduced[pivot_row]
			for row in range(row_count):
				if row != pivot_row and (reduced[row][col] &1):
					for k in range(col, col_count):
						reduced[row][k] ^= reduced[pivot_row][k]
			pivot_row += 1
			if pivot_row == row_count:
				break
		return pivot_row
	
	#dimension of GH_d(G,s)
	def homology_dimension_in_bigrading(
		self,
		d: int,
		s: int,
		maslov: GradingFunction,
		alexander: GradingFunction,
	)-> int:
		source, _, d_ds = self.differential_matrix_in_bigrading(d, s, maslov, alexander)
		_, _, d_dplus1_s = self.differential_matrix_in_bigrading(d+1, s, maslov, alexander)
		return len(source) - self.rank_mod_2(d_ds)-self.rank_mod_2(d_dplus1_s)
		
	def homology_dimensions(
		self,
		maslov: GradingFunction,
		alexander: GradingFunction,
		bigradings: Iterable[Bigrading] | None = None,
	) -> HomologyDimensions:
		
		if bigradings is None:
			bigradings = self.graded_states(maslov, alexander).keys()
		
		out: HomologyDimensions = {}
		for d, s in bigradings:
			dim = self.homology_dimension_in_bigrading(d,s, maslov, alexander)
			if dim:
				out[(d,s)] = dim
		return out
		
	def poincare_polynomial_terms(
		self,
		maslov: GradingFunction,
		alexander: GradingFunction,
		bigradings: Iterable[Bigrading] | None=None,
	) -> List[Tuple[int, int, int]]:
		
		dims = self.homology_dimensions(maslov, alexander, bigradings)
		
		return sorted((d, s, dim) for (d,s), dim in dims.items())
		
	def poincare_polynomial(
    self,
    maslov: GradingFunction,
    alexander: GradingFunction,
    bigradings: Iterable[Bigrading] | None = None,
	):
		q = Symbol("q")
		t = Symbol("t")
		terms = self.poincare_polynomial_terms(maslov, alexander, bigradings)
		expr = sum(Integer(dim) * q**d * t**s for d, s, dim in terms)
		return expand(expr)

	def print_fully_blocked(
		self,
		maslov: GradingFunction,
		alexander: GradingFunction,
		bigradings: Iterable[Bigrading] | None = None,
	) -> None:
		pprint(self.poincare_polynomial(maslov, alexander, bigradings), use_unicode=True)

	def simply_blocked_poincare_polynomial(
		self,
		maslov: GradingFunction,
		alexander: GradingFunction,
		bigradings: Iterable[Bigrading] | None = None,
	):
		q = Symbol("q")
		t = Symbol("t")
		full_poly = self.poincare_polynomial(maslov, alexander, bigradings)
		factor = (1 + q**-1 * t**-1) ** (self.grid.n - 1)
		return simplify(expand(full_poly / factor))

	def print_simply_blocked(
		self,
		maslov: GradingFunction,
		alexander: GradingFunction,
		bigradings: Iterable[Bigrading] | None=None,
	) -> None:
		pprint(self.simply_blocked_poincare_polynomial(maslov, alexander, bigradings), use_unicode=True)
			
				
			
			

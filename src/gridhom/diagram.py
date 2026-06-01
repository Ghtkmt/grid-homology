from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Iterable, List, Sequence, Tuple


Point = Tuple[float, float]

@dataclass(frozen=True)
class GridDiagram:
	x_rows_by_col: Tuple[int, ...]
	o_rows_by_col: Tuple[int, ...]
	
	def __post_init__(self) -> None:
		n = len(self.x_rows_by_col)
		if n==0 or len(self.o_rows_by_col) != n:
			raise ValueError("X-markings and O-markings must have the same positive number")
		if sorted(self.x_rows_by_col) != list(range(n)):
			raise ValueError("X-markings must occupy each column exactly once")
		if sorted(self.o_rows_by_col) != list(range(n)):
			raise ValueError("O-markings must occupy each column exactly once")
		if any(xc == oc for xc, oc in zip(self.x_rows_by_col, self.o_rows_by_col)):
			raise ValueError("X and O cannot occupy the same square")
	
	@property
	def n(self) -> int:
		return len(self.x_rows_by_col)
	
	@property
	def x_positions(self) -> Tuple[Point, ...]:
		return tuple((r+0.5,c+0.5) for c, r in enumerate(self.x_rows_by_col))
		
	@property
	def o_positions(self) -> Tuple[ Point, ...]:
		return tuple((r+0.5,c+0.5) for c, r in enumerate(self.o_rows_by_col))
	
	@property
	def x_set(self) ->frozenset[Point]:
		return frozenset(self.x_positions)
		
	@property
	def o_set(self) ->frozenset[Point]:
		return frozenset(self.o_positions)
	
	def has_x(self, point: Point) -> bool:
		return point in self.x_set
		
	def has_o(self, point: Point) -> bool:
		return point in self.o_set
	
	def all_states(self) -> Iterable["State"]:
		from .state import State
		for perm in permutations(range(self.n)):
			yield State(tuple(perm))
			
	@classmethod
	def from_rows(cls, rows: Sequence[str]) -> "GridDiagram":
		n = len(rows)
		if n == 0 or any(len(row) != n for row in rows):
			raise ValueError("rows must describe a nonempty square grid")

		x_cols: List[int] = []
		o_cols: List[int] = []
		for r, row in enumerate(rows):
			xs = [c for c, ch in enumerate(row) if ch.upper() == "X"]
			os = [c for c, ch in enumerate(row) if ch.upper() == "O"]
			if len(xs) != 1 or len(os) != 1:
				raise ValueError(f"row {r} must contain exactly one X and one O")
			x_cols.append(xs[0])
			o_cols.append(os[0])
		x_cols.reverse()
		o_cols.reverse()
		
		def invert_perm(cols_by_row):
			rows_by_col = [0] * len(cols_by_row)
			for r, c in enumerate(cols_by_row):
				rows_by_col[c] = r
			return tuple(rows_by_col)

		return cls(tuple(invert_perm(x_cols)), tuple(invert_perm(o_cols)))


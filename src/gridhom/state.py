from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Tuple

Point = Tuple[float, float]

@dataclass(frozen=True)
class State:
	rows_by_col: Tuple[int, ...]
	
	def __post_init__(self) -> None:
		n = len(self.rows_by_col)
		if sorted(self.rows_by_col) != list(range(n)):
			raise ValueError("A grid state must contain exactly one point in each row and each column")
		
	@property
	def n(self) -> int:
		return len(self.rows_by_col)
	
	@property
	def points(self) -> Tuple[Point, ...]:
		return tuple((r,c) for c, r in enumerate(self.rows_by_col))
		
	@property
	def point_set(self) -> FrozenSet[Point]:
		return frozenset(self.points)
		
	def row(self, col: int) -> int:
		return self.rows_by_col[col]
		
	def differs_from(self, other:"state") -> Tuple[int, ...]:
		if self.n != other.n:
			raise ValueError("States must have the same size")
		return tuple(c for c in range(self.n) if self.rows_by_col[c] != other.rows_by_col[c])
	
	def swap_cols(self, c1: int, c2: int) -> "State":
		rows = list(self.rows_by_col)
		rows[c1], rows[c2] = rows[c2], rows[c1]
		return State(tuple(rows))
			
				
			

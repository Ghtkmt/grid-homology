from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

from .diagram import GridDiagram
from .state import State

Point = Tuple[float, float]

def _cyclic_open_interval(start: int, end: int, n: int) -> Tuple[int, ...]:
	out = []
	k = start  % n
	while k!= end:
		out.append(k)
		k = (k+1) % n
	out.append(end)
	return tuple(out)
	
@dataclass(frozen=True)
class Rectangle:
	n: int
	row_start: int
	row_end: int
	col_start: int 
	col_end: int 
	
	@property
	def horizontal_interior(self) ->Tuple[int, ...]:
		return _cyclic_open_interval(self.row_start, self.row_end, self.n)
		
	@property
	def vertical_interior(self) ->Tuple[int, ...]:
		return _cyclic_open_interval(self.col_start, self.col_end, self.n)
		
	def contains_interior_point(self, point: Point) -> bool:
		x, y = point
		return (
			((x-self.horizontal_interior[0]) %self.n < (self.horizontal_interior[-1]-self.horizontal_interior[0]) %self.n) 
				and (x !=self.horizontal_interior[0])
				and (y != self.vertical_interior[0])
				and (( y - self.vertical_interior[0]) %self.n < (self.vertical_interior[-1]-self.vertical_interior[0]) %self.n)
				)
	
	def interior_count(self, points: Iterable[point]) -> int:
		return sum(1 for p in points if self.contains_interior_point(p))
		
	def state_interior_count(self, state: State) -> int:
		return self.interior_count(state.points)
		
	def x_count(self, grid: GridDiagram) -> int:
		return self.interior_count(grid.x_positions)
		
	def o_count(self, grid: GridDiagram) -> int:
		return self.interior_count(grid.o_positions)
		
	def is_empty_for_states(self, x: State, y: State) -> bool:
		return self.state_interior_count(x)==0 and self.state_interior_count(y) ==0
	
	def is_x_free(self, grid: GridDiagram) ->bool:
		return self.x_count(grid) == 0
	
	def is_o_free(self, grid: GridDiagram) ->bool:
		return self.o_count(grid) == 0
		
		
class RectangleFinder:
	def __init__(self, grid: GridDiagram):
		self.grid= grid
		
	def rectangles_between(self, x: State, y: State) -> List[Rectangle]:
		if x.n != self.grid.n or y.n != self.grid.n:
			return ValueError("State size must match grid size")
		differing_cols = x.differs_from(y)
		if len(differing_cols) != 2:
			return []
		c1, c2 = differing_cols
		r1x, r2x = x.row(c1), x.row(c2)
		r1y, r2y = y.row(c1), y.row(c2)
		if not (r1x == r2y and r2x==r1y):
			return []
		if r1x<r1y %self.grid.n:
			return [
				Rectangle(self.grid.n, r1x, r1y, c1, c2),
				Rectangle(self.grid.n, r1y, r1x, c2, c1)
				]
		elif r1x > r1y %self.grid.n:
			return [
				Rectangle(self.grid.n, r2x, r2y, c2, c1),
				Rectangle(self.grid.n, r2y, r2x, c1, c2)
			]
	
	def empty_rectangles_between(self, x: State, y: State) -> List[Rectangle]:
		out=[]
		for rect in self.rectangles_between(x, y):
			if rect.is_empty_for_states(x, y):
				out.append(rect)
		return out
	
	def empty_x_free_rectangles_between(self, x: State, y: State) -> List[Rectangle]:
		out=[]
		for rect in self.empty_rectangles_between(x, y):
			if rect.is_x_free(self.grid):
				out.append(rect)
		return out
		
	def fully_blocked_rectangles_between(self, x: State, y: State) -> List[Rectangle]:
		out=[]
		for rect in self.empty_rectangles_between(x, y):
			if rect.is_x_free(self.grid) and rect.is_o_free(self.grid):
				out.append(rect)
		return out
		
	
	
			
		

from gridhom import GridDiagram, State, Rectangle, RectangleFinder, DifferentialContribution, DifferentialBuilder

def test_fully_blocked_rectangles_between_swapped_cols():
	g = GridDiagram.from_rows([
		"o.x..",
		".o.x.",
		"..o.x",
		"x..o.",
		".x..o"
	])
	x = State((0,1,2,3,4))
	y = State((0,2,1,3,4))
	builder = DifferentialBuilder(g)
	
	rects = builder._fully_blocked_rectangles_between(x,y)
	print(rects)
	assert len(rects) == 1
	

g = GridDiagram.from_rows([
		"o.x..",
		".o.x.",
		"..o.x",
		"x..o.",
		".x..o"
])
builder = DifferentialBuilder(g)
x = State((0,1,2,3,4))
y = State((0,2,1,3,4))
print(g) 
print(builder.differential_of_state(x))
print(builder.differential_of_state(y))
print(builder.matrix())

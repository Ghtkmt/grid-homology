from gridhom import GridDiagram, State, Rectangle, RectangleFinder

def test_rectangles_between_swapped_cols():
	g = GridDiagram.from_rows([
		"o.x..",
		".o.x.",
		"..o.x",
		"x..o.",
		".x..o"
	])
	x = State((0,1,2,3,4))
	y = State((0,3,2,1,4))
	rf = RectangleFinder(g)
	
	rects = rf.rectangles_between(x,y)
	assert len(rects)== 2

def test_no_rect():
	g = GridDiagram.from_rows([
		"o.x..",
		".o.x.",
		"..o.x",
		"x..o.",
		".x..o"
	])
	x = State((0,1,2,3,4))
	y = State((4,2,3,1,0))
	rf = RectangleFinder(g)
	
	rects = rf.rectangles_between(x,y)
	assert len(rects)== 0
	
def test_no_empty_rect():
	g = GridDiagram.from_rows([
		"o.x..",
		".o.x.",
		"..o.x",
		"x..o.",
		".x..o"
	])
	x = State((0,1,2,3,4))
	y = State((0,3,2,1,4))
	rf = RectangleFinder(g)
	
	e_rects = rf.empty_rectangles_between(x,y)
	assert len(e_rects)== 0

def test_has_empty_rec():
	g = GridDiagram.from_rows([
		"o.x..",
		".o.x.",
		"..o.x",
		"x..o.",
		".x..o"
	])
	x = State((0,1,2,3,4))
	y = State((0,2,1,3,4))
	rf = RectangleFinder(g)
	rects = rf.rectangles_between(x,y)
	

	e_rects = rf.empty_rectangles_between(x,y)
	print(e_rects)
	assert len(e_rects)== 1
	
def test_has_empty_x_free_rec():
	g = GridDiagram.from_rows([
		"o.x..",
		".o.x.",
		"..o.x",
		"x..o.",
		".x..o"
	])
	x = State((0,1,2,3,4))
	y = State((0,1,2,4,3))
	rf = RectangleFinder(g)
	
	e_xf_recs = rf.empty_x_free_rectangles_between(x,y)
	recs = rf.rectangles_between(x,y)
	
			
	assert len(e_xf_recs) == 0
	
	

from gridhom.grading import GridGrading
from gridhom.blocked import FullyBlockedComplex
from gridhom.diagram import GridDiagram

g = GridDiagram((1,0,4,3,2),(4,3,2,1,0))
									
grading = GridGrading(g)
maslov, alexander = grading.functions()

complex_ = FullyBlockedComplex(g)
complex_.print_fully_blocked(maslov, alexander)
complex_.print_simply_blocked(maslov, alexander)

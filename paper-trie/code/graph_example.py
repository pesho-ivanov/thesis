import numpy as np
from bio import letters
from graph import Edge, Graph
from graph_full import generate_read

transitions = {0: [Edge(0, 1, l, 1 / 4) for l in letters],
			   1: [Edge(1, 0, l, 1 / 4) for l in letters]}
graph = Graph(0, transitions)


def generate():
	read = generate_read(graph)
	print(read)
	# Possible output:
	#
	# Segment: GGCT
	# Mutations: [(0, 'copy', 'G'), (1, 'copy', 'G'), (0, 'copy', 'T'),
	#             (1, 'del', '-'), (0, 'copy', 'T')]
	# Read Errors: [(0, 'read', 'G'), (1, 'read', 'G'), (0, 'error', 'C'),
	#               (0, 'read', 'T')]

	return read



# set interesting random seed; ensure reproducibility
np.random.seed(89)

read = generate()
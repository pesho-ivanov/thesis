import numpy as np
from bio import Segment
from graph_example import generate

def interesting_read(read: Segment):
	missing_ops = {'copy', 'edit', 'ins', 'del'} - {a for _, a, _ in read.mutations}
	missing_errors = {'read', 'error'}- {a for _, a, _ in read.errors}

	if len(missing_ops) > 0 or len(missing_errors) > 0:
		print(missing_ops, missing_errors)
		return False
	else:
		return True


for i in range(100):
	np.random.seed(i)
	read = generate()
	if interesting_read(read):
		print(i)
		break
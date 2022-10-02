import numpy as np
from bio import Genome

def cut(g_mut: Genome, L=4):
	start = np.random.randint(0, len(g_mut) - L + 1)
	return g_mut.get_segment(start, L)

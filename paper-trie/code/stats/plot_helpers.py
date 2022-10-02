import numpy as np


def crop_zeroes(*vectors):
	begin_of_zeroes = [np.max(np.where(vector)) for vector in vectors]
	begin_of_zeroes = max(begin_of_zeroes)
	vectors = [vector[0:begin_of_zeroes] for vector in vectors]
	if len(vectors) == 1:
		return vectors[0]
	else:
		return vectors

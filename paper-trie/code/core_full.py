import numpy as np
from bio import Segment, Genome, Pos
from mutate_full import mutate_letter
from read_full import read_letter

L = 4


def generate_read():
	# generate genome
	g = Genome('ACCGT')
	i = 25 # np.random.randint(0, len(g) - L + 1)
	# start from empty read
	read = Segment('')

	while len(read) < L:
		letter = g[i]
		# mutate genome
		action, letter = mutate_letter(letter)
		read.mutations += [(Pos(g, i), action, letter)]
		if action != 'del':
			# read letter
			action, letter = read_letter(letter)
			read.errors += [(Pos(g, i), action, letter)]
			# append letter to read
			read += letter
		if action != 'ins':
			i += 1
	return read
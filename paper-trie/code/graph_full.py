from bio import Segment
from graph import Graph
from mutate_full import mutate_letter
from read_full import read_letter

L = 4


def generate_read(g: Graph):
	v = g.start
	read = Segment('')

	while len(read) < L:
		# generate genome
		edge = g.pick_edge(v)
		# mutate genome
		action, letter = mutate_letter(edge.letter)
		read.mutations += [(edge, action, letter)]
		if action != 'del':
			# read letter
			action, letter = read_letter(letter)
			read.errors += [(edge, action, letter)]
			# append letter to read
			read += letter
		if action != 'ins':
			v = edge.t
	return read
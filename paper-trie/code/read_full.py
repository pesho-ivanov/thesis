from utilities import select_action
from bio import Segment, letters, Pos

p_error = 0.1

def read_letter(letter):
	"""
	:param letter
	:return: (read/error, new letter)
	"""
	actions = [(1 - p_error, 'read', letter)] + \
			  [(p_error / 3, 'error', l) for l in letters if l != letter]
	return select_action(actions)

def read_segment(seg: Segment):
	"""
	:param seg: the segment to be read
	:param p_error: error probability
	:return: the resulting read
	"""
	for i in range(len(seg)):
		action, letter = read_letter(seg[i])
		seg.errors += [(Pos(seg, i), action, letter)]
		seg[i] = letter
	return seg

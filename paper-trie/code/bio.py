from typing import List, Tuple

letters = {'A','C','G','T'}


class Genome:
	"""
	Convenient representation of genomes
	"""

	def __init__(self, s: str):
		self.s = s
		# if genome is being mutated, this list contains its mutation history
		self.mutations: List[Tuple[Pos, str, str]] = []

	def __len__(self):
		return len(self.s)

	def __getitem__(self, offset):
		"""
		Overload array indexing, as in `genome[i]`
		:param offset: 0-based
		:return: the item-th letter in the genome
		"""
		return self.s[offset]

	def __setitem__(self, offset, letter):
		"""
		Overload assignment to array elements, as in `genome[i] = 'A'`
		:param offset: 0-based
		:param letter: the new letter
		:return: the updated genome
		"""
		s = list(self.s)
		s[offset] = letter
		self.s = "".join(s)

	def __iadd__(self, letter):
		"""
		Overload append, as in `genome += 'A'`
		:param letter:
		:return:
		"""
		self.s += letter
		return self

	def __repr__(self):
		"""Representation of genome"""
		return 'Genome: {}\nMutations: {}'.format(self.s, self.mutations)

	def get_segment(self, start, L):
		s = Segment(self[start:start+L])
		# determine the origin of every letter in this segment
		letters_origin = [(i, m) for i, m in enumerate(self.mutations)
						  if m[1] != 'del']
		m_start = letters_origin[start][0]
		m_end = letters_origin[start+L-1][0] # determine index of last produced letter
		s.mutations = self.mutations[m_start:m_end+1]
		return s


class Segment(Genome):
	"""
	Convenient representation of segments.
	Supports the same operations as a genome
	"""

	def __init__(self, s: str):
		super().__init__(s)
		# if segment is being read, this list contains its mutation history
		self.errors = []

	def __repr__(self):
		"""Representation of segment"""
		return 'Segment: {}\nMutations: {}\nRead Errors: {}'.format(self.s, self.mutations, self.errors)


class Pos:

	def __init__(self, g: Genome, index: int):
		"""
		:param g:
		:param index:
		:return: a position referring to the index-th letter of g
		"""
		self.g = g
		self.index = index

	def __repr__(self):
		"""Representation of position"""
		return repr('{}⟦{}⟧'.format(self.g.s, self.index))

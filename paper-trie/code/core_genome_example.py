import numpy as np
from bio import Genome
from mutate_full import mutate
from read_full import read_segment
from cut_full import cut


def generate(L=4):

	g = Genome('ATCGAA')
	print('Original genome:\n' + str(g))
	# Possible output:
	#
	# Original genome:
	# Genome: ATCGAA
	# Mutations: []

	##########
	# MUTATE #
	##########

	g_mut = mutate(g)
	print('\nMutated genome:\n' + str(g_mut))
	# Possible output:
	#
	# Mutated genome:
	# Genome: CTAGCA
	# Mutations: [('ATCGAA⟦0⟧', 'edit', 'C'), ('ATCGAA⟦1⟧', 'copy', 'T'), ('ATCGAA⟦2⟧', 'del', '-'),
	#             ('ATCGAA⟦3⟧', 'ins', 'A'), ('ATCGAA⟦3⟧', 'copy', 'G'), ('ATCGAA⟦4⟧', 'edit', 'C'),
	#             ('ATCGAA⟦5⟧', 'copy', 'A')]

	########
	# READ #
	########

	seg = cut(g_mut, L)
	print('\nCut segment:\n' + str(seg))
	# Possible output:
	#
	# Cut segment:
	# Segment: TAGC
	# Mutations: [('ATCGAA⟦1⟧', 'copy', 'T'), ('ATCGAA⟦2⟧', 'del', '-'), ('ATCGAA⟦3⟧', 'ins', 'A'),
	# 			('ATCGAA⟦3⟧', 'copy', 'G'), ('ATCGAA⟦4⟧', 'edit', 'C')]
	# Read Errors: []

	read = read_segment(seg)
	print('\nRead segment:\n' + str(read))
	# Possible output:
	#
	# Read segment:
	# Segment: TCGC
	# Mutations: [('ATCGAA⟦1⟧', 'copy', 'T'), ('ATCGAA⟦2⟧', 'del', '-'), ('ATCGAA⟦3⟧', 'ins', 'A'),
	# 			('ATCGAA⟦3⟧', 'copy', 'G'), ('ATCGAA⟦4⟧', 'edit', 'C')]
	# Read Errors: [('TCGC⟦0⟧', 'read', 'T'), ('TCGC⟦1⟧', 'error', 'C'), ('TCGC⟦2⟧', 'read', 'G'),
	#               ('TCGC⟦3⟧', 'read', 'C')]

	return read


# set interesting random seed; ensure reproducibility
np.random.seed(19)

read = generate()
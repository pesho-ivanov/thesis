from utilities import select_action
from bio import letters, Genome, Pos

epsilon = '-'

p_copy = 0.7; p_ed = 0.1; p_ins = 0.1; p_del = 0.1
# p_copy = 0.2; p_ed = 0.1; p_ins = 0.6; p_del = 0.1

def mutate_letter(letter):
	"""
	:param letter
	:return: (edit/ins/del/copy, new letter)
	"""
	actions = [(p_copy, 'copy', letter)] \
		+ [(p_ed/3, 'edit', l) for l in letters if l != letter] \
		+ [(p_ins/4, 'ins', l) for l in letters] \
		+ [(p_del, 'del', epsilon)]
	return select_action(actions)

def mutate(g_core: Genome):
	"""
	:param g_core: the genome to be mutated
	:return: the mutated genome and its generation history
	"""
	g_mut = Genome('') # start from empty genome
	i = 0
	while i < len(g_core):
		action, letter = mutate_letter(g_core[i])
		# record the mutations
		g_mut.mutations += [(Pos(g_core, i), action, letter)]
		if action != 'del':
			g_mut += letter # append letter to genome
		if action != 'ins':
			i += 1
	return g_mut

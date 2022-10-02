def read_letter(letter):
	actions = [(1 - p_error, 'read', letter)] + \
	          [(p_error / 3, 'error', l) for l in letters if l != letter]
	return select_action(actions)

def read_segment($\scriptstyle\segment$: Segment):
	for i in range(|$\scriptstyle\segment$|):
		action, letter = read_letter($\scriptstyle\segment$[i])
		$\scriptstyle\segment$.errors += [(Pos($\scriptstyle\segment$, i), action, letter)]@\label{line:read-history}@
		$\scriptstyle\segment$[i] = letter
	return $\scriptstyle\segment$@\label{line:read-return}@
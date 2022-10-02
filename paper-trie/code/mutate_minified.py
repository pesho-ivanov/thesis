def mutate_letter(letter):
	actions = [(p_ed / 3, 'edit', l) for l in letters if l != letter] + \@\label{line:mutate-actions-def}@
			  [(p_ins / 4, 'ins', l) for l in letters] + \
			  [(p_del, 'del', $\epsilon$)] + \
			  [(p_copy, 'copy', letter)]
	return select_action(actions)@\label{line:mutate-actions-select}@

def mutate($\scriptstyle\genome^\gcore$: Genome):
	$\scriptstyle\genome ^\gmut$ = Genome('') # start from empty genome
	i = 0
	while i < |$\scriptstyle\genome^\gcore$|:
		action, letter = mutate_letter($\scriptstyle\genome^\gcore$[i])
		# record the mutations
		$\scriptstyle\genome ^\gmut$.mutations += [(Pos($\scriptstyle\genome^\gcore$, i), action, letter)]@\label{line:mutate-history}@
		if action != 'del':@\label{line:mutate-del-check}@
			$\scriptstyle\genome ^\gmut$ += letter # append letter to genome@\label{line:mutate-no-del}@
		if action != 'ins':@\label{line:mutate-ins-check}@
			i += 1@\label{line:mutate-no-ins}@
	return $\scriptstyle\genome ^\gmut$@\label{line:mutate-return}@

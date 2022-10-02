def generate_read($\graph$: Graph):
	v = $\graph$.start
	$\scriptstyle\segment^\gread$ = Segment('')@\label{line:empty}@

	while len($\scriptstyle\segment^\gread$) < L:@\label{line:loop}@
		# generate genome
		edge = $\graph$.pick_edge(v)@\label{line:edge}@
		# mutate genome
		action, letter = mutate_letter(edge.letter)@\label{line:mutate}@
		$\scriptstyle\segment ^\gread$.mutations += [(edge, action, letter)]@\label{line:record}@
		if action != 'del':
			# read letter
			action, letter = read_letter(letter)@\label{line:read}@
			$\scriptstyle\segment ^\gread$.errors += [(edge, action, letter)]
			# append letter to read
			$\scriptstyle\segment ^\gread$ += letter
		if action != 'ins':
			v = edge.t@\label{line:new-state}@
	return $\scriptstyle\segment^\gread$

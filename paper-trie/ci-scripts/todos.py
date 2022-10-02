import os
import sys
from helpers import eprint, eprint_lines, paper_path, final_checks_file

default_log_file = os.path.join(paper_path, 'ci-output/latexmk/main.log')


def check(log_file=default_log_file):
	with open(log_file, 'r') as f:
		todos = []
		for line in f:
			if "TODO on page" in line:
				todos.append(line)

	n_todos = len(todos)
	if n_todos > 0:
		eprint('\n[ERROR]: ', n_todos, 'todos:')
		eprint_lines(todos)
		eprint('[SOLUTION]:')
		solutions = [
			'1) Remove the listed TODOs',
			'2) Disable the check for todos by editing {}.'.format(final_checks_file)
		]
		eprint_lines(solutions, '> ')
		return False

	return True


if __name__ == "__main__":
	ok = check()
	if not ok:
		sys.exit(1)

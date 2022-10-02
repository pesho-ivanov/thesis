import os
import re
import sys
from helpers import eprint, eprint_lines, paper_path, dir_path, get_short_filename, get_list, checks_file

default_log_file = os.path.join(paper_path, 'ci-output/main-short.log')

# acceptable warnings
acceptable_warnings_file = os.path.join(dir_path, 'acceptable_warnings_list.txt')
acceptable_warnings = get_list(acceptable_warnings_file)


def extract_string_between(s, start, end):
	query = start + '([\s\S]*)' + end
	result = re.search(query, s)
	return result.group(1)


def check(log_file=default_log_file):
	warnings_list = []

	with open(log_file, 'r') as f:
		log = f.read()
		warnings = re.sub('Result: o\) Errors: [0-9]*, Warnings: [0-9]*, BadBoxes: [0-9]*', '', log)
		split = warnings.split('** ')
		for s in split:
			s = s.strip()
			lines = s.split('\n')
			lines = [l.strip() for l in lines]
			s = '  '.join(lines)
			if s != '':
				if not any(a in s for a in acceptable_warnings):
					warnings_list.append(s)

	n_warnings = len(warnings_list)
	if n_warnings > 0:
		eprint('\n[ERROR]:', n_warnings, 'warnings:')
		eprint_lines(warnings_list, '> ')
		eprint('[SOLUTION]:')
		solutions = [
			'1) Fix the issues raised by the warnings.',
			'2) Add listed warnings to {}.'.format(get_short_filename(acceptable_warnings_file)),
			'3) Disable the check for warnings by editing {}.'.format(checks_file)
		]
		eprint_lines(solutions, '> ')
		return False

	return True


if __name__ == "__main__":
	ok = check()
	if not ok:
		sys.exit(1)


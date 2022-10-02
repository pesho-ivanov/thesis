import os
import sys
import argparse
from helpers import paper_path, dir_path, eprint, eprint_lines, final_checks_file

default_log_file = os.path.join(paper_path, 'ci-output/latexmk/main.log')
default_page_limit = 1


def get_page(log_file, label):
	with open(log_file, 'r', encoding='iso-8859-1') as f:
		for line in f:
			if label in line:
				page = int(line.split()[1])
	return page


def get_last_body_page(log_file):
	return get_page(log_file, 'LASTBODYPAGE')


def get_last_references_page(log_file):
	return get_page(log_file, 'LASTREFERENCESPAGE')


def get_last_page(log_file):
	return get_page(log_file, 'LASTPAGE')


def check(page_limit=default_page_limit, log_file=default_log_file):
	n_pages = get_last_body_page(log_file)
	if n_pages > page_limit:
		eprint('\n[ERROR]: Number of pages ({}) exceeds pagelimit ({}): '.format(n_pages, page_limit))
		eprint('[SOLUTION]:')
		solutions = [
			'1) Increase pagelimit in {}.'.format(os.path.join(dir_path, 'pagelimit.py')),
			'2) Disable the pagelimit check by editing {}.'.format(final_checks_file)
		]
		eprint_lines(solutions, '> ')
		return False
	return True


if __name__ == "__main__":
	# parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--log-file', type=str, default=default_log_file)
	options = ['lastbodypage', 'lastreferencespage', 'lastpage', 'check']
	parser.add_argument('--action', nargs='?', type=str, default='check', choices=options)
	parser.add_argument('--page_limit', type=int, default=default_page_limit)
	args = parser.parse_args()
	# run
	if args.action == 'lastbodypage':
		print(get_last_body_page(args.log_file))
	elif args.action == 'lastreferencespage':
		print(get_last_references_page(args.log_file))
	elif args.action == 'lastpage':
		print(get_last_page(args.log_file))
	elif args.action == 'check':
		ok = check(args.page_limit)
		if not ok:
			sys.exit(1)

from __future__ import print_function
import sys
import os
import glob


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


def eprint_lines(lines, prefix=''):
	for l in lines:
		eprint(prefix + l)


dir_path = os.path.dirname(os.path.realpath(__file__))
paper_path = os.path.join(dir_path, '..')
paper_path = os.path.abspath(paper_path)
root = os.path.join(paper_path, '..')
root = os.path.abspath(root)


def get_short_filename(filename):
	return os.path.relpath(filename, root)


def get_list(filename):
	with open(filename, 'r') as f:
		lines = f.read().splitlines()
		lines = [l for l in lines if not l.startswith('#')]
		return lines


checks_file = os.path.join(dir_path, 'checks.py')
checks_file = get_short_filename(checks_file)
final_checks_file = os.path.join(dir_path, 'final_checks.py')
final_checks_file = get_short_filename(final_checks_file)

ci_output_dir = os.path.join(paper_path, 'ci-output')
header_file = os.path.join(paper_path, 'header.tex')
__tex_pattern = os.path.join(paper_path, '**/*.tex')


# a generator iterating over all lines of *.tex files (except header.tex)
# returns pairs (filename, linenum, linetext)
def iterate_nonheader_tex_lines():
    for filename in glob.glob(__tex_pattern, recursive=True):
        if not filename.startswith(ci_output_dir) and not filename == header_file:
            with open(filename, 'r', encoding="utf-8") as file:
                for i, line in enumerate(file):
                    yield (filename, i, line)

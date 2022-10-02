# Some publishers object to Type 3 fonts. This script checks if the generated PDF contains any Type 3 fonts

import os
import sys
from subprocess import check_output, CalledProcessError
from helpers import eprint, eprint_lines, paper_path, checks_file

default_pdf = os.path.join(paper_path, 'ci-output/main.pdf')
search_string = "Type 3"


def check(pdf=default_pdf):
	try:
		output = check_output(['pdffonts', pdf])
	except CalledProcessError as e:
		output = e.output
		output = output.decode('utf-8')
		eprint(output)
		return False

	output = output.decode('utf-8')
	lines = output.splitlines()

	header = lines[0:2]
	fonts = lines[2:]

	type3 = [f for f in fonts if search_string in f]
	n_type3 = len(type3)

	if n_type3 > 0:
		eprint('\n[ERROR]:', n_type3, '"Type 3" fonts:')
		eprint_lines(header, '> ')
		eprint_lines(type3, '> ')
		eprint('[SOLUTION]:')
		solutions = [
			'1) Discussion: https://tex.stackexchange.com/questions/18687/how-to-generate-pdf-without-any-type3-fonts',
			'2) Most likely problem: The paper contains figures drawn using matplotlib. ' +
			'In this case, add this to the code that generate the figures: ' +
			"plt.rc('text', usetex=True); plt.rc('font', family='serif'); plt.rc('font', size=17)",
			'3) Disable the check for Type 3 fonts by editing {}.'.format(checks_file)
		]
		eprint_lines(solutions, '> ')
		return False

	return True


if __name__ == "__main__":
	output = check_output(['pdffonts', default_pdf])
	ok = check()
	if not ok:
		sys.exit(1)

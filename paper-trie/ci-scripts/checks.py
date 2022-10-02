import sys

from fonts import check as check_fonts
from compiler_warnings import check as check_warnings
from linting import check as check_linting


ok_fonts = check_fonts()
ok_warnings = check_warnings()
ok_linting = check_linting()

oks = [ok_fonts, ok_warnings, ok_linting]

if not all(oks):
	sys.exit(1)

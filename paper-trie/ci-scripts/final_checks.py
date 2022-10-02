import sys

from todos import check as check_todos
from pages import check as check_page_limit


ok_todos = check_todos()
ok_page_limit = check_page_limit()

oks = [ok_todos, ok_page_limit]
if not all(oks):
	sys.exit(1)

from re import search
from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model

search = Cmd2ArgumentParser(prog="search", usage="search the index")


search.add_argument(
    '-t',
	'--tags',
	nargs='+',
    dest='tags',
	default=[],
	help="tags you want to search for."
)

search.add_argument(
    '-w',
	'--terms',
	nargs='+',
    dest='terms',
	default=[],
	help="Terms you want to search for."
)

search.add_argument(
    '-s',
	'--sources',
	nargs='+',
    dest='sources',
	default=[],
	help="sources you want to search for."
)

search.add_argument(
    '-p',
	'--path',
    type=str,
    dest='path',
	default='',
	help="Path"
)

search.add_argument(
    '-a',
    dest="all",
	help="shows all entries",
    action="store_true"
)

@with_argparser(search)
def main(self, opts):
    tags = opts.tags
    terms = opts.terms
    sources = opts.sources
    path = opts.path
    show_all = opts.all
    print(path)

    if not show_all:
        view.printSearch(tags=tags, terms=terms, sources=sources, path=path)
    else:
        view.printAllEntries()


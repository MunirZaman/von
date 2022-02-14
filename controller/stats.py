from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model

stats = Cmd2ArgumentParser(usage="show statistics")
stats.add_argument("-t", nargs="+", dest="tags", default=[], type=str)
stats.add_argument("-w", nargs="+", dest="terms", default=[], type=str)

# improve
@with_argparser(stats)
def main(self, opts):
    view.printLevel()
    if len(opts.tags) > 0:
        view.printStatsTags(opts.tags)
    if len(opts.terms) > 0:
        view.printStatsTerms(opts.terms)


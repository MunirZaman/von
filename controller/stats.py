from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model

stats = Cmd2ArgumentParser(usage="show statistics")

# improve
@with_argparser(stats)
def main(self, opts):
    view.printLevel()
    #view.printSearch()

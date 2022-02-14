from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model

add = Cmd2ArgumentParser(prog="add", usage="adds a new file/problem to index")

add.add_argument("paths", nargs="+", default=[], help="paths")

@with_argparser(add)
def main(self, opts):
    paths = opts.paths
    for path in paths:
        prob = model.makeProblemFromPath(path)
        model.addProblemToIndex(prob)
        view.log(f"{prob} added to index")

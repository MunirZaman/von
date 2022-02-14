from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model

index = Cmd2ArgumentParser(prog="index", usage="rebuilds the index")

@with_argparser(index)
def main(self, opts):
    model.rebuildIndex()
    view.success("Successfully rebuilt index.")

from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model, tex

latex = Cmd2ArgumentParser(prog="latex", usage="latex")
latex.add_argument('label')

@with_argparser(latex)
def main(self, opts):
    entry = model.VonIndex()[opts.label]
    fn = tex.makeTeX(entry)
    print(fn)
    tex.compileTeX(fn)
    tex.cleanTeX()


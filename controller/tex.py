from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model, tex

latex = Cmd2ArgumentParser(prog="latex", usage="latex")

latex.add_argument('-l', nargs=1, default=[], type=str, dest="label")
latex.add_argument('-a', nargs=1, default=[], type=str, dest="folder")
latex.add_argument('-p', '--pdf', dest="pdf", action='store_true')

@with_argparser(latex)
def main(self, opts):
    if len(opts.folder) == 1:
        tex.makeTeXAll(opts.folder[0], compile=opts.pdf)

    elif len(opts.label) == 1:
        entry = model.VonIndex()[opts.label[0]]
        fn = tex.makeTeX(entry)
        if opts.pdf:
            tex.compileTeX(fn)
            tex.cleanTeX()


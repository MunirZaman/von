import os
import subprocess
import pathlib

from . import model

LATEXMK = ['latexmk', '-pdflatex']
LATEXMK_CLEAN = ['latexmk', '-c']

TEX = \
"""\\documentclass[11pt,numbers=noenddot,svgnames,dvipsnames]{scrartcl}
\\usepackage[top=1in, left=1in, right=1in, bottom=1in]{geometry}
\\usepackage{munir}

\\begin{document}
\\begin{problem*}
@problem
\\end{problem*}
\\begin{sol}
@solution
\\end{sol}
\\end{document}
"""


def compileTeX(path, opts = []):
    subprocess.call([*LATEXMK, *opts, path])
    parent = pathlib.PurePath(path).parent
    filename = pathlib.PurePath(path).name.replace('.tex', '.pdf')
    os.system(filename)

def getTeXsrc(obj):
    if isinstance(obj, model.Problem):
        state = obj.state
        solve = obj.bodies[1]

        src = TEX
        src = src.replace("@problem", state)
        src = src.replace("@solution", solve)
        return src
    elif isinstance(obj, model.IndexEntry):
        obj = obj.full
        return getTeXsrc(obj)
    else:
        raise Warning("could not generate TeX src.")
        return None


def makeTeX(obj):
    src = getTeXsrc(obj)
    if src is None:
        return None

    if isinstance(obj, model.Problem):
        fn =  obj.label.replace(" ",  "-").replace("/", "-") + ".tex"
    elif isinstance(obj, model.IndexEntry):
        obj = obj.full
        fn =  obj.label.replace(" ",  "-").replace("/", "-") + ".tex"

    try:
        with open(fn, 'x') as f:
            f.write(src)
    
    except FileExistsError:
        with open(fn, 'w') as f:
            f.write(src)

    return fn

def cleanTeX():
    subprocess.call([*LATEXMK_CLEAN])

    
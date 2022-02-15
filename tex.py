import os
import subprocess
import pathlib

from . import model
from . import view

LATEXMK = ['latexmk', '-pdflatex']
LATEXMK_CLEAN = ['latexmk', '-c']

TEX = \
"""\\documentclass[11pt,numbers=noenddot,svgnames,dvipsnames]{scrartcl}
\\usepackage[top=1in, left=1in, right=1in, bottom=1in]{geometry}
\\usepackage[asy]{munir}

\\begin{document}
\\begin{problem*}
@problem
\\end{problem*}
\\begin{sol}
@solution
\\end{sol}
\\end{document}
"""


def compileTeX(path, opts = [], stdout = subprocess.STDOUT):
    subrun = subprocess.run([*LATEXMK, *opts, path], stdout = stdout)
    parent = pathlib.PurePath(path).parent
    filename = pathlib.PurePath(path).name.replace('.tex', '.pdf')
    #os.system(filename)

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
        #fn =  obj.label.replace(" ",  "-").replace("/", "-") + ".tex"
        fn = pathlib.PurePath(model.completePath(obj.path)).name
        # should i use label as file name?
    elif isinstance(obj, model.IndexEntry):
        obj = obj.full
        #fn =  obj.label.replace(" ",  "-").replace("/", "-") + ".tex"
        fn = pathlib.PurePath(model.completePath(obj.path)).name

    try:
        with open(fn, 'x') as f:
            f.write(src)
    
    except FileExistsError:
        with open(fn, 'w') as f:
            f.write(src)

    return fn

def cleanTeX():
    subprocess.call([*LATEXMK_CLEAN])

    
def makeTeXAll(folder, compile=True):
    cwd = os.getcwd()
    if compile:
        view.warn("This might take a long time.")

    for entry in model.VonIndex().values():
        path = model.completePath(entry.path)
        purepath = pathlib.PurePath(path)
        parent = purepath.parent
        fname = purepath.name

        #create directory
        short_parent = model.shortenPath(parent)
        new_parent = os.path.join(folder, short_parent)
        try:
            os.makedirs(new_parent)
        except FileExistsError:
            pass
        
        # write problems to files
        new_path = os.path.join(folder, short_parent, fname)
        texsrc = getTeXsrc(entry)

        try:
            with open(new_path, 'x') as file:
                file.write(texsrc)
        except FileExistsError:
            with open(new_path, 'w') as file:
                file.write(texsrc)            

        if compile:
            os.chdir(new_parent)
            os.system(' '.join([*LATEXMK, fname]))
            os.system(' '.join(LATEXMK_CLEAN))
            os.chdir(cwd)
            view.log(f"Successfully compiled {new_path}")

    os.chdir(cwd)



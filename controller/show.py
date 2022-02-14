from cmd2 import Cmd2ArgumentParser, with_argparser
from matplotlib.pyplot import show
from .. import view, model

show = Cmd2ArgumentParser(prog="show", usage="show an entry from index")

show.add_argument("label", type=str) # label of the problem
show.add_argument("-p", action="store_true") # show the problem
show.add_argument("-s", action="store_true") # show the problem and solution

# HACK! IMPROVE THIS!
@with_argparser(show)
def main(self, opts):
    label = opts.label
    if label in model.VonIndex():
        entry = model.VonIndex()[label]
        problem = entry.full
        if opts.p:
            if opts.s:
                view.printProblem(problem, show=True)
            else:
                view.printProblem(problem, show=False)
        else:
            view.printEntry(entry)
    
    #TODO: IMPROVE
    elif label=='all':
        for l in model.VonIndex():
            view.printEntry(model.VonIndex()[l])

    elif label.isnumeric():
        for l in list(model.VonIndex())[-int(label):]:
            view.printEntry(model.VonIndex()[l])        
    else:
        view.error(f"{label} not found in index")


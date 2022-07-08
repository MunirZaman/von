from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model

show = Cmd2ArgumentParser(prog="show", usage="show an entry from index")

show.add_argument("-l", type=str, dest='label', nargs=1, default=[], help="label/source of the problem to show") # label of the problem
show.add_argument("-p", action="store_true", help="show the problem only") # show the problem
show.add_argument("-s", action="store_true", help="show the problem with solution") # show the problem and solution
show.add_argument("-a", action="store_true", help="show all problems") # shows all problems

@with_argparser(show)
def main(self, opts):

    if not opts.a and len(opts.label) == 1:
        label = opts.label[0]
        if label in model.VonIndex():
            entry = model.VonIndex()[label]
            problem = entry.full

            if opts.s:
                view.printProblem(problem, show=True)
            elif opts.p:
                view.printProblem(problem, show=False)
            else:
                view.printEntry(entry)
        
        elif label.isnumeric():
            # if label is a numeric value, say n
            # then show the last n problems in index
            for l in list(model.VonIndex())[-int(label):]:
                entry = model.VonIndex()[l]
                problem = entry.full

                if opts.s:
                    view.printProblem(problem, show=True)
                elif opts.p:
                    view.printProblem(problem, show=False)
                else:
                    view.printEntry(entry)        
        else:
            view.error(f"{label} not found in index")
    
    elif opts.a:
        for l in list(model.VonIndex()):
            entry = model.VonIndex()[l]
            problem = entry.full

            if opts.s:
                view.printProblem(problem, show=True)
            elif opts.p:
                view.printProblem(problem, show=False)
            else:
                view.printEntry(entry)      


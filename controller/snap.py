from cmd2 import Cmd2ArgumentParser, with_argparser
from .. import view, model, snapshot

snap = Cmd2ArgumentParser(prog="snap", usage="Snapshot")

snap.add_argument('-m', '--make', action="store_true", dest="make", help='Take a snapshot')
snap.add_argument('-d', '--diff', action="store_true", dest="diff", help="Diff Snapshot")
snap.add_argument('-i', '--index', action="store_true", dest="index", help="Update Index")

@with_argparser(snap)
def main(self, opts):
    if opts.make:
        snapshot.makeSnapshot()
    
    if opts.diff:
        view.printDiff(snapshot.diffSnapshot())

    if opts.index:
        view.out("Building Index...", style="green")
        snapshot.updateIndexFromDiff()
        view.success("Successfully built index.")

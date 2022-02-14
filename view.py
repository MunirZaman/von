import rich
import rich.console
import rich.traceback as traceback
from rich import print # overwrite print function
from rich.panel import Panel

from . import model
from . import rc

PROBLEM_HARDNESS = rc.PROBLEM_HARDNESS

traceback.install()

console = rich.console.Console()
error_console = rich.console.Console(stderr=True)

def error(msg):
    error_console.print("Error: "+ msg, style="bold red")

def warn(msg):
    error_console.print("Warning: "+ msg, style="bold yellow")

def out(message, *args, **kwargs):
	console.print(message, *args, **kwargs)

def getEntryString(entry: model.IndexEntry):
    s = ""
    label = entry.label
    label_string = f"[bold red]{label}[/bold red]"

    if hasattr(entry, 'tags') and type(entry.tags) == list:
        if ('fav' in entry.tags or 'favourite' in entry.tags) and rc.TERM_EMOJI:
            label_string += " :two_hearts:"

    if hasattr(entry, 'hardness') and type(entry.hardness) == int and entry.hardness > 0:
        hard = entry.hardness
        level = None
        if hard >= PROBLEM_HARDNESS['brutal']:
            level = 4
        elif hard >= PROBLEM_HARDNESS['hard']:
            level = 3
        elif hard >= PROBLEM_HARDNESS['mid']:
            level = 2
        elif hard >= PROBLEM_HARDNESS['easy']:
            level = 1

        if rc.TERM_EMOJI:
            label_string += " " + ":crossed_swords:"*level

    s += label_string + "\n"
    #if entry.isFav:
    #    label_string += " :two_hearts:"
    if hasattr(entry, 'tags') and type(entry.tags) == list and not entry.tags == []:
        tags = entry.tags
        tags_string = f"[bold yellow]tags:[/bold yellow] " + f"[yellow]{str(tags)[1:-1]}[/yellow]"
        s += tags_string

    if hasattr(entry, 'desc'):
        desc = entry.desc[:70] + " ..."
        desc_string = f"\n[bold cyan]description:[/bold cyan]\n\n[cyan]" \
                      + "\n".join(["\t" + line for line in desc.splitlines()]) + "[/cyan]"
        s += desc_string

    path = entry.path
    path_string = f"\n\n[blue]{path}[/blue]"
    s += path_string

    return s

def printEntry(entry: model.IndexEntry, *args, **kwargs):
    out(Panel(getEntryString(entry)), *args, **kwargs)

def getProblemString(problem: model.Problem):
    s = getEntryString(problem.entry)
    state_string = f"[cyan]{problem.state}[/cyan]"
    solve_string = f"[cyan]{problem.bodies[1]}[/cyan]"

    return s, state_string, solve_string

def printProblem(problem: model.Problem, show=False, *args, **kwargs):
    s = getProblemString(problem)
    out(s[0])
    out("\n")
    out(Panel(s[1], title=f"[bold blue]{problem.entry.label}[/bold blue]", title_align="right"))
    if show:
        out(Panel(s[2], title="[bold blue]Solution[/bold blue]", title_align="right"))

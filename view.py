import rich
import rich.console
import rich.traceback as traceback
from rich import print # overwrite print function
from rich.panel import Panel
from rich.table import Table

from . import model
from . import rc
from . import stats

PROBLEM_HARDNESS = rc.PROBLEM_HARDNESS

traceback.install()

console = rich.console.Console()
error_console = rich.console.Console(stderr=True)

def log(msg, *args, **kwargs):
    console.log(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    if rc.TERM_EMOJI:
        error_console.print("❌ "+ msg, style="bold red", *args, **kwargs)
    else:
        error_console.print("Error: "+ msg, style="bold red", *args, **kwargs)

def warn(msg, *args, **kwargs):
    if rc.TERM_EMOJI:
        error_console.print("⚠ "+ msg, style="bold yellow", *args, **kwargs)
    else:
        error_console.print("Warning: "+ msg, style="bold yellow", *args, **kwargs)

def success(msg, *args, **kwargs):
    if rc.TERM_EMOJI:
        out("[bold green]✅ "+ msg, *args, **kwargs)
    else:
        out(msg, style="green", *args, **kwargs)

def out(message, *args, **kwargs):
	console.print(message, *args, **kwargs)


def getEntryString(entry: model.IndexEntry):
    s = ""
    label = entry.label
    label_string = f"[bold red]{label}[/]"

    if hasattr(entry, 'tags') and type(entry.tags) == list:
        if ('fav' in entry.tags or 'favourite' in entry.tags):
            if rc.TERM_EMOJI:
                label_string = f"[bold magenta]{label}[/]" + " 💖"
            else:
                label_string = f"[bold magenta]{label} <3[/]"

    if hasattr(entry, 'hardness') and type(entry.hardness) == int and entry.hardness > 0:
        hard = entry.hardness
        level = stats.getLevelFromHardness(hard)

        if rc.TERM_EMOJI:
            label_string += " " + "⚔"*level
        else:
            difficulty = ""
            if level == 1:
                difficulty = " [green]X[/]"
            elif level == 2:
                difficulty = " [yellow]XX[/]"
            elif level == 3:
                difficulty = " [blue]XXX[/]"
            elif level == 4:
                difficulty = " [red]XXXX[/]"
            else:
                difficulty = ""
            label_string += difficulty

    s += label_string + "\n"

    if hasattr(entry, 'tags') and type(entry.tags) == list and not entry.tags == []:
        tags = entry.tags
        tags_string = f"[bold yellow]tags:[/bold yellow] " + f"[yellow]{str(tags)[1:-1]}[/yellow]"
        s += tags_string

    if hasattr(entry, 'desc'):
        desc = entry.desc
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


LEVEL_DICT_EMOJI = \
{
    1: "[bold green]Noob[/] 👶",
    2: "[bold yellow]Intermediate[/] 🙂",
    3: "[bold red]Master[/] 👌😎",
    4: "[bold blue]GrandMaster[/] 💪😎"
}

LEVEL_DICT_TEXT = \
{
    1: "[bold green]Noob[/]",
    2: "[bold yellow]Intermediate[/]",
    3: "[bold red]Master[/]",
    4: "[bold blue]GrandMaster[/]"
}


def printLevel():
    level, avg = stats.getLevel()
    if rc.TERM_EMOJI:
        LEVEL_DICT = LEVEL_DICT_EMOJI
    else:
        LEVEL_DICT = LEVEL_DICT_TEXT
    s = f"[bold blue]Level:[/] {LEVEL_DICT[level]} {avg}\n"
    out(s)

def getSearchItem(entry: model.IndexEntry):
    label = entry.label
    tags = entry.tags
    diff = entry.hardness

    if 'fav' in tags or 'favourite' in tags:
        if rc.TERM_EMOJI:
            label_string = f"[bold magenta]{label}[/] 💖"
        else:
            label_string = f"[bold magenta]{label} <3[/]"
    else:
        label_string = f"[bold red]{label}[/]"

    tags_string = f"[yellow]{str(tags)[1:-1]}[/]"

    if rc.TERM_EMOJI:
        diff_string = "⚔"*stats.getLevelFromHardness(diff)
    else:
        diff_string = "X"*stats.getLevelFromHardness(diff)
        
    return [label_string, tags_string, diff_string]
    

def printSearch(*args, **kwargs):
    table = Table()
    table.add_column("Label", justify="center")
    table.add_column("Tags", justify="left")
    table.add_column("Difficulty", justify="center")

    results = model.runSearch(*args, **kwargs)
    for res in results:
        table.add_row(*getSearchItem(res))

    out(table)


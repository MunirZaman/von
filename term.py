import sys
import cmd2
from cmd2 import style

from . import rc
from . import model
from . import view

from .controller import (
    index,
    show,
    search,
    tex,
    add,
    stats
)

WELCOME_MESSAGE = style("Welcome to VON!\n", fg="red", bold=True, underline=True)
PROMPT = style("$> ", fg="green", bold=True)

class VonTerm(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT
        self.intro = WELCOME_MESSAGE
        self.debug = True

    def do_exit(self, *args):
        sys.exit()

    do_index = index.main
    do_show = show.main
    do_search = search.main
    do_tex = tex.main
    do_add = add.main
    do_stats = stats.main


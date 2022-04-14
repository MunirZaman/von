import os
import rich.box

SEPERATOR = "\n---\n"

VON_BASE_PATH = os.path.expanduser("~\\Documents\\von\\")
VON_INDEX_PATH = os.path.join(VON_BASE_PATH, "index")
VON_SNAPSHOT_PATH = os.path.join(VON_BASE_PATH, "snapshot")


PROBLEM_HARDNESS = {'easy': 0, 'mid': 5, 'hard': 10, 'brutal': 15}
TERM_EMOJI = True # use emojis in terminal

if TERM_EMOJI:
    RICH_BOX = rich.box.ROUNDED # default rich table box
else:
    RICH_BOX = rich.box.ASCII2 # ise ASCII2


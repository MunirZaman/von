from . import model
from . import rc

PROBLEM_HARDNESS = rc.PROBLEM_HARDNESS

def getLevel():
    """returns the avarage difficulty of problems"""
    diffs = [model.VonIndex()[label].hardness for label in list(model.VonIndex()) if model.VonIndex()[label].hardness > 0]
    
    avg = int(sum(diffs)/len(diffs))
    level = getLevelFromHardness(avg)

    return level, avg

def getLevelFromHardness(hardness: int):
    if hardness >= PROBLEM_HARDNESS['brutal']:
        level = 4
    elif hardness >= PROBLEM_HARDNESS['hard']:
        level = 3
    elif hardness >= PROBLEM_HARDNESS['mid']:
        level = 2
    elif hardness >= PROBLEM_HARDNESS['easy']:
        level = 1
    else:
        level = 0

    return level



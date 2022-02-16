from watchdog.utils import dirsnapshot

from . import rc
from . import model


class pickleSnapshot(model.pickleObj):
    def _initial(self):
        return None


def VonSnapshot(mode = 'rb'):
    return pickleSnapshot(rc.VON_SNAPSHOT_PATH, mode=mode)


def getSnapshot():
    snap = dirsnapshot.DirectorySnapshot(rc.VON_BASE_PATH)
    return snap

def makeSnapshot():
    with VonSnapshot(mode = 'wb') as snap:
        snap.store = getSnapshot()

def diffSnapshot():
    old_snapshot = VonSnapshot().store

    if old_snapshot is not None:
        new_snapshot = getSnapshot()
        diff_snapshot = dirsnapshot.DirectorySnapshotDiff(old_snapshot, new_snapshot)
        diff = \
        {
            'modified': [f for f in diff_snapshot.files_modified if f.endswith('.tex')],
            'created' : [f for f in diff_snapshot.files_created if f.endswith('.tex')],
            'deleted' : [f for f in diff_snapshot.files_deleted if f.endswith('.tex')],
            'moved': [f for f in diff_snapshot.files_moved if f[0].endswith('.tex')]
        }

        return diff
    
    else:
        diff = \
        {
            'modified': [],
            'created': [],
            'deleted': [],
            'moved': []
        }        
        return diff


def updateIndexFromDiff():
    diff = diffSnapshot()
    path_entry_dict = {}

    for created in diff["created"]:
        model.addProblemToIndex(model.makeProblemFromPath(model.shortenPath(created)))

    for deleted in diff["deleted"]:
        if path_entry_dict != {}: # if path_entry_dict is empty
            for e in model.VonIndex().values():
                path_entry_dict[e.path] = e

        if model.shortenPath(deleted) in path_entry_dict.keys():
            del model.VonIndex()[path_entry_dict[model.shortenPath(deleted)].label]

    for modified in diff['modified']:
        if modified not in diff['deleted'] and modified not in [m[0] for m in diff['moved']]:
            problem = model.makeProblemFromPath(model.shortenPath(modified))
            model.addProblemToIndex(problem)

    if len(diff['moved']) > 0: # in most cases we wont move files

        if path_entry_dict != {}: # if path_entry_dict is empty
            for e in model.VonIndex().values():
                path_entry_dict[e.path] = e

        for moved in diff['moved']:
            old = moved[0]
            new = moved[1]

            if model.shortenPath(old) in path_entry_dict.keys():
                del model.VonIndex()[path_entry_dict[model.shortenPath(old)].label]

            model.addProblemToIndex(model.makeProblemFromPath(model.shortenPath(new)))

    return diff


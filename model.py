import os
import collections
from statistics import mode
import yaml
import pickle
from .rc import SEPERATOR, VON_BASE_PATH, VON_INDEX_PATH

# Enter&Exit Methods: https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit

def shortenPath(path):
    return os.path.relpath(path, VON_BASE_PATH)

def completePath(path):
    return os.path.join(VON_BASE_PATH, path)

def vonOpen(path, *args, **kwargs):
    return open(completePath(path), *args, **kwargs)


class pickleObj:
    """Pickle Obj for storing stuff in files """

    def _initial(self):
        return None

    def __init__(self, path, mode='rb'):
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            # if the specified path is not a file or 
            # if the file is empty then set store to _initial.
            self.store = self._initial()
        else:
            # else set store = file data
            with vonOpen(path, 'rb') as f:
                self.store = pickle.load(f)
        self.path = path
        self.mode = mode

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        # rewrite everything if mode is 'wb'
        if self.mode == 'wb':
            with vonOpen(self.path, 'wb') as f:
                pickle.dump(self.store, f)

    def set(self, store):
        self.store = store


class pickleDict(pickleObj, collections.abc.MutableMapping):
    def _initial(self):
        return {}

    def __getitem__(self, key):
        try:
            return self.store[key]
        except IndexError:
            raise IndexError(f"{key} not a valid key")

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class pickleList(pickleObj, collections.abc.MutableSequence):
    def _initial(self):
        return []

    def __getitem__(self, key):
        try:
            return self.store[key]
        except IndexError:
            raise IndexError(f"{key} not a valid key")

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


def VonIndex(mode='rb'):
    return pickleDict(VON_INDEX_PATH, mode)

#def VonToday(mode='rb'):
#    return pickleList(VON_TODAY_PATH, mode)


class Problem:
    def __init__(self, path, **kwargs):
        self.label = None # identifier
        self.source = None
        self.desc = None # description 
        self.tags = []
        self.hardness = -1
        self.bodies = []
        self.path = path

        for key in kwargs:
            setattr(self, key, kwargs[key])

        if self.label is None:
            if not self.source is None:
                self.label = self.source
            else:
                raise AttributeError('label not defined.')
            
    @property
    def entry(self):
        return IndexEntry(
            label = self.label,
            source = self.source,
            desc = self.desc,
            tags = self.tags,
            hardness = self.hardness,
            path = self.path
        )

    @property
    def state(self):
        return self.bodies[0]

    def __repr__(self):
        return self.label


def makeProblemFromPath(path):
    # Creates a problem instance from a source, without looking at Index
    with vonOpen(path, 'r') as f:
        text = ''.join(f.readlines())
    x = text.split(SEPERATOR)
    data = yaml.safe_load(x[0])
    if data is None:
        return None
    data['bodies'] = [_.strip() for _ in x[1:]]
    return Problem(path, **data)

def addProblemByFileContents(path, text):
    with vonOpen(path, 'w') as f:
        print(text, file=f)
    print("Wrote to " + path)
    # Now update cache
    p = makeProblemFromPath(shortenPath(path))
    addProblemToIndex(p)
    return p

def getAllProblems():
    # Get's all problem from VON_BASE_PATH
    ret = []
    for root, _, filenames in os.walk(VON_BASE_PATH):
        for fname in filenames:
            if not fname.endswith('.tex'):
                continue
            path = shortenPath(os.path.join(root, fname))
            p = makeProblemFromPath(path)
            if p is not None:
                ret.append(p)
    return ret


class IndexEntry:
    def __init__(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])

    # search things
    def hasTag(self, tag):
        return tag.lower() in [_.lower() for _ in self.tags]

    def hasSource(self, source):
        return (source.lower() in self.source.lower()) if (not self.source is None) else False

    def hasTerm(self, term):
        blob = self.label
        if not self.source is None:
            blob += " " + self.source
        if hasattr(self, 'desc') and not self.desc is None:
            blob += " " + self.desc

        return (term.lower() in blob.lower() or self.hasTag(term))

    @property
    def full(self):
        return makeProblemFromPath(self.path)


def addEntryToIndex(entry):
    with VonIndex('wb') as index:
        index[entry.label] = entry

def addProblemToIndex(problem):
    with VonIndex('wb') as index:
        p = problem
        index[p.label] = p.entry
        #return index[p.source]

def setEntireIndex(d):
    with VonIndex('wb') as index:
        index.set(d)

def rebuildIndex():
    """rebuild index by reading VON_BASE_PATH """
    d = {}
    for p in getAllProblems():
        if p.source in d:
            pass # do smth
        d[p.label] = p.entry
    setEntireIndex(d)

def runSearch(
    terms=[], tags=[], sources=[], path='', alph_sort=False
):

    def _matches(entry):
        return (
            all([entry.hasTag(_) for _ in tags]) and all([entry.hasTerm(_) for _ in terms]) and
            all([entry.hasSource(_) for _ in sources]) and entry.path.startswith(path)
        )
        
    with VonIndex() as index:
        result = [entry for entry in index.values() if _matches(entry)]

    if alph_sort:
        result.sort(key=lambda e: e.label)
    else:
        result.sort(key=lambda e: e.hardness)

    return result


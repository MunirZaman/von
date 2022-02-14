from .term import VonTerm

if __name__ == '__main__':
    import sys
    c = VonTerm()
    sys.exit(c.cmdloop())

class Tick(object):
    h: float
    o: float
    l: float
    c: float
    v: float

    def __init__(self, entry):
        self.h = entry['h']
        self.o = entry['o']
        self.l = entry['l']
        self.c = entry['c']
        self.v = entry['v']

    def to_array(self):
        return self.h, self.o, self.l, self.c, self.v


import copy

class Atom:
    
    FRESH_COUNT = 0
    SYMBOLS = set()
        
    def __init__(self):
        pass
        
    @classmethod
    def fromElements(self, elements):
        Atom.SYMBOLS.add(elements[0])
        atom = Atom()
        atom.pred = elements[0]        
        if len(elements) > 1:
            # there are arguments
            atom.args = elements[1][1:-1]
        else:
            # empty arguments
            atom.args = []
        return atom
            
    @classmethod
    def fromString(cls, s):
        atom = Atom()
        if '(' in s:
            atom.pred = s[0:s.find('(')]
            atom.args = s[s.find('(')+1:-1].split(',')
        else:
            atom.pred = s
            atom.args = []
        return atom
    
    @classmethod    
    def freshWithArgs(cls, args):
        atom = Atom()
        atom.pred = Atom.freshPredSymbol()
        atom.args = copy.deepcopy(args)
        return atom
                
    def toDatalog(self, kind):
        atom = Atom()
        atom.pred = self.pred + '_' + kind
        atom.args = copy.deepcopy(self.args)
        return atom

    # return the variables that appear in the atom
    def vars(self):
        return {arg for arg in self.args if arg[0].isupper()}                        
        
    @classmethod    
    def freshPredSymbol(cls):
        Atom.FRESH_COUNT += 1
        return 'tmp' + str(Atom.FRESH_COUNT)
        
    def __str__(self):
        s = self.pred
        if len(self.args) > 0:
            s = s + '(' + ','.join(self.args) + ')'
        return s            
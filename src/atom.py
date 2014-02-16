import copy
from grammar import Grammar

class Atom:
    
    FRESH_COUNT = 0
    atoms = set()
       
    def __init__(self):
        pass
        
    @classmethod
    def fromElements(self, elements, add = True):
        atom = Atom()
        atom.pred = elements[0]        
        if len(elements) > 1:
            # there are arguments
            atom.args = elements[1][1:-1]
        else:
            # empty arguments
            atom.args = []
        if add:
            Atom.atoms.add(atom)
        return atom
            
    @classmethod
    def fromString(cls, s):
        return Atom.fromElements(Grammar.parseAtom(s))
    
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
    
    def isGround(self):
        return len(self.vars()) == 0                        
        
    @classmethod    
    def freshPredSymbol(cls):
        Atom.FRESH_COUNT += 1
        return 'tmp' + str(Atom.FRESH_COUNT)
        
    def __str__(self):
        s = self.pred
        if len(self.args) > 0:
            s = s + '(' + ','.join(self.args) + ')'
        return s            
import copy
from grammar import Grammar

class Atom:
    
    FRESH_COUNT = 0
    atoms = set()
    issuerMap = {}
       
    def __init__(self):
        self.issuer = None
        
    @classmethod
    def fromElements(self, elements, add = True):
        atom = Atom()
        atom.pred = elements[0]
        atom.args = []
        for l in elements[1:]:
            if l[0] == '@':
                # issuer argument
                #atom.args.insert(0,l[1])
                atom.issuer = l[1]
                # constant and variable arguments
            if l[0] == '(':
                atom.args = atom.args + l[1:-1]
        if add:
            Atom.atoms.add(atom.clone())
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
    
    def clone(self):
        c = Atom()
        c.pred = copy.deepcopy(self.pred)
        c.args = copy.deepcopy(self.args)
        c.issuer = copy.deepcopy(self.issuer) 
        return c

    def toDatalog(self, kind):
        atom = Atom()
        atom.pred = self.pred + '_' + kind
        atom.args = copy.deepcopy(self.args)
        return atom

    # return the variables that appear in the atom
    def getArgs(self):
        return self.args
    
    # return the variables that appear in the atom
    def getPreds(self):
        # atoms returns one positive atom and no negative atoms
        s = set()
        s.add(self.pred)
        return (s, set())
    
    def isGround(self):
        return len({x for x in self.args if x.isupper()}) == 0

    def inlineIssuer(self):
        if self.pred not in Atom.issuerMap.keys():
            return 
        if Atom.issuerMap[self.pred] == 'no':
            return
        if self.issuer == None:
            self.issuer = 'admin'
        if Atom.issuerMap[self.pred] == 'pred':
            self.pred = self.pred + '_' + self.issuer
        elif Atom.issuerMap[self.pred] == 'args':
            self.args.insert(0,self.issuer)
        self.issuer = None
            
        
    @classmethod
    def freshPredSymbol(cls):
        Atom.FRESH_COUNT += 1
        return 'tmp' + str(Atom.FRESH_COUNT)

    def __str__(self):
        s = self.pred
        if len(self.args) > 0:
            s = s + '(' + ','.join(self.args) + ')'
        if self.issuer is not None:
            s = s + '@' + self.issuer
        return s

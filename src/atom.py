import re

class AtomParseException(Exception):
    pass

class Atom:
    
    argRegExpr = re.compile("[a-zA-Z]\w*$")
    predRegExpr = re.compile("[a-zA-Z]\w*$")    
    atomRegExpr = re.compile("[a-zA-Z][a-zA-Z0-9]*(\([a-zA-Z]\w*(\,[a-zA-Z]\w*)*\))?$")
    
    def __init__(self):
        self.args = []
        
    @classmethod
    def fromString(cls, string):
        if Atom.atomRegExpr.match(string) is None:
            raise AtomParseException, 'Error parsing atom: ' + string
        atom = Atom()
        if '(' in string:
            atom.pred = string[:string.find('(')]
            atom.args = string[string.find('(')+1:-1].split(',')                
        else:
            atom.pred = string            
        atom.validate()
        return atom
            
            
    def validate(self):
        self.validateArgs()
        self.validatePred()
            
    def validateArgs(self):
        for arg in self.args:
            if Atom.argRegExpr.match(arg) is None:
                raise AtomParseException, 'Error parsing arguments in atom ' + str(self)
            
    def validatePred(self):
        if Atom.predRegExpr.match(self.pred) is None:
            raise AtomParseException, 'Error parsing predicate name of atom ' + str(self)
        
    def __str__(self):
        s = self.pred
        if len(self.args) > 0:
            s = s + '(' + ', '.join(self.args) + ')'
        return s            
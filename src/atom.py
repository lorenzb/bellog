import re

class AtomParseException(Exception):
    pass

class Atom:
    
    argRE = re.compile("[a-zA-Z]\w*$")
    predRE = re.compile("[a-zA-Z]\w*$")    
    atomRE = re.compile("[a-zA-Z][a-zA-Z0-9]*(\([a-zA-Z]\w*(\,[a-zA-Z]\w*)*\))?$")
    
    def __init__(self):
        self.args = []
        
    @classmethod
    def fromString(cls, string):
        if Atom.atomRE.match(string) is None:
            raise AtomParseException, 'Error parsing atom: ' + string
        atom = Atom()
        if '(' in string:
            atom.pred = string[:string.find('(')]
            atom.args = string[string.find('(')+1:-1].split(',')                
        else:
            atom.pred = string            
        atom.validate()
        return atom
    
    # return the variables that appear in the atom
    def vars(self):
        return {arg for arg in self.args if arg[0].isupper()}    
            
    def validate(self):
        self.validateArgs()
        self.validatePred()
            
    def validateArgs(self):
        for arg in self.args:
            if Atom.argRE.match(arg) is None:
                raise AtomParseException, 'Error parsing arguments in atom ' + str(self)
            
    def validatePred(self):
        if Atom.predRE.match(self.pred) is None:
            raise AtomParseException, 'Error parsing predicate name of atom ' + str(self)
        
    def toDatalog(self, kind):
        atom = Atom()
        atom.pred = self.pred + '_' + kind
        atom.args = []
        for arg in self.args:
            atom.args.append(arg)
        return atom
            
        
    def __str__(self):
        s = self.pred
        if len(self.args) > 0:
            s = s + '(' + ', '.join(self.args) + ')'
        return s            
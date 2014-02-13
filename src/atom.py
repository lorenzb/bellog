class Atom:
    
    FRESH_COUNT = 0
    
    def __init__(self, elements):
        self.pred = elements[0]        
        if len(elements) > 1:
            # there are arguments
            self.args = elements[1][1:-1:2]
        else:
            # empty arguments
            self.args = []
        
    # return the variables that appear in the atom
    def vars(self):
        return {arg for arg in self.args if arg[0].isupper()}                
        
    def toDatalog(self, kind):
        atom = Atom()
        atom.pred = self.pred + '_' + kind
        atom.args = []
        for arg in self.args:
            atom.args.append(arg)
        return atom
        
    @classmethod    
    def freshPredSymbol(cls):
        Atom.FRESH_COUNT += 1
        return 'tmp' + str(Atom.FRESH_COUNT)
        
    def __str__(self):
        s = self.pred
        if len(self.args) > 0:
            s = s + '(' + ','.join(self.args) + ')'
        return s            
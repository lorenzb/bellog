from rule import Rule
from grammar import Grammar
from atom import Atom

class Policy:
    
    def __init__(self):
        self.rules = []
    
    @classmethod
    def fromString(self, string):
        policy=Policy()
        elements = Grammar.parsePolicy(string)
        for ruleElements in elements:
            rule = Rule.fromElements(ruleElements)
            policy.rules.append(rule)
        policy.checkAtoms()
        return policy
            
            
    def checkAtoms(self):
        if len(Atom.SYMBOLS - {r.head.pred for r in self.rules}.union({'top', 'true', 'bot', 'false'})) > 0:
            raise Exception('The following predicate symbols have not been defined:' + ', '.join(Atom.SYMBOLS - {r.head.pred for r in self.rules}.union({'top', 'true', 'bot', 'false'})))
        
    def checkIfQueryArityMatches(self, atom):
        definedQueryArities = {len(r.head.args) for r in self.rules if r.head.pred == atom.pred}
        if len(definedQueryArities) != 1:
            raise Exception('Atoms with different arities defined for the same predicate symbol: ' + atom.pred)
        definedArity = definedQueryArities.pop()
        if definedArity != len(atom.args):
            raise Exception('Query arity mismatch. The arity of ' + str(atom) + ' in the given policy is ' + str(definedArity))
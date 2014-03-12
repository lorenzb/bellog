from rule import Rule
from grammar import Grammar
from atom import Atom
from graph import strongly_connected_components_path

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
            policy.postProcess()
        policy.checkAtomsWithIssuers()
        #policy.checkNoEdbAtoms()
        policy.checkIdbArities()        
        policy.checkStratified()
        policy.checkFreeVars()
        return policy
    
    def postProcess(self):
        self.preds = {a.pred for a in Atom.atoms}
        self.idbs = {r.head.pred for r in self.rules}
        if len(self.idbs.intersection({'top', 'true', 'bot', 'false'})) > 0:
            raise Exception('The predicates: ' + ', '.join({'top', 'true', 'bot', 'false'}.intersection(self.idbs)) + ' cannot appear in the rule heads')
        self.edbs = self.preds - self.idbs.union({'top', 'true', 'bot', 'false'})
        
    def checkAtomsWithIssuers(self):
        for p in self.idbs:
            issuers = {a.issuer for a in Atom.atoms if a.pred == p and a.issuer is not None}
            if len(issuers) == 0:
                Atom.issuerMap[p] = 'no'
            else:
                variablesUsedAsIssuers = len({x for x in issuers if x.isupper()}) > 0
                if variablesUsedAsIssuers:
                    Atom.issuerMap[p] = 'args'  
                else:
                    Atom.issuerMap[p] = 'pred'
                    self.idbs = self.idbs - {p}
                    self.idbs = self.idbs.union({p + '_' + x for x in issuers})
                    if {a for a in Atom.atoms if a.pred == p and a.issuer is None}:
                        self.idbs.add(p + '_admin')
        # processed all atoms, now we can inline all issuers in the atoms
        for r in self.rules:
            r.inlineIssuer()
        for a in Atom.atoms:
            a.inlineIssuer()
                    
    def checkNoEdbAtoms(self):
        if len(self.edbs) > 0:
            raise Exception('The following predicate symbols have not been defined: ' + ', '.join(self.edbs))
        
    def checkIdbArities(self):
        for pred in self.idbs:
            arities = {len(a.args) for a in Atom.atoms if a.pred == pred}
            if len(arities) != 1:
                raise Exception('The predicate symbol ' + pred + ' is used with multiple arities: ' + ','.join(map(str, arities)))
                    
    def checkQuery(self, atom):
        if not atom.isGround():
            raise Exception('The query ' + str(atom) + ' is not ground.')
        if atom.pred not in self.idbs.union({'false', 'bot', 'top', 'true'}):
            #raise Exception('The predicate ' + atom.pred + ' is not defined in the policy')
            self.edbs.add(atom.pred)
            return
        definedArity = {len(a.args) for a in Atom.atoms if a.pred == atom.pred}.pop()
        if definedArity != len(atom.args):
            raise Exception('Query arity mismatch. The arity of ' + str(atom) + ' in the given policy is ' + str(definedArity))
        
    def checkFreeVars(self):
        for r in self.rules:
            headFreeVars = {x for x in r.head.getArgs() if x.isupper()} - {x for x in r.body.getArgs() if x.isupper()}
            if headFreeVars:
                raise Exception('The head of rule ' + str(r) + ' contains the free variables: ' + ','.join(headFreeVars))
        
    def checkStratified(self):
        vertices = self.idbs.union(self.edbs).union({'false', 'bot' , 'top', 'true'})
        edges = {}
        posPreds = {}
        negPreds = {}
        for v in vertices:
            posPreds[v] = set()
            negPreds[v] = set()
            for r in {rule for rule in self.rules if rule.head.pred == v}:
                (pos, neg) = r.body.getPreds() 
                posPreds[v] = posPreds[v].union(pos)
                negPreds[v] = negPreds[v].union(neg)
        for v in vertices:
            edges[v] = list(posPreds[v].union(negPreds[v]))        
        for component in strongly_connected_components_path(vertices, edges):
            for v in component:
                if negPreds[v].intersection(set(component)):
                    raise Exception('The dependent predicates ' + str(map(str, component)) + ' cannot be stratified')

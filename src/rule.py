from atom import Atom
from query import Query

class Rule:
    
    def __init__(self):
        pass
    
    @classmethod
    def fromElements(self, elements):
        rule = Rule()
        rule.head = Atom.fromElements(elements[0])
        print elements[2]
        rule.body = Query.fromElements(elements[2])
        return rule
    
    def toDatalogRules(self):
        if self.body.operator == '':
            ruleTop = str(self.head.toDatalog('top')) + ' :- ' + str(self.body.subqueries[0].toDatalog('top'))
            ruleBot = str(self.head.toDatalog('bot')) + ' :- ' + str(self.body.subqueries[0].toDatalog('bot'))
            return [ruleTop, ruleBot]        
        elif self.body.operator == '!':
            freshAtom = Atom.freshWithArgs(self.body.vars())                             
            ruleTop = str(self.head.toDatalog('top')) + ' :- tnot(' + str(freshAtom.toDatalog('bot')) + ')'
            ruleBot = str(self.head.toDatalog('bot')) + ' :- tnot(' + str(freshAtom.toDatalog('top')) + ')'
            subqueryRule = Rule()
            subqueryRule.head = freshAtom
            subqueryRule.body = self.body.subqueries[0]             
            return [ruleTop, ruleBot] + subqueryRule.toDatalogRules()
        elif self.body.operator == '~':
            freshAtom = Atom.freshWithArgs(self.body.vars())                             
            ruleTop = str(self.head.toDatalog('top')) + ' :- ' + str(freshAtom.toDatalog('bot'))
            ruleBot = str(self.head.toDatalog('bot')) + ' :- ' + str(freshAtom.toDatalog('top'))
            subqueryRule = Rule()
            subqueryRule.head = freshAtom
            subqueryRule.body = self.body.subqueries[0]             
            return [ruleTop, ruleBot] + subqueryRule.toDatalogRules()
        elif self.body.operator == '^':
            freshAtoms = []
            datalogRules = []
            for subquery in self.body.subqueries:
                freshAtom = Atom.freshWithArgs(sorted(subquery.vars()))
                freshAtoms.append(freshAtom)
                newRule = Rule()
                newRule.head = freshAtom
                newRule.body = subquery
                datalogRules += newRule.toDatalogRules()
            ruleTop = str(self.head.toDatalog('top')) + ' :- ' + ','.join([str(x.toDatalog('top')) for x in freshAtoms])
            ruleBot = str(self.head.toDatalog('bot')) + ' :- ' + ','.join([str(x.toDatalog('bot')) for x in freshAtoms])    
            datalogRules += [ruleTop, ruleBot]
            return datalogRules        
                
    def __str__(self):
        return str(self.head) + ':-' + str(self.body)
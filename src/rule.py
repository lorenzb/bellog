from atom import Atom
from query import Query

class RuleParseException(Exception):
    pass

class Rule:
    def __init__(self):
        pass
    
    @classmethod
    def fromString(cls, string):
        rule = Rule()
        rule.head = Atom.fromString(string.split(':-')[0])
        rule.body = Query.fromString(string.split(':-')[1])
        return rule
    
    def toDatalogRules(self):
        for kind in ['top', 'bot']:
            if self.body.isAtomic:
                datalogRuleTop = str(self.head.toDatalog('top')) + ' :- ' + str(self.body.subqueries[0].toDatalog('top'))
                datalogRuleBot = str(self.head.toDatalog('bot')) + ' :- ' + str(self.body.subqueries[0].toDatalog('bot'))
                return [datalogRuleTop, datalogRuleBot]               
            elif self.body.operator == '^':
                datalogRules = []
                freshAtoms = []
                for subquery in self.body.subqueries:
                    freshAtom = Atom.fromString(Atom.freshPredSymbol() + '(' + ','.join(sorted(subquery.vars())) + ')')                        
                    newRuleString = str(freshAtom) + ':-' + str(subquery)
                    newRule = Rule.fromString(newRuleString)
                    freshAtoms.append(freshAtom)
                    datalogRules = datalogRules + newRule.toDatalogRules()
                for kind in ['top', 'bot']:
                    tmp = [str(freshAtom.toDatalog(kind)) for freshAtom in freshAtoms]
                    datalogRule = str(self.head.toDatalog(kind)) + ' :- ' + ','.join(tmp)                    
                    datalogRules.append(datalogRule)
                return datalogRules
            elif self.body.operator == '~':
                freshAtom = Atom.fromString(Atom.freshPredSymbol() + '(' + ','.join(sorted(self.body.vars())) + ')')                   
                datalogRuleTop = str(self.head.toDatalog('top')) + ' :- ' + str(freshAtom.toDatalog('bot'))
                datalogRuleBot = str(self.head.toDatalog('bot')) + ' :- ' + str(freshAtom.toDatalog('top'))
                subqueryRule = Rule.fromString(str(freshAtom) + ':-' + str(self.body.subqueries[0]))
                return [datalogRuleTop, datalogRuleBot] + subqueryRule.toDatalogRules()
            elif self.body.operator == '!':
                freshAtom = Atom.fromString(Atom.freshPredSymbol() + '(' + ','.join(sorted(self.body.vars())) + ')')                   
                datalogRuleTop = str(self.head.toDatalog('top')) + ' :- tnot(' + str(freshAtom.toDatalog('bot')) + ')'
                datalogRuleBot = str(self.head.toDatalog('bot')) + ' :- tnot(' + str(freshAtom.toDatalog('top')) + ')'
                subqueryRule = Rule.fromString(str(freshAtom) + ':-' + str(self.body.subqueries[0]))
                return [datalogRuleTop, datalogRuleBot] + subqueryRule.toDatalogRules()                                          
                
    def __str__(self):
        return str(self.head) + ':-' + str(self.body)
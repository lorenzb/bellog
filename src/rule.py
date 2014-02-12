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
    
    def toDatalogRules(self, kind):
        assert kind in ['top', 'bot']
        if self.body.isAtomic:
            datalogRule = str(self.head.toDatalog(kind)) + ' :- ' + str(self.body.subqueries[0].toDatalog(kind))
            return [datalogRule]
        else:
            datalogRule = 
            newRule = Rule()
            
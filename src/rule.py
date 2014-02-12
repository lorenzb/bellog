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
        rule.query = Query.fromString(string.split(':-')[1])
        return rule
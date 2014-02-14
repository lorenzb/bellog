from rule import Rule
import sys
from grammar import Grammar

# takes a filename as input and returns a set of rules
class Parser:
      
    @classmethod
    def parseRules(cls, rules):
        bellogRules = []
        lineCounter = 0
        for r in rules:
            lineCounter += 1
            r = r.strip().replace(' ', '')
            #try:
            bellogRules.append(Rule.fromElements(Grammar.parseRule(r)))
            #except Exception as e:
            #    print 'Could not parse rule at line', lineCounter, ':', line
            #    print 'Check your syntax'
            #    print 'Exception', e
            #    sys.exit(-1)
        return bellogRules
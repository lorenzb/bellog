from rule import Rule
import sys
from grammar import Grammar

# takes a filename as input and returns a set of rules
class Parser:
      
    @classmethod
    def parseFile(cls, filename):
        rules = []
        fileIn = open(filename, 'r')
        lineCounter = 0
        for line in fileIn:
            lineCounter += 1
            line = line.strip().replace(' ', '')
            #try:
            rules.append(Rule.fromElements(Grammar.parseRule(line)))
            #except:
            #    print 'Could not parse rule at line', lineCounter, ':', line
            #    print 'Check your syntax'
            #    sys.exit(-1)
        fileIn.close()
        return rules
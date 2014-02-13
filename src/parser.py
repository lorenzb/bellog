from rule import Rule
import sys

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
            try:
                rules.append(Rule.fromString(line))
            except:
                print 'Could not parse rule at line', lineCounter, ':', line
                print 'Check your syntax'
                sys.exit(-1)
        fileIn.close()
        return rules
    
    @classmethod
    def bellogRulesToDatalogRules(cls, bellogRules):
        datalogRules = []
        for bellogRule in bellogRules:
            datalogRules += bellogRule.toDatalogRules()
        return datalogRules
    
    @classmethod
    def parseConjunctedQueries(cls, string):
        s='q(X)^(r(X)^q(X))^s(X)^(d(Y)^d(A))'
        print s.split('^')[0]
        
Parser.parseConjunctedQueries('s')
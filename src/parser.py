from rule import Rule

# takes a filename as input and returns a set of rules
class Parser:
      
    @classmethod
    def parseFile(cls, filename):
        rules = []
        fileIn = open(filename, 'r')
        for line in fileIn:
            line = line.strip().replace(' ', '')
            rules.append(Rule.fromString(line))
        fileIn.close()
        return rules
    
    @classmethod
    def bellogRulesToDatalogRules(cls, bellogRules):
        datalogRules = []
        for bellogRule in bellogRules:
            datalogRules += bellogRule.toDatalogRules()
        return datalogRules
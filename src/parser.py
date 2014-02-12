from rule import Rule

# takes a filename as input and returns a set of rules
class Parser:
    
    @classmethod
    def freshAtom(cls):
    
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
        for bellogRule in bellogRules:
            if bellogRule.body.isAtomic:
                print bellogRule.toDatalog('bot')
                print bellogRule.toDatalog('top')
            else:
                pass
            
        
Parser.parseFile('/home/ptsankov/eth/projects/kaba/code/bellog.git/examples/simple.blg')
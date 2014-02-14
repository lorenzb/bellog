from parser import Parser
from config import config
from atom import Atom
import sys
import pexpect

class XSB:
    
    STATIC_RULES = ['true_bot', 
                    'true_top',
                    'bot_bot', 
                    'top_top', 
                    'bot_top :- tnot(top_top)', 
                    'top_bot :- tnot(bot_bot)', 
                    'false_top :- tnot(top_top)', 
                    'false_bot :- tnot(top_top)']
    
    def __init__(self):       
        self.xsb = pexpect.spawn(config['XSB_PATH'])
        
    def loadBellogProgram(self, rules):        
        bellogRules = Parser.parseRules(rules)
        
        # check if there are any predicates that have not been defined
        undefinedAtoms = Atom.SYMBOLS - {r.head.pred for r in bellogRules}.union({'false', 'true', 'top', 'bot'})
        if len(undefinedAtoms) > 0:
            print 'The following predicate symbols have not been defined:', ', '.join(undefinedAtoms)
            sys.exit(-1)
        
        # translate the rules to Datalog and load them into XSB    
        self.xsb.sendline('[user].')
        self.xsb.sendline(':- auto_table.')
        for bellogRule in bellogRules:
            for datalogRule in bellogRule.toDatalogRules():
                self.xsb.sendline(datalogRule + '.')
                
        # load also the static datalog rules
        for datalogRule in XSB.STATIC_RULES:           
            self.xsb.sendline(datalogRule + '.')
            
        # tell XSB that we're done loading rules
        self.xsb.sendcontrol('d')    
        self.xsb.expect('yes')
        
    def query(self, queryString):
        atom = Atom.fromString(queryString)
        self.xsb.sendline(str(atom.toDatalog('bot')) + '.')
        geqBot = self.xsb.expect(['yes', 'no']) == 0
        self.xsb.sendline(str(atom.toDatalog('top')) + '.')
        geqTop = self.xsb.expect(['yes', 'no']) == 0
        if geqBot and geqTop:
            return 'true'
        elif geqBot:
            return 'bot'
        elif geqTop:
            return 'top'
        else:
            return 'false'

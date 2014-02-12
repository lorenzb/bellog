import pexpect
from parser import Parser
from config import config
from atom import Atom

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
        
    def loadBellogProgram(self, filename):        
        bellogRules = Parser.parseFile(filename)
        self.xsb.sendline('[user].')
        self.xsb.sendline(':- auto_table.')
        for rule in Parser.bellogRulesToDatalogRules(bellogRules):
            datalogRule = rule + '.'
            self.xsb.sendline(datalogRule)
        for rule in XSB.STATIC_RULES:
            datalogRule = rule + '.'
            self.xsb.sendline(datalogRule)
        self.xsb.sendcontrol('d')    
        self.xsb.expect('yes')
        print 'File', filename, 'loaded'
        
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
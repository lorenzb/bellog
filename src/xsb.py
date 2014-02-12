import pexpect
from parser import Parser
from config import config
from atom import Atom

class XSB:
    def __init__(self):       
        self.xsb = pexpect.spawn(config['XSB_PATH'])
        
    def loadBellogProgram(self, filename):        
        bellogRules = Parser.parseFile(filename)
        self.xsb.sendline('[user].')
        self.xsb.sendline(':- auto_table.')
        for rule in Parser.bellogRulesToDatalogRules(bellogRules):
            datalogRule = rule + '.'
            self.xsb.sendline(datalogRule)
        self.xsb.sendline('true_bot.')
        self.xsb.sendline('true_top.')
        self.xsb.sendline('bot_bot.')
        self.xsb.sendline('top_top.')
        self.xsb.sendline('bot_top :- tnot(top_top).')        
        self.xsb.sendline('top_bot :- tnot(bot_bot).')        
        self.xsb.sendline('false_top :- tnot(top_top).')
        self.xsb.sendline('false_bot :- tnot(top_top).')        
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
from config import config
from atom import Atom
import pexpect
from grammar import Grammar

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
        
    def loadPolicy(self, policy):
        # translate the rules to Datalog and load them into XSB
        self.policy = policy
        self.xsb.sendline('[user].')
        self.xsb.sendline(':- auto_table.')
        for rule in policy.rules:
            for datalogRule in rule.toDatalogRules():
                self.xsb.sendline(datalogRule + '.')
        # load also the static datalog rules
        for datalogRule in XSB.STATIC_RULES:
            self.xsb.sendline(datalogRule + '.')
            
        # tell XSB that we're done loading rules
        self.xsb.sendcontrol('d')
        self.xsb.expect('yes')
        
    def query(self, queryString):
        try:
            atom = Atom.fromElements(Grammar.parseAtom(queryString), add=False)
        except Exception:
            raise Exception('Could not parse the query ' + queryString)
        atom.inlineIssuer()
        self.policy.checkQuery(atom)
        self.xsb.sendline('set_prolog_flag(unknown,fail).')
        self.xsb.expect('yes')
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

    def close(self):
        self.xsb.close()

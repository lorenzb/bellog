#!/usr/bin/python
import getopt
import os.path
import sys
from xsb import XSB
from policy import Policy
from utils import escapeCharacters
from grammar import Grammar
from atom import Atom

def main():  
    bellogFilename = None
    queryString = None
    datalogFilename = None    
    opts, args = getopt.getopt(sys.argv[1:], 'i:q:o:', ['input', 'query'])
    for o, a in opts:
        if o == '-i':
            bellogFilename = a
        elif o == '-q':
            queryString = a
        elif o == '-o':
            datalogFilename = a
            
    if bellogFilename is None and (queryString is None or datalogFilename is None):
        print 'Usage: python', sys.argv[0], '-i <BelLog file> -q <query> [-o <Datalog filename>]'
        sys.exit(-1)
       
    fileStr = open(bellogFilename, 'r').read().strip()
    polStr = '\n'.join([l for l in fileStr.split('\n') if ':-' in l])
    try:                
        policy = Policy.fromString(escapeCharacters(polStr))
        if queryString is not None:
            query = Atom.fromElements(Grammar.parseAtom(escapeCharacters(queryString)))
        policy.processPolicy()            
    except Exception as e:
        print 'Error parsing the policy:', e
        sys.exit(-1)                             
       
       
    if queryString is not None:        
        xsb = XSB()    
        try:
            policy.checkQuery(query)                    
            xsb.loadPolicy(policy)        
            print 'Query', queryString, ':', xsb.query(query)
            xsb.close()
        except Exception as e:
            print 'Error loading the policy:', e
            sys.exit(-1)
            xsb.close()
                  
    if datalogFilename is not None:
        if os.path.isfile(datalogFilename):
            msg = 'Override ' + datalogFilename + '?'
            shall = True if raw_input("%s (y/N) " % msg).lower() == 'y' else False
            if not shall:
                sys.exit(-1)
        outFile = open(datalogFilename, 'w')        
        for rule in policy.rules:
            for datalogRule in rule.toDatalogRules():
                outFile.write(datalogRule + '.\n') 
        for datalogRule in XSB.STATIC_RULES:
            outFile.write(datalogRule + '.\n')        
        outFile.close()            

if __name__ == '__main__':                                                                                                                     
    main()
    

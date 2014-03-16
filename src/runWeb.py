#!/usr/bin/python
import getopt
import sys
from xsb import XSB
from policy import Policy
from utils import escapeCharacters
from atom import Atom
from grammar import Grammar

def main():  
    webStr = None
    queryString = None    
    opts, args = getopt.getopt(sys.argv[1:], 'i:q:', ['input', 'query'])
    for o, a in opts:
        if o == '-i':
            webStr = a
        elif o == '-q':
            queryString = a
            
    if webStr is None or queryString is None:
        print "Incorrect usage"
        sys.exit(-1)

    xsb = XSB()
    try:
        webStr = webStr.replace('<newline>', '\n')
        polStr = '\n'.join([l for l in webStr.split('\n') if ':-' in l])
        policy = Policy.fromString(escapeCharacters(polStr))
        query = Atom.fromElements(Grammar.parseAtom(escapeCharacters(queryString)))
        policy.processPolicy()   
        policy.checkQuery(query)     
        xsb.loadPolicy(policy)
        print xsb.query(escapeCharacters(queryString))
        xsb.close()
    except Exception as e:
        print 'Error:', e
        xsb.close()
        sys.exit(-1)
         

if __name__ == '__main__':
    main()

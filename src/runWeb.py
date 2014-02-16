#!/usr/bin/python
import getopt
import sys
from xsb import XSB
from policy import Policy

def main():  
    policyString = None
    queryString = None    
    opts, args = getopt.getopt(sys.argv[1:], 'i:q:', ['input', 'query'])
    for o, a in opts:
        if o == '-i':
            policyString = a
        elif o == '-q':
            queryString = a
            
    if policyString is None or queryString is None:
        print "Incorrect usage"
        sys.exit(-1)

    xsb = XSB()
    try:
        policy = Policy.fromString(policyString)
    except Exception as e:
        print 'Error:', e
        sys.exit(-1)     
    xsb.loadPolicy(policy)
    print xsb.query(queryString)
    xsb.close()

if __name__ == '__main__':
    main()

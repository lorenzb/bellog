#!/usr/bin/python
import getopt
import sys
from xsb import XSB
from policy import Policy

def main():  
    bellogFilename = None
    queryString = None    
    opts, args = getopt.getopt(sys.argv[1:], 'i:q:', ['input', 'query'])
    for o, a in opts:
        if o == '-i':
            bellogFilename = a
        elif o == '-q':
            queryString = a
            
    if bellogFilename is None or queryString is None:
        print 'Usage: python', sys.argv[0], '-i <BelLog file> -q <query>'
        sys.exit(-1)
      
    xsb = XSB()
    try:
        fileStr = open(bellogFilename, 'r').read().strip()
        polStr = '\n'.join([l for l in fileStr.split('\n') if ':-' in l])
        policy = Policy.fromString(polStr)        
        xsb.loadPolicy(policy)
        print 'Query', queryString, ':', xsb.query(queryString)
        xsb.close()
    except Exception as e:
        print 'Error:', e
        xsb.close()
        sys.exit(-1)                

if __name__ == '__main__':                                                                                                                     
    main()

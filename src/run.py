#!/usr/bin/python
import getopt
import sys
from xsb import XSB

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
    xsb.loadBellogProgram(bellogFilename)
    print 'Query', queryString, ':', xsb.query(queryString)

if __name__ == '__main__':                                                                                                                     
    main()
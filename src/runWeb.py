#!/usr/bin/python
import getopt
import sys
from xsb import XSB

def main():  
    bellogString = None
    queryString = None    
    opts, args = getopt.getopt(sys.argv[1:], 'i:q:', ['input', 'query'])
    for o, a in opts:
        if o == '-i':
            bellogString = a
        elif o == '-q':
            queryString = a
            
    if bellogString is None or queryString is None:
        print "Incorrect usage"
        sys.exit(-1)
    xsb = XSB(  )
    try:
        xsb.loadBellogProgram([x for x in bellogString.split('<next>') if x != ''])
        print xsb.query(queryString)
    except Exception as e:
        print 'Error:', e
        sys.exit(-1)     
    xsb.close()

if __name__ == '__main__':
    main()

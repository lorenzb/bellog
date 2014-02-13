from pyparsing import Word, Literal, srange, ZeroOrMore, Optional, OneOrMore, Forward, Group, Or

#USAGE: query.parseString('(owner(X) ^ !(grant(X,Y)) ^ true)', parseAll=True)

class Grammar:
    left = Literal('(')
    right = Literal(')')
    comma = Literal(',')
    conj = Literal('^')
    neg = Literal('!')
    inv = Literal('~')
    arrow = Literal(':-')
    pred = Word(srange("[a-z]"), srange("[a-zA-Z0-9]") )
    const = Word(srange("[a-z]"), srange("[a-zA-Z0-9]") )
    var = Word(srange("[A-Z]"), srange("[a-zA-Z0-9]") )
    arg = Optional(comma) + (const | var)
    args = Group(left + arg + Optional(ZeroOrMore(comma + arg)) + right)
    atom = Group(pred + Optional(args))
    query = Forward()
    conjQuery = Group(left + query + OneOrMore(conj + query) + right)
    negQuery = Group(neg + left + query + right)
    invQuery = Group(inv + left + query + right)
    query << Or([atom, invQuery, negQuery, conjQuery])
    rule = atom + arrow + query
    
    @classmethod
    def parseRule(cls, string):
        return Grammar.rule.parseString(string, parseAll=True)
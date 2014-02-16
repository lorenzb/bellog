from pyparsing import Word, Literal, srange, ZeroOrMore, Optional, OneOrMore, Forward, Group, Or

#USAGE: query.parseString('(owner(X) ^ !(grant(X,Y)) ^ true)', parseAll=True)

class Grammar:
    left = Literal('(')
    right = Literal(')')
    comma = Literal(',').suppress()
    conj = Literal('^')
    neg = Literal('!')
    inv = Literal('~')
    arrow = Literal(':-').suppress()
    overrideOp = Or([Literal('-false->'), Literal('-bot->'), Literal('-top->'), Literal('-true->')])
    plusOp = Literal('-plus-')
    timesOp = Literal('-times-') 
    pred = Word(srange("[a-z]"), srange("[a-zA-Z0-9]") )
    const = Word(srange("[a-z]"), srange("[a-zA-Z0-9]") )
    var = Word(srange("[A-Z]"), srange("[a-zA-Z0-9]") )
    arg = Optional(comma) + (const | var)
    args = Group(left + arg + Optional(ZeroOrMore(comma + arg)) + right)
    atom = Group(pred + Optional(args))
    
    unaryOperator = neg | inv
    binaryOperator = overrideOp | plusOp | timesOp
    query = Forward()    
    query << Or([atom, Group(unaryOperator + query), Group(left + query + OneOrMore(conj + query) + right), Group(left + query + binaryOperator + query + right)])
        
    rule = Group(atom + arrow + query)
    policy = OneOrMore(rule)
    
    @classmethod
    def parseRule(cls, string):
        return Grammar.rule.parseString(string, parseAll=True)
    
    @classmethod
    def parsePolicy(cls, string):
        return Grammar.policy.parseString(string, parseAll=True)
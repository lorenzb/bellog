from atom import Atom

class Query:
        
    def __init__(self):
        pass
       
        
    @classmethod
    def fromElements(self, elements):
        query = Query()
        query.subqueries = []
        if elements[0] == '!':
            # negated query
            query.operator = '!'
            subquery = Query.fromElements(elements[1])
            query.subqueries.append(subquery)          
        elif elements[0] == '~':
            # inverted query
            query.operator = '~'
            subquery = Query.fromElements(elements[1])
            query.subqueries.append(subquery)
        elif elements[0] == '(':
            # infix query
            if elements[2] == '^':
                # conjunction            
                query.operator = '^'
                for subqueryElements in elements[1:-1:2]:
                    subquery = Query.fromElements(subqueryElements)                 
                    query.subqueries.append(subquery)
            elif elements[2] in ['-false->', '-bot->', '-top->', '-true->']:
                return Query.fromElements(Query.getOverride(elements[1], elements[2][1:-2], elements[3]))
            elif elements[2] == '-plus-':
                return Query.fromElements(Query.getPlus(elements[1], elements[3]))
            elif elements[2] == '-times-':
                return Query.fromElements(Query.getTimes(elements[1], elements[3]))
        else:
            # atomic query
            query.operator = ''
            query.subqueries.append(Atom.fromElements(elements))
        return query
            
    # returns the set of variables that appear in the query
    def getArgs(self):
        allVars = []
        for subquery in self.subqueries:
            allVars = allVars + subquery.getArgs()
        return allVars
    
    def getPreds(self):
        posPreds = set()
        negPreds = set()
        if self.operator == '!':
            for subquery in self.subqueries:
                subqueryPreds = subquery.getPreds()
                negPreds = negPreds.union(subqueryPreds[0])
                negPreds = negPreds.union(subqueryPreds[1]) 
        else:
            for subquery in self.subqueries:
                subqueryPreds = subquery.getPreds()
                posPreds = posPreds.union(subqueryPreds[0])
                negPreds = negPreds.union(subqueryPreds[1])   
        return (posPreds, negPreds)
    
    def __str__(self):
        if self.operator == '^':                
            return '(' + '^'.join(map(str, self.subqueries)) + ')'
        elif self.operator == '':
            return str(self.subqueries[0])
        else:
            return self.operator + '(' + str(self.subqueries[0]) + ')'            
        
        
    # Syntactic shorthands defined below
        
    # template method that replace the "-true->" operator with a query that corresponds to this operator
    @classmethod    
    def getOverride(cls, p, value, q):
        return ['!', ['(', ['!', ['(', Query.getEq(p, value), '^', q, ')']], '^', ['!', ['(', ['!', Query.getEq(p, value)], '^', p, ')']], ')']]
    
    @classmethod
    def getEq(cls, p, value):
        if value == 'true':
            return ['(', p, '^', ['~', p], ')']
        elif value == 'false':
            return ['(', ['!', p], '^', ['!', ['~', p]], ')']
        elif value == 'bot':
            return ['(', Query.getEq(Query.getOr(p, 'top'), 'true'), '^', ['!', Query.getEq(p, 'true')], '^', ['!', Query.getEq(p, 'false')], ')']
        elif value == 'top':
            return ['(', Query.getEq(Query.getOr(p, 'bot'), 'true'), '^', ['!', Query.getEq(p, 'true')], '^', ['!', Query.getEq(p, 'false')], ')']
        
    @classmethod
    def getOr(cls, p, value):
        if value in ['bot', 'top']:
            return ['!', ['(', ['!', p], '^', [value], ')']]
        elif value == 'false':
            return ['!', ['(', ['!', p], '^', ['true'], ')']]
        elif value == 'true':
            return ['!', ['(', ['!', p], '^', ['false'], ')']]
        
    @classmethod
    def getPlus(cls, p, q):
        return ['!', ['(', ['!', ['(', p, '^', ['top'], ')']], '^', ['!', ['(', q, '^', ['top'], ')']], '^', ['!', ['(', p, '^', q, ')']], ')']]
    
    @classmethod
    def getTimes(cls, p, q):
        return ['!', ['(', ['!', ['(', p, '^', ['bot'], ')']], '^', ['!', ['(', q, '^', ['bot'], ')']], '^', ['!', ['(', p, '^', q, ')']], ')']]
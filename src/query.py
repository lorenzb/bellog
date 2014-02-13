from atom import Atom
import copy

class Query:
        
    def __init__(self):
        pass
    
    # template method that replace the "-true->" operator with a query that corresponds to this operator
    @classmethod    
    def getTrueOverride(self, p, q):
        return ['!', '(', ['(', ['!', '(', ['(', ['(', p, '^', ['~', '(', p, ')'], ')'], '^', q, ')'], ')'], '^', ['!', '(', ['(', ['!', '(', ['(', p, '^', ['~', '(', p, ')'], ')'], ')'], '^', p, ')'], ')'], ')'], ')']
        
    @classmethod
    def fromElements(self, elements):
        query = Query()
        query.subqueries = []
        if elements[0] == '!':
            # negated query
            query.operator = '!'
            subquery = Query.fromElements(elements[2])
            query.subqueries.append(subquery)          
        elif elements[0] == '~':
            # inverted query
            query.operator = '~'
            subquery = Query.fromElements(elements[2])
            query.subqueries.append(subquery)
        elif elements[0] == '(':
            # infix query
            if elements[2] == '^':
                # conjunction            
                query.operator = '^'
                for subqueryElements in elements[1:-1:2]:
                    subquery = Query.fromElements(subqueryElements)                 
                    query.subqueries.append(subquery)
            elif elements[2] == '-true->':
                return Query.fromElements(Query.getTrueOverride(elements[1], elements[3]))
        else:
            # atomic query
            query.operator = ''
            query.subqueries.append(Atom.fromElements(elements))
        return query
            
    # returns the set of variables that appear in the query
    def vars(self):
        allVars = set()
        for subquery in self.subqueries:
            allVars = allVars.union(subquery.vars())
        return allVars
    
    def __str__(self):
        if self.operator == '^':                
            return '(' + '^'.join(map(str, self.subqueries)) + ')'
        elif self.operator == '':
            return str(self.subqueries[0])
        else:
            return self.operator + '(' + str(self.subqueries[0]) + ')'
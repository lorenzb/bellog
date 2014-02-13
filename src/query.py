from atom import Atom

class QueryParseException(Exception):
    pass

class Query:
        
    def __init__(self, elements):
        self.subqueries = []
        if elements[0] == '!':
            # negated query
            self.operator = '!'
            subquery = Query(elements[2])
            self.subqueries.append(subquery)          
        elif elements[0] == '~':
            # inverted query
            self.operator = '~'
            subquery = Query(elements[2])
            self.subqueries.append(subquery)
        elif elements[0] == '(':
            # conjunction of queries
            self.operator = '^'
            for subqueryElements in elements[1:-1:2]:
                subquery = Query(subqueryElements)                 
                self.subqueries.append(subquery)
        else:
            # atomic query
            self.operator = ''
            self.subqueries.append(Atom(elements))
            
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
from atom import Atom

class QueryParseException(Exception):
    pass

class Query:
    def __init__(self):
        self.operator = None
        self.subqueries = []
        self.isAtomic = False        
        
    @classmethod
    def fromString(self, string):
        query = Query()
        if len(string) <=0:
            raise QueryParseException, 'Cannot parse an empty query'
        
        if string[0] == '!':
            # negated query
            query.operator = '!'
            query.isAtomic = False
            subquery = Query.fromString(string[2:-1])
            query.subqueries.append(subquery)          
        elif string[0] == '~':
            # inverted query
            query.operator = '~'
            query.isAtomic = False
            subquery = Query.fromString(string[2:-1])
            query.subqueries.append(subquery)
        elif string[0] == '(':
            # conjunction of queries
            query.operator = '^'
            query.isAtomic = False
            for subqueryString in string[1:-1].split('^'):
                query.subqueries.append(Query.fromString(subqueryString))
        else:
            # atomic query
            self.operator = ''
            query.isAtomic = True
            query.subqueries.append(Atom.fromString(string))
        return query
            
    # returns the set of variables that appear in the query
    def vars(self):
        allVars = set()
        for subquery in self.subqueries:
            allVars = allVars.union(subquery.vars())
        return allVars
    
    def __str__(self):
        if self.isAtomic:
            assert len(self.subqueries) == 1
            # the subquery is an atom
            return str(self.subqueries[0])
        else:            
            # we have a composite query
            if self.operator == '^':
                assert len(self.subqueries) >= 1                
                return '(' + '^'.join(map(str, self.subqueries)) + ')'
            else:
                assert len(self.subqueries) == 1
                return self.operator + '(' + str(self.subqueries[0]) + ')'
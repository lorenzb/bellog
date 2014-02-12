from atom import Atom

class QueryParseException(Exception):
    pass

class Query:
    def __init__(self):
        self.operator = None
        self.subqueries = None
        self.isAtomic = False        
        
    @classmethod
    def fromString(self, string):
        print 'query', string
        query = Query()
        if len(string) <=0:
            raise QueryParseException, 'Cannot parse an empty query'
        
        if string[0] == '!':
            # negated query
            query.operator = '!'
            query.isAtomic = False
            subquery = Query.fromString(string[2:-1])
            query.subqueries = {subquery}
            return query             
        elif string[0] == '~':
            # inverted query
            query.operator = '~'
            query.isAtomic = False
            subquery = Query.fromString(string[2:-1])
            query.subqueries = {subquery}
            return query
        elif string[0] == '(':
            # conjunction of queries
            query.operator = '^'
            query.isAtomic = False
            query.subqueries = set()
            for subqueryString in string[1:-1].split('^'):
                query.subqueries.add(Query.fromString(subqueryString))
            return query
        else:
            # atomic query
            query.isAtomic = True
            query.subquery = {Atom.fromString(string)}
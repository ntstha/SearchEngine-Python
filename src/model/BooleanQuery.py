#@author
class BooleanQuery:
    def __init__(self,query1,query2,booleanOperator):
        self.query1 = query1;
        self.query2 = query2;
        self.booleanOperator = booleanOperator;
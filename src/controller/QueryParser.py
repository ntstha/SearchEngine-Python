#@author
from nltk.corpus import stopwords
from nltk.stem.porter import *

from src.controller.QueryExecutor import QueryExecutor;
from src.model.BooleanOperator import BooleanOperator;


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

class QueryParser:

    def splitStemAndRemoveStopwords(self,query):
        stemmed_string_tokens=[];
        tokens=query.split();
        stemmer = PorterStemmer();
        for t in tokens:
            if t.lower() in stopwords.words('english'):
                continue;
            else:
                stemmed_string_tokens.append(stemmer.stem(t.lower()));
        return stemmed_string_tokens;

    def removeStopWords(self,query_string):
        parsed_string_tokens=[];
        tokens = query_string.split();
        for t in tokens:
            if t.lower() not in {"and","or","not"} and t.lower() in stopwords.words('english'):
                continue;
            else:
                parsed_string_tokens.append(t.lower());
        return " ".join(parsed_string_tokens);

    def stemQueryString(self,query_string):
        stem_tokens=[];
        stemmer = PorterStemmer();
        tokens = query_string.split();
        for t in tokens:
            if BooleanOperator.is_boolean_op(t):
                stem_tokens.append(t);
            elif t==BooleanOperator.LParen or t==BooleanOperator.RParen:
                stem_tokens.append(t);
            else:
                stem_tokens.append(stemmer.stem(t));

        return " ".join(stem_tokens);

    def generate_postfix_expr(self,query_string):
        tokens =query_string.split();
        stack = Stack();
        active_query=[];
        for t in tokens:
            t=t.lower();
            if t==BooleanOperator.LParen:
                stack.push(t);
            elif t==BooleanOperator.RParen:
                while stack.peek()!=BooleanOperator.LParen:
                    active_query.append(stack.pop());
                stack.pop();
            elif t==BooleanOperator.AND or t==BooleanOperator.OR or t==BooleanOperator.NOT:
                while not stack.isEmpty() and BooleanOperator.precedence(stack.peek())>BooleanOperator.precedence(t):
                    active_query.append(stack.pop());
                stack.push(t);
            else:
                active_query.append(t);

        if not stack.isEmpty():
            while not stack.isEmpty():
                active_query.append(stack.pop());

        return active_query;

    def execute_postfix_tokens(self,post_fix_tokens):
        stack=Stack();
        queryExecutor = QueryExecutor();
        result=[];
        for t in post_fix_tokens:
            if not BooleanOperator.is_boolean_op(t):
                stack.push(t)
            elif t==BooleanOperator.NOT:
                operand = stack.pop();
                result = queryExecutor.execute_not_operation(operand);
                stack.push(result);
            elif t==BooleanOperator.AND:
                operand1=stack.pop();
                operand2=stack.pop();
                result = queryExecutor.execute_and_operation(operand1,operand2);
                stack.push(result);
            else:
                operand1=stack.pop();
                operand2=stack.pop();
                result = queryExecutor.execute_or_operation(operand1,operand2);
                stack.push(result);
        if not stack.isEmpty():
            result=stack.pop();
            if isinstance(result,basestring):
                result=queryExecutor.doc_containing_single_term(result);
        return result;


#@author
class BooleanOperator:
    OR="or"
    AND="and";
    NOT="not";
    LParen="(";
    RParen=")";

    @staticmethod
    def is_boolean_op(token):
        if token==BooleanOperator.AND or token==BooleanOperator.OR or token==BooleanOperator.NOT:
            return True;
        else:
            return False;

    @staticmethod
    def precedence(token):
        if token==BooleanOperator.NOT:
            return  3;
        elif token==BooleanOperator.AND:
            return 2;
        else:
            return 1;

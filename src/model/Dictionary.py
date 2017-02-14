#@author
class Dictionary:
    def __init__(self,list_term=[]):
        self.list_term = list_term;

    def is_word_in_dic(self,word):
        for t in self.list_term:
            if word==t.term_word:
                return True;
        return False;

    def get_term_from_dic(self,word):
        for t in self.list_term:
            if t.term_word==word:
                return t;
        return None;






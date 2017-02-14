from collections import defaultdict
class Term:
    term_id_index = defaultdict(list)
    def __init__(self,document_id=None,term_word=None,term_id=None,term_freq=None,ft=None,Wt=None,Tf=None):
        self.document_id = document_id;
        self.term_word = term_word;
        self.term_id = term_id;
        self.term_freq = term_freq;
        self.ft=ft;
        self.Wt=Wt;
        self.Tf=Tf;
        Term.term_id_index[term_id].append(self);

    def __cmp__(self, other):
        if self.term_id > other.term_id:
            return 1;
        elif self.term_id < other.term_id:
            return -1;
        else:
            if self.document_id > other.document_id:
                return 1;
            else:
                return -1;

    def __repr__(self):
        return "["+str(self.document_id)+","+str(self.term_freq)+","+str(self.term_word)+"]";

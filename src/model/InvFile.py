class InvFile:
    def __init__(self,dft=None,list_term=[]):
        self.dft=dft;
        self.list_term = list_term;

    def __repr__(self):
        return "["+str(self.dft)+","+",".join(map(repr,self.list_term))+"]";
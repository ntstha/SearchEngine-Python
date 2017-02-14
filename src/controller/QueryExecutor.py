#@author Nishit Shrestha
from nltk.corpus import stopwords;

from src.controller.Reader import Reader;
from src.model.BooleanOperator import BooleanOperator;


class QueryExecutor:
    inv_file_hash={};
    def __init__(self):
        reader = Reader();
        global inv_file_hash;
        global document_list;
        global no_of_doc;
        no_of_doc=1400;
        document_list=list(range(1,no_of_doc+1));
        inv_file_hash= reader.read_inv_file();

    def get_doc_from_invFile(self,inv_file):
        doc_containing_term=[];
        for term in inv_file.list_term:
            doc_containing_term.append(term.document_id);
        return doc_containing_term;

    def doc_containing_single_term(self,word):
        result=[];
        if word in stopwords.words('english'):
            result=[];
        else:
            inv_file=self.get_document_containing(word);
            if inv_file!=None:
                result = self.get_doc_from_invFile(inv_file);
        return result;

    def get_document_containing(self,word):
        inv_file = inv_file_hash.get(word);
        return inv_file;

    def execute_not_operation(self,entry):
        if not isinstance(entry,basestring):
            doc_not_containing_term=[];
            if len(entry)>0:
                doc_not_containing_term=set(document_list)-set(entry);
        else:
            query=entry;
            if query in stopwords.words('english'):
                return None;
            else:
                doc_containing_term = [];
                doc_not_containing_term=[];
                inv_file = self.get_document_containing(query);
                if inv_file!=None:
                    doc_containing_term = self.get_doc_from_invFile(inv_file);
                    doc_not_containing_term=set(document_list)-set(doc_containing_term);
        return doc_not_containing_term;

    def execute_boolean_operation(self,query1,query2,operation):
        is_query1_stopword=False;
        is_query2_stopword=False;
        if query1 in stopwords.words('english'):
            is_query1_stopword=True;
        if query2 in stopwords.words('english'):
            is_query2_stopword=True;

        if is_query1_stopword  and is_query2_stopword:
            result=[];
        elif not is_query1_stopword and not is_query2_stopword:
            inv_file1 = self.get_document_containing(query1);
            inv_file2 = self.get_document_containing(query2);
            doc_containing_term1=[];
            doc_containing_term2=[];
            if inv_file1!=None:
                doc_containing_term1=self.get_doc_from_invFile(inv_file1);
            if inv_file2!=None:
                doc_containing_term2=self.get_doc_from_invFile(inv_file2);
            if operation==BooleanOperator.AND:
                result = list(set(doc_containing_term1) & set(doc_containing_term2));
            else:
                result = list(set(doc_containing_term1) | set(doc_containing_term2));
        else:
            doc_containing_term1=[];
            doc_containing_term2=[];
            if is_query1_stopword:
                inv_file2 = self.get_document_containing(query2);
                if inv_file2!=None:
                    doc_containing_term2=self.get_doc_from_invFile(inv_file2);
                result=doc_containing_term2;
            else:
                inv_file1 = self.get_document_containing(query1);
                if inv_file1!=None:
                    doc_containing_term1=self.get_doc_from_invFile(inv_file1);
                result=doc_containing_term1;
        return result;

    def execute_and_operation(self,entry1,entry2):
        result=[];
        if not isinstance(entry1,basestring) and not isinstance(entry2,basestring):
            result=list(set(entry1) & set(entry2));
        elif isinstance(entry1,basestring) and isinstance(entry2,basestring):
            result = self.execute_boolean_operation(entry1,entry2,BooleanOperator.AND);
        else:
            if not isinstance(entry1,basestring) and isinstance(entry2,basestring):
                is_query_stopword=False;
                if entry2 in stopwords.words('english'):
                    is_query_stopword=True;
                if is_query_stopword:
                    result = entry1;
                else:
                    doc_containing_term=[];
                    inv_file = self.get_document_containing(entry2);
                    if inv_file!=None:
                        doc_containing_term=self.get_doc_from_invFile(inv_file);
                    result = list(set(entry1) & set(doc_containing_term));
            else:
                is_query_stopword=False;
                if entry1 in stopwords.words('english'):
                    is_query_stopword=True;
                if is_query_stopword:
                    result = entry2;
                else:
                    doc_containing_term=[];
                    inv_file = self.get_document_containing(entry1);
                    if inv_file!=None:
                        doc_containing_term=self.get_doc_from_invFile(inv_file);
                    result = list(set(doc_containing_term) & set(entry2));
        return result;

    def execute_or_operation(self,entry1,entry2):
        result=[];
        if not isinstance(entry1,basestring) and not isinstance(entry2,basestring):
            result=list(set(entry1) & set(entry2));
        elif isinstance(entry1,basestring) and isinstance(entry2,basestring):
            result = self.execute_boolean_operation(entry1,entry2,BooleanOperator.OR);
        else:
            if not isinstance(entry1,basestring) and isinstance(entry2,basestring):
                is_query_stopword=False;
                if entry2 in stopwords.words('english'):
                    is_query_stopword=True;
                if is_query_stopword:
                    result = entry1;
                else:
                    doc_containing_term=[];
                    inv_file = self.get_document_containing(entry2);
                    if inv_file!=None:
                        doc_containing_term=self.get_doc_from_invFile(inv_file);
                    result = list(set(entry1) | set(doc_containing_term));
            else:
                is_query_stopword=False;
                if entry1 in stopwords.words('english'):
                    is_query_stopword=True;
                if is_query_stopword:
                    result = entry2;
                else:
                    doc_containing_term=[];
                    inv_file = self.get_document_containing(entry1);
                    if inv_file!=None:
                        doc_containing_term=self.get_doc_from_invFile(inv_file);
                    result = list(set(doc_containing_term) | set(entry2));
        return result;

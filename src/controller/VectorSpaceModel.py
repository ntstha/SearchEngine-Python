#@author Nishit Shrestha
import numpy as np;
from nltk.stem.porter import *

from src.controller.Reader import Reader;
from src.utilities.FileHelper import FileHelper;
from QueryParser import QueryParser;
import operator


class VectorSpaceModel:

    def __init__(self):
        fileReader = Reader();
        global obj_dict;
        global num_docs;
        num_docs=6;
        obj_dict=fileReader.read_inv_file();

    def computeTfOfWordInDoc(self,doc_term_freq):
        return 1+np.log(doc_term_freq);

    def computeWdOfDoc(self):
        Wd_dict={};
        for key,value in obj_dict.iteritems():
            invFile = value;
            for term in invFile.list_term:
                doc_id = term.document_id;
                if Wd_dict.get(doc_id)==None:
                    Wd_dict[doc_id]=np.square(self.computeTfOfWordInDoc(term.term_freq));
                else:
                    Wd_dict[doc_id]=Wd_dict[doc_id]+np.square(self.computeTfOfWordInDoc(term.term_freq));

        #square root each Wd again
        for key,value in Wd_dict.iteritems():
            Wd_dict[key]=np.sqrt(Wd_dict[key]);

        return Wd_dict;

    def calcWtOfWord(self):
        term_model ={};
        for key,value in obj_dict.iteritems():
            invFile = value;
            dft = invFile.dft;
            Wt = self.getWt(dft);
            term_model[key]=Wt;

        return term_model;

    def getWt(self,dft):
        return np.log(1+num_docs/dft);

    def generateDocumentMatrix(self):
        term_model=self.calcWtOfWord();
        Wd_dict = self.computeWdOfDoc();
        return term_model,Wd_dict;

    def generateCosineForQuery(self,query,term_model,Wd_dict):
        cosine_matrix={};
        queryParser = QueryParser();
        stemmed_tokens = queryParser.splitStemAndRemoveStopwords(query);
        for token in stemmed_tokens:
            if obj_dict.get(token)==None:
                continue;
            inv_file=obj_dict[token];
            for t in inv_file.list_term:
                sum=0;
                if cosine_matrix.get(t.document_id)!=None:
                    sum=cosine_matrix[t.document_id];
                cosine_matrix[t.document_id]=sum+self.computeTfOfWordInDoc(t.term_freq)*term_model[token];

        #divide by Wd
        for key,value in cosine_matrix.iteritems():
            Wd = Wd_dict[key];
            cosine_matrix[key]=cosine_matrix[key]/Wd;

        return cosine_matrix;

    def orderDocAccordingToCosine(self,cosine_matrix):
        ordered_doc_id=[];
        sorted_cosine_matrix = sorted(cosine_matrix.items(), key=operator.itemgetter(1),reverse=True)
        for doc_id in sorted_cosine_matrix:
            ordered_doc_id.append(doc_id[0]);
        return ordered_doc_id;

















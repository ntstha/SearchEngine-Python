from src.controller.VectorSpaceModel import VectorSpaceModel;
from src.utilities.FileHelper import FileHelper;
from nltk.corpus import stopwords;
from nltk.stem.porter import *
import operator
import re;

queries=[];

fileHelper = FileHelper();
text = fileHelper.getTextFromFile('cran/cran.qry');

listindex=[];
index = text.find(".I",0);

queries=[];
while index >= 0:
    listindex.append(index);
    index = text.find(".I",index+1);

for i,j in enumerate(listindex):
    query_token=[];
    start=j;
    if i==len(listindex)-1:
        end=len(text);
        ind = text.find(".W",start,end);
        start=ind+2;
        doc_words = re.findall("\\w+",text[start:end]);
    else:
        end = listindex[i+1]-1;
        start=j;
        ind = text.find(".W",start,end);
        start=ind+2;
        doc_words = re.findall("\\w+",text[start:end]);
    for w in doc_words:
        if w.isalpha():
            query_token.append(w.lower());
    queries.append(" ".join(query_token));

vectorSpaceModelObj = VectorSpaceModel();

for query in queries:
    term_model,Wd_dict = vectorSpaceModelObj.generateDocumentMatrix();
    cosine_matrix=vectorSpaceModelObj.generateCosineForQuery(query,term_model,Wd_dict);
    sorted_cosine_matrix=sorted(cosine_matrix.items(), key=operator.itemgetter(1),reverse=True);
    print "For query: "+query+" ranked order of document are \n";
    print [int(t[0]) for t in sorted_cosine_matrix];
    print "\n";
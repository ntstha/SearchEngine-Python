#@author Nishit Shrestha
import copy
import os
import pickle
import time

from nltk.corpus import stopwords
from nltk.stem.porter import *

from src.model.Dictionary import Dictionary
from src.model.InvFile import InvFile
from src.model.Term import Term
from src.utilities.FileHelper import FileHelper;

start_time = time.time()

fileHelper = FileHelper();

text = fileHelper.getTextFromFile("cran/cran.all.1400");

listindex=[];
doc_text=[];
index = text.find(".I 1",0);
words=[];

stop_word_pattern=re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*');
count=1;

while index >= 0:
    listindex.append(index)
    count=count+1;
    index = text.find(".I "+str(count))

dictionary= Dictionary();
stemmer = PorterStemmer();
term_id_counter=1;
dict={};
doc_id=0;
for i,j in enumerate(listindex):
    doc_dict={};
    doc_terms={};
    start=j;
    if i==len(listindex)-1:
        end=len(text);
        ind = text.find(".W",start,end);
        start=ind+2;
        doc_words = re.findall("\\w+",stop_word_pattern.sub('', text[start:end]));
    else:
        end = listindex[i+1]-1;
        start=j;
        ind = text.find(".W",start,end);
        start=ind+2;
        doc_words = re.findall("\\w+",stop_word_pattern.sub('', text[start:end]));
    if i==0:
        doc_id=1;
    else:
        index = listindex[i];
        char=text[index];
        result="";
        while char!="\n":
            if char.isdigit():
                result+=char;
            index=index+1;
            char=text[index]
        doc_id=int(result);
    for w in doc_words:
       if w.isalpha():
           stemmed_word = stemmer.stem(w.lower());
           if dict.get(stemmed_word)==None:
                term = Term();
                term.document_id=i+1;
                term.term_word=stemmed_word;
                term.term_freq=1;
                term.term_id=term_id_counter;
                term_id_counter=term_id_counter+1; #increment the id counter

                dict[stemmed_word]=term.term_id;
                doc_dict[stemmed_word]=term.term_id,term.term_freq;
                doc_terms[term.term_id]=term;

           else:
                if doc_dict.get(stemmed_word)==None:
                   term_id = dict[stemmed_word];
                   term_freq=0;
                   term=Term();
                else:
                    term_id,term_freq = doc_dict[stemmed_word];
                    term = doc_terms.get(term_id);
                term.document_id=i+1;
                term.term_word=stemmed_word;
                term.term_freq=term_freq+1;
                term.term_id=term_id;
                doc_terms[term.term_id]=term;
                doc_dict[stemmed_word]=term.term_id,term.term_freq;

    dictionary.list_term.extend(doc_terms.values());


#Now we have a dictionary
#Sort the dictionary in ascending order according to term_id
dictionary.list_term = sorted(dictionary.list_term);

#Now we go through each of the dictionary terms and find out the document frequency and form a Inverted File Hash
INV_FILE_HASH={}
dft = 1;
term = dictionary.list_term[0];

inv_file = InvFile();
inv_file.dft=dft;
inv_file.list_term.append(term);

INV_FILE_HASH[term.term_word]=inv_file;

current_doc_id = term.document_id;
for i in range(1,len(dictionary.list_term)):
        current_term = dictionary.list_term[i];
        if term.term_id==current_term.term_id:
            if current_term.document_id > current_doc_id:
                dft=dft+1;
                current_doc_id=current_term.document_id;
            inv_file.dft=dft;
            inv_file.list_term.append(current_term);
        else:
            dft=1;
            term=copy.copy(current_term);
            inv_file = InvFile(None,[]);
            inv_file.dft=dft;
            inv_file.list_term.append(current_term);
            current_doc_id=current_term.document_id;
            INV_FILE_HASH[term.term_word]=inv_file;


if os.path.exists('output.txt'):
    os.remove('output.txt');

output = open('output.txt', 'ab+')
pickle.dump(INV_FILE_HASH, output)
output.close()


print("Wrote the inverted matrix to Output.txt in %s seconds." % (time.time() - start_time))


















#@author Nishit Shrestha
import re
import os
from nltk.stem.porter import *
from operator import itemgetter

#Read document file
file = open('../cran/cran.all.1400','r');
#read the entire file
text = file.read();
file.close();
#get each documents from the text. Documents are separated by .I
words = text.split();

#read from stopwords file
file = open('../stopwords.txt','r');
stop_words = file.read();
file.close();

#create a file for writing output
#file = open('result.txt','w+');

docs=[];

start1=False;
start2=False;
doc_word="";
for id,word in enumerate(words):
    if start1 is False and word=='.I':
        start1=True;
        continue;
    if start1 is True and start2 is False and word=='.W':
        start2=True;
        continue;

    if start1 is True and start2 is True and word!='.I':
        if word=='.':
            continue;
        doc_word=doc_word+" "+word;
        if id==len(words)-1:
            docs.append(doc_word);
        continue;

    if start1 is True and start2 is True and word=='.I':
        docs.append(doc_word);
        doc_word="";
        start2=False;
        continue;

#print docs;

def is_word_in_dic(dictionary,word):
    for item in dictionary:
        if item[0]==word:
            return True;
    return False;

def get_item_from_dic(dic,word):
    for index,item in enumerate(dic):
        if item[0]==word:
            return index,item;
    return -1,[];
#now we have all the words after .W and between .I which I conider to be a single document
#we iterate through each document and process them

#storing id and word in a dictionary
dic=[];
stemmer = PorterStemmer();
for doc in docs:
    if len(doc)==0:
        continue;
    words = doc.split();
    for word in words:
        if word in stop_words:
            continue; #remove stop words from the list
        else:
            if word.isalpha():
                stemmed_word = stemmer.stem(word);
                if not is_word_in_dic(dic,stemmed_word):
                    dic.append((stemmed_word,1)); #append unique word to the dictionary with an id and frequency
                else:
                    index,dic_term=get_item_from_dic(dic,stemmed_word);
                    dic_term=(dic_term[0],dic_term[1]+1);
                    dic[index]=dic_term;


#now we have a dictionary that has the term_index, unique term and term_frequency
result=[];
doc_num=0;
for doc in docs:
    count_word=0;
    term_list=[];
    if len(doc)==0:
        continue;
    doc_num = doc_num+1;
    words = re.findall('\\w+',doc);
    for word in words:
        if word in stop_words:
            continue; #remove stop words from the list
        else:
            if is_word_in_dic(dic,word):
                stemmed_word = stemmer.stem(word);
                index,dic_term=get_item_from_dic(dic,stemmed_word);
                if not dic_term in term_list:
                    count_word=count_word+1;
                term_list.append(dic_term);
    term_list.sort(key=itemgetter(1));
    result.append((doc_num,count_word,term_list))

for r in result:
    print 'Document Id: '+str(r[0])+'\t\tNo of Unique words: '+str(r[1])+'\n';
    for t in r[2]:
        print '\t'+str(t[0])+'\t'+str(t[1])+'\n';

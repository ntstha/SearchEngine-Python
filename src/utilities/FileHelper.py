#Author Nishit Shrestha
import re
from nltk.corpus import stopwords
import os;
class FileHelper:

    def __init__(self):
        global stop_word_pattern;
        stop_word_pattern=re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')

    def getTextFromFile(self,file_name):
        my_dir = os.path.dirname(os.path.dirname(__file__));
        file_path = os.path.join(my_dir,file_name);
        file = open(file_path,'r');
        text = file.read();
        file.close();
        return text;

    def getIndexOfStartOfDocs(self,text):
        listindex=[];
        index = text.find(".I 1",0);
        count=1;
        while index >= 0:
            listindex.append(index)
            count=count+1;
            index = text.find(".I "+str(count))
        return listindex;

    def getDocIdAndWordsInIndex(self,i,j,text,listindex):
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
        return doc_id,doc_words;
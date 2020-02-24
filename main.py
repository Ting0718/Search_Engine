import os
import nltk
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import tokenizer

blackList = ['[document]', 'noscript', 'head', 'header', 'html', 'meta', 'input', 'script', 'style', 'b', 'button']

class DocID:
    def __init__(self):
        self.current_doc = 0
        self.doc_ids = dict()

    def add_to_docs(self,url: str):
        '''Assigns a doc_id to a url and adds it to the doc_ids dictionary'''
        self.doc_ids[self.current_doc] = url
        self.current_doc += 1
        return self.current_doc - 1

def readFiles(mypath:str):
    '''parsing through all the files'''
    filepaths = []
    for root, dirs, files in os.walk(mypath, topdown=True):
        for name in files: 
            filepaths.append(os.path.join(root,name))
    return filepaths

def parseFiles(filename:str):
    ''' Reads through the corpus '''
    f = open(filename, 'r')
    content = json.load(f)

    url = content["url"]
    html = content["content"]

    output = " "
    soup = BeautifulSoup(html, "lxml")
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blackList:
            output += '{} '.format(t)
    output = tokenizer.tokenize(output)
    return output


def writeFiles(inverted_index: dict, filename: str):
    '''Writes parsed information into a disk'''
    f = open(filename, "w")
    for k, v in inverted_index.items():
        f.write(k + " " + " ".join(map(str, sorted(v))) + "\n")
    f.close()

def mergeFiles():
    ''' Merging files '''

def tfidf():
    ''' calculate the tf-idf '''

def porterstemer(s:str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))



if __name__=="__main__":
    path = "ANALYST/www-db_ics_uci_edu"
    files = readFiles(path)
    d = DocID()
    a = []
    #d = {"apple": [2, 4], "aardvark": [2, 1, 7, 5]}
    for file in files:
        a.append(parseFiles(file))
    writeFiles(d,"test.txt")



import os
import nltk
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import tokenizer
from collections import defaultdict

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

def merge(list1, list2):
    answer = []
    c1, c2 = 0,0
    while(c1 < len(list1) and c2 < len(list2)):
        if list1[c1] == list2[c2]:
            answer.append(list1[c1])
            c1 += 1
            c2 += 1
        elif list1[c1] < list2[c2]:
            answer.append(list1[c1])
            c1 += 1
        else:
            answer.append(list2[c2])
            c2 += 1
    return answer + list1[c1:] + list2[c2:]

def mergeFiles(partialIndexes:list):
    ''' Merging files '''
    Index = [] # The current line of the index corresponding to the partial index. "False" if line empty
    fileStorage = []
    for x in partialIndexes: 
        with open(x,'r') as files:
            Index.append(files.readline().rstrip().split()) #reads the first line for every file
            fileStorage.append(files)

    with open('output.py','w') as output:
        while(not any(Index)): #while there are still valid lines in the files
            #Find the smallest alphabetical index word
            smallest = "ZZZZZZZZZ"
            for x in Index:
                if(x): #If x isn't False 
                    smallest = min(smallest, x[0])
            #If the thing is a smallest
            toWrite = []
            for i in range(len(Index)): 
                if(Index[i] != False and Index[i][0] == smallest):
                    merge(Index[i+1:],toWrite)
                    #Gets the next value
                    Index[i] = fileStorage[i].readline()
                    if(Index[i] == ""):
                        Index[i] = False 
                    else: 
                        Index[i] = Index[i].rstrip().split()
            #writing to file
            output.write(" ".join(toWrite) +'\n')
    


def tfidf():
    ''' calculate the tf-idf '''

def porterstemer(s:str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))



if __name__=="__main__":
    d = defaultdict(list)
    #path = "ANALYST/www-db_ics_uci_edu"

    path = "Users/shireenhsu/Desktop/ANALYST"
    files = readFiles(path)

    {"term": ["doc1", "doc2", "doc3"]}

    for file in files:
        file_id = file
        list_of_tokens = list(set(parseFiles(file)))  # remove duplicates
        for token in list_of_tokens:
            d[token].append(file)


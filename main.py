import os
import nltk
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import tokenizer
from collections import defaultdict
import threading
import indexer
import simhash

blackList = ['[document]', 'noscript', 'head', 'header', 'html', 'meta', 'input', 'script', 'style', 'b', 'button']
MAX_INDEX_LENGTH = 15000
THREADS = 3

class DocID:
    def __init__(self):
        self.current_doc = 0
        self.doc_ids = dict()

    def add_to_docs(self,url: str):
        '''Assigns a doc_id to a url and adds it to the doc_ids dictionary'''
        self.doc_ids[self.current_doc] = url
        self.current_doc += 1
        return self.current_doc - 1


class IndexerManager:
    def __init__(self,doc_id_tracker,files):
        self.current_url = 0
        self.doc_id_tracker = doc_id_tracker
        self.files = files
        self.partial_indexes = []
        self.simhashes = simhash.HashManager(0.95)

    def id_index(self,document):
        return self.doc_id_tracker.add_to_docs(document)

    def request_document(self):
        if self.current_url < len(self.files):
            self.current_url += 1
            page = self.files[self.current_url-1]
            return (page,self.doc_id_tracker.add_to_docs(page))
        else:
            return False

    def add_partial_index(self,index):
        self.partial_indexes.append(index)

    def check_simhash(self,text):
        hashed_doc = simhash.calculate_hash(text)
        if self.simhashes.find_near_duplicate(hashed_doc):
            return True
        else:
            self.simhashes.add(hashed_doc)
            return False


def readFiles(mypath:str):
    '''parsing through all the files'''
    filepaths = []
    for root, dirs, files in os.walk(mypath, topdown=True):
        for name in files: 
            filepaths.append(os.path.join(root,name))
    return filepaths

def parseFiles(filename:str):
    ''' Reads through the corpus '''
    f = open(filename, 'r', encoding = "utf-8", errors = "ignore")
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


def writeFile(inverted_index: dict, filename: str):
    '''Writes parsed information into a disk'''
    f = open(filename, "w")
    for k, v in sorted(inverted_index.items()):
        f.write(k + "," + ",".join(str(x[0]) + " " +str(x[1]) for x in sorted(v, key = lambda x: x[0])) + "\n")
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
        files = open(x,'r')
        Index.append(files.readline().rstrip().split(",")) #reads the first line for every file
        fileStorage.append(files)
    print(Index)
    print(fileStorage)
    with open('output.txt',"w") as output:
        def allFalse():
            for x in Index:
                if x != False:
                    return True
            return False
        while(allFalse()): #while there are still valid lines in the files
            #Find the smallest alphabetical index word
            smallest = "zzzzzzzzzzzzzzz"
            for x in Index:
                if(x): #If x isn't False 
                    smallest = smallest if smallest<x[0] else x[0]
            #If the thing is a smallest
            toWrite = []
            word = ""
            for i in range(len(Index)): 
                if(Index[i] != False and Index[i][0] == smallest):
                    word = Index[i][0]
                    toWrite = merge(Index[i][1:],toWrite)
                    #Gets the next value
                    Index[i] = fileStorage[i].readline()
                    if(Index[i] == ""):
                        Index[i] = False 
                    else: 
                        Index[i] = Index[i].rstrip().split(",")
            #writing to file
            toWrite.insert(0,word)
            s = ",".join(toWrite) + '\n'
            output.write(s)
        
    for files in fileStorage:
        files.close()
    


def tf(tokenized_file:[str]):
    ''' calculate the tf and return as a list of tuples of (term,frequency) '''
    terms = defaultdict(int)
    for t in tokenized_file:
        stemWord = porterstemmer(t)
        terms[stemWord] += 1
    to_ret = []
    for k,v in terms.items():
        to_ret.append((k,v))
    return to_ret

def porterstemmer(s:str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))



if __name__=="__main__":
    #path = "ANALYST/www-db_ics_uci_edu"
    path = "/Users/Scott/Desktop/DEV"
    #path = "/Users/shireenhsu/Dekstop/121_Assignment3/ANALYST"
    #path = "ANALYST"
    files = readFiles(path)
    doc_id = DocID()
    manager = IndexerManager(doc_id,files)
    get_doc_lock = threading.Lock()
    indexers = [indexer.Indexer("partial(thread" + str(i) + ").txt",manager,get_doc_lock,i) for i in range(1,THREADS+1)]
    for indexer in indexers:
        indexer.start()
    for indexer in indexers:
        indexer.join()
    mergeFiles(manager.partial_indexes)



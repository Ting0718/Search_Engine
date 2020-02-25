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


def writeFiles(inverted_index: dict, filename: str):
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
        Index.append(files.readline().rstrip().split()) #reads the first line for every file
        fileStorage.append(files)
    print(Index)
    print(fileStorage)
    with open('/Users/jason/Desktop/CMP 121 Information Retrieval/Json Merging Test/output.txt',"a") as output:
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
                        Index[i] = Index[i].rstrip().split()
            #writing to file
            toWrite.insert(0,word)
            s = " ".join(toWrite) + '\n'
            output.write(s)
        
    for files in fileStorage:
        files.close()
    


def tf(tokenized_file:[str]):
    ''' calculate the tf and return as a list of tuples of (term,frequency) '''
    terms = defaultdict(int)
    for t in tokenized_file:
        terms[t] += 1
    to_ret = []
    for k,v in terms.items():
        to_ret.append((k,v))
    return to_ret




def porterstemer(s:str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))



if __name__=="__main__":
    d = defaultdict(list)
    #path = "ANALYST/www-db_ics_uci_edu"

    #path = "/Users/Scott/Desktop/DEV"
    path = "ANALYST"
    files = readFiles(path)
    doc_id = DocID()
    for file in files:
        list_of_tokens = tf(parseFiles(file))  # remove duplicates
        id_num = doc_id.add_to_docs(file)
        for token in list_of_tokens:
            d[token[0]].append((id_num,token[1]))
        print(id_num)
    writeFiles(d,"testA.txt")

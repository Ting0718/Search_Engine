import os
import nltk
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import tokenizer

blackList = ['[document]', 'noscript', 'head', 'header', 'html', 'meta', 'input', 'script', 'style', 'b', 'button']

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


def writeFiles(inverted_index: dict, file: "JSON file"):
    '''Writes parsed information into a disk'''
    j = json.dumps(dict, sort_keys=True)
    f = open(file, "w")
    f.write(j)
    f.close()


def mergeFiles(partialIndexes:list):
    ''' Merging files '''
    Index = [] # The current line of the index corresponding to the partial index. "False" if line empty
    for x in partialIndexes: 
        with open(x,'r') as files:
            Index.append(files.readline().rstrip().split()) #reads the first line for every file
    
    while(not any(Index)): #while there are still valid lines in the files
        #Find the smallest alphabetical index word
        smallest = ''
        for x in Index:
            if(x): #If x isn't False 
                smallest = min(smallest, x)
        #If the thing is a smallest
        

        
    


def tfidf():
    ''' calculate the tf-idf '''

def porterstemer(s:str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))

if __name__=="__main__":
    path = "ANALYST"
    files = readFiles(path)
    for file in files:
        print(parseFiles(file))



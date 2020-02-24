import os
import nltk
from nltk.stem import PorterStemmer
import json

def readFiles(mypath:str):
    '''parsing through all the files'''
    filepaths = []
    for root, dirs, files in os.walk(mypath, topdown=True):
        for name in files: 
            filepaths.append(os.path.join(root,name))
    return filepaths

def parseFiles(filename:str):
    ''' Reads through the corpus '''


def writeFiles(inverted_index: dict, file: "JSON file"):
    '''Writes parsed information into a disk'''
    j = json.dumps(dict, sort_keys=True)
    f = open(file, "w")
    f.write(j)
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
    path = "/Users/jason/Desktop/ANALYST"
    files = readFiles(path)



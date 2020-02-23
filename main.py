from os import listdir
from os.path import isfile,join
import nltk
from nltk.stem import PorterStemmer
import json


def readFiles(mypath:str):
    '''parsing through all the files'''
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]


def parseFiles(filename:str):
    ''' Reads through the corpus '''


def writeFiles(inverted_index: dict, file: "JSON file"):
    '''Writes parsed information into a disk'''
    j = json.dumps(dict)
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
    path = ''
    files = readFiles("/Users/jason/Desktop/ANALYST")
    print(files)



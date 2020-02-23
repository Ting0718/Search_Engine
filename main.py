import os

def readFiles(mypath:str):
    '''parsing through all the files'''
    filepaths = []
    for root, dirs, files in os.walk(mypath, topdown=True):
        for name in files: 
            filepaths.append(os.path.join(root,name))
    return filepaths

def parseFiles(filename:str):
    ''' Reads through the corpus '''


def writeFiles():
    '''Writes parsed information onto the disk'''

def mergeFiles():
    ''' Merging files '''

def tfidf():
    ''' calculate the tf-idf '''

def porterstemer():
    '''porter stemmer'''

if __name__=="__main__":
    path = ''
    files = readFiles("/Users/jason/Desktop/ANALYST")



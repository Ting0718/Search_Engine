import os
import nltk
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import tokenizer

blackList = ['[document]', 'noscript', 'head', 'header',
             'html', 'meta', 'input', 'script', 'style', 'b', 'button']


def readFiles(mypath: str):
    '''parsing through all the files'''
    filepaths = []
    for root, dirs, files in os.walk(mypath, topdown=True):
        for name in files:
            filepaths.append(os.path.join(root, name))
    return filepaths


def parseFiles(filename: str):
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

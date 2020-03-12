from nltk.stem import PorterStemmer
import os
import time
import json
import binarySearch
from collections import defaultdict
import math

def porterstemmer(s: str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))

def SetOfDocId(line):
    '''return a list of doc for a term'''
    s = set()
    for i in line:
        s.add(int(i.split()[0]))
    return s

def getToken(line: str) -> str:
    '''get the first token in each posting'''
    return line.split(",")[0]

def mergePostings(list_of_posting: list):
    '''merge a list of postings in inverted list'''
    if len(list_of_posting) == 0:
        return []
    return set.intersection(*list_of_posting)

def translate_ids(id_dict:dict,id_list):
    ret = []
    for id in id_list:
        ret.append(id_dict[str(id)])
    return ret

def queryScore(term:str, queries:list) -> float:
    ''' Calculates the Wt,q for each query'''
    tf = 0
    for x in queries:
        if x == term:
            tf += 1
    return tf/len(queries)

def Score(queries:list, docIds:dict) -> list:
    index = json.load(open("indexindex.json",'r'))
    keys = sorted(index.keys())
    Scores = defaultdict(int)
    Magnitude = defaultdict(int)
    doc_length = len(docIds.keys())
        #Retrieves the terms
    with open("output.txt",'r') as f:
        list_docIDs = []
        for x in queries:
            q_score = queryScore(x,queries)
            list_of_posting = []
            closest = binarySearch.search(keys,x)
            offset = index[keys[closest]]
            f.seek(offset)
            for y in range(20):
                line = f.readline()
                line = line.split(',')
                if(line[0] == x):
                    list_of_posting = line[1:]
                    list_docIDs.append(SetOfDocId(line[1:]))
                    break
            f.seek(0)
            for posting in list_of_posting:
                temp = posting.split()
                doc = temp[0]
                tf = int(temp[1])
                Scores[doc] += q_score * ((1 + math.log10(tf)) * math.log10(doc_length/len(list_of_posting)))
        docSet = mergePostings(list_docIDs)
        """To Do: binary search implementation of this"""
       
    print(sorted(Scores.items(), key=lambda item: item[1],reverse=True)[:50])
    return [k for k, v in sorted(Scores.items(), key=lambda item: item[1],reverse=True)]
            


def search_result(queries:str, number_of_results:int): 
    start_time = time.time()
    queries = queries.split()
    queries = [porterstemmer(x) for x in queries]
    docIds = json.load(open("docID.json",'r'))
    # index = json.load(open("indexindex.json",'r'))
    # keys = sorted(index.keys())
    # list_of_posting = []

    # with open("output.txt",'r') as f:
    #     for x in queries:
    #         closest = binarySearch.search(keys,x)
    #         offset = index[keys[closest]]
    #         f.seek(offset)
    #         for y in range(20):
    #             line = f.readline()
    #             if(line.split(',')[0] == x):
    #                 list_of_posting.append(SetOfDocId(line))
    #                 break
    #         f.seek(0)
    results = Score(queries,docIds)
    results = translate_ids(docIds,results[:number_of_results]) # return the first 5 URLst
    return results + [time.time()-start_time]


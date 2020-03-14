from nltk.stem import PorterStemmer
import os
import time
import json
import binarySearch
from collections import defaultdict
import math
from collections import namedtuple
from sklearn.metrics.pairwise import cosine_similarity
import itertools
import numpy as np

Term = namedtuple("Term", "term docID tf idf")

def porterstemmer(s: str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))


def SetOfDocId_tf(line):
    '''return a list of doc for a term'''
    s = set()
    for i in line:
        s.add(i.split()[0])
    return s

def SetOfDocId(line):
    l = set()
    word = line.split(",")[0]
    for i in line.split(",")[1:]:
        d = i.split()
        l.add((word,int(d[0]),d[1]))
    return l

def SetOfDocIdWithoutTf(line):
    '''return a set of doc for a term'''
    s = set()
    for i in line.split(",")[1:]:
        s.add(i.split()[0])
    return s

def getToken(line: str) -> str:
    '''get the first token in each posting'''
    return line.split(",")[0]

def mergePostings(list_of_posting: list):
    '''merge a list of postings in inverted list'''
    if len(list_of_posting) == 0:
        return []
    return list(set.intersection(*list_of_posting))

def translate_ids(id_dict:dict,id_list):
    ret = []
    for id in id_list:
        ret.append(id_dict[str(id)])
    return ret

def getTfInADoc(line: str, docId:int): # need to use term to find the line later 
    for p in line.split(",")[1:]:
        if int(p.split()[0]) == docId:
            return int(p.split()[1])

def getIdf(line: str): # get the idf corresponding to the line
    return len(line.split(","))-1


def tf_for_query(query:str, queries:list):
    s = 0
    for i in queries:
        if i == query:
            s += 1
    return s

def Score_for_doc(query,tf,idf,total_docs)-> ["a list of tf-idf for queries"]:
    '''calculate the tf-idf here first'''
    tf = 1 + math.log10(tf)
    idf = math.log10(total_docs/idf)
    return tf * idf

def score_for_query(query:str,tf:int, line:str,total_docs):
    tf = 1 + math.log10(tf)
    idf = math.log10(total_docs/getIdf(line))
    return tf*idf


def search_result_cosine(queries: list, number_of_results: int) -> list:
    start_time = time.time()
    index = json.load(open("indexindex.json",'r'))
    keys = sorted(index.keys())
    queries = [porterstemmer(x) for x in queries]
    #Retrieves the termss
    query_vector = defaultdict(str)
    d = defaultdict(list)
    doc_scores = defaultdict(list)
    cos_sim = defaultdict(set)
    docIds = json.load(open("docID.json", 'r'))
    total_docs = len(docIds.keys())

    '''need to do the intersection too'''
    with open("output.txt",'r') as f:
        for x in queries:
            closest = binarySearch.search(keys,x)
            offset = index[keys[closest]]
            f.seek(offset)
            for y in range(20):
                line = f.readline()
                line2 = line.split(',')
                if(line2[0] == x):
                    idf = len(line2) - 1
                    query_vector[x] = score_for_query(x, tf_for_query(x, queries), line,total_docs)
                    for i in SetOfDocId(line):
                       d[i[1]].append(Term(x,i[1],i[2],idf))
            f.seek(0)

    for i in list(d):
        if len(d[i]) != 2:
            del d[i]
        for term in d[i]:
           doc_scores[i].append(Score_for_doc(term.term,int(term.tf),term.idf,total_docs))
    
    for doc in doc_scores:
        q1 = [list(query_vector.values())]
        d1 = [(doc_scores[doc])]
        cos_sim[doc] = cosine_similarity(q1, d1)
    
    l = [i[0] for i in sorted(cos_sim.items(),key=lambda item: item[1], reverse=True)[:number_of_results]]
    return translate_ids(docIds, l) + [time.time()-start_time]


def queryScore(term: str, queries: list) -> float:
    ''' Calculates the Wt,q for each query'''
    tf = 0
    for x in queries:
        if x == term:
            tf += 1
    return tf/len(queries)



def Score(queries: list, docIds: dict, number_of_results:int) -> list:
    index = json.load(open("indexindex.json", 'r'))
    keys = sorted(index.keys())
    Scores = defaultdict(int)
    Magnitude = defaultdict(int)
    doc_length = len(docIds.keys())
    #Retrieves the terms
    with open("output.txt", 'r') as f:
        list_docIDs = []
        for x in queries:
            q_score = queryScore(x, queries)
            list_of_posting = []
            closest = binarySearch.search(keys, x)
            offset = index[keys[closest]]
            f.seek(offset)
            for y in range(20):
                line = f.readline()
                line = line.split(',')
                if(line[0] == x):
                    list_of_posting = line[1:]
                    list_docIDs.append(SetOfDocId_tf(line[1:]))
                    break
            f.seek(0)
            for posting in list_of_posting:
                temp = posting.split()
                doc = temp[0]
                tf = int(temp[1])
                Scores[doc] += q_score * ((1 + math.log10(tf)) * math.log10(doc_length/len(list_of_posting)))

    docSet = mergePostings(list_docIDs)  # this is the intersection

    disjunction = {k for k, v in sorted(
        Scores.items(), key=lambda item: item[1], reverse=True)} - set(docSet) # this is the disjunction

    if len(docSet) < number_of_results: 
        disjunction_num = number_of_results - len(docSet) 
        disjunction_truncate = list(disjunction)[:disjunction_num]
        return docSet + disjunction_truncate

    elif len(docSet) >= number_of_results:
        return docSet


def search_result(queries: str, number_of_results: int):
    start_time = time.time()
    queries = queries.split()
    queries = [porterstemmer(x) for x in queries]
    docIds = json.load(open("docID.json", 'r'))
    results = Score(queries, docIds, number_of_results)
    # return the first 5 URLst
    results = translate_ids(docIds, results[:number_of_results])
    return results + [time.time()-start_time]


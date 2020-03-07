from nltk.stem import PorterStemmer
import os
import time
import json
import binarySearch

def porterstemmer(s: str):
    '''porter stemmer'''
    porter = PorterStemmer()
    return (porter.stem(s))

def SetOfDocId(line: str):
    '''return a list of doc for a term'''
    s = set()
    for i in line.split(',')[1:]:
        s.add(int(i.split()[0]))
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

def search_result(queries:str):
    queries = queries.split()
    queries = [porterstemmer(x) for x in queries]
    start_time = time.time()
    docIds = json.load(open("docID.json",'r'))
    index = json.load(open("indexindex.json",'r'))
    keys = sorted(index.keys())
    list_of_posting = []

    with open("output.txt",'r') as f:
        for x in queries:
            closest = binarySearch.search(keys,x)
            print(keys[closest])
            offset = index[keys[closest]]
            f.seek(offset)
            for x in range(20):
                line = f.readline()
                #print(line)
                if(line.split(',')[0] == x):
                    print("match")
                    list_of_posting.append(SetOfDocId(line))
                    break
            print("New Term")
            f.seek(0)
    print(list_of_posting)
    top_five = translate_ids(docIds,mergePostings(list_of_posting)[:5]) # return the first 5 URLst
    print(top_five)
    return top_five + [time.time()-start_time]
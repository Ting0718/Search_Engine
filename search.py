from nltk.stem import PorterStemmer
import os
import time
import json

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
    return list(set.intersection(*list_of_posting))

def translate_ids(id_dict:dict,id_list):
    ret = []
    for id in id_list:
        ret.append(id_dict[str(id)])
    return ret

if __name__ == "__main__":

    docIds = json.load(open("docID.json",'r'))
    split = ["9",'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    files = {}
    for x in split:
        files[x] = f"outputs/output{x}.txt"

    queries = [porterstemmer(x) for x in input("Enter Search: ").split()]
    start_time = time.time()
    q = sorted(queries)
    list_of_posting = []
    ''' Time could be improved if you don't open the file evertime, or open it once for each start letter.'''
    fileStorage = []
    for query in q:
        with open(files[query[0]],'r') as f:
            for line in f:
                if getToken(line) == query:
                    list_of_posting.append(SetOfDocId(line))
    # f = open("output.txt",'r')
    # index = 0
    # for line in f:
    #     if getToken(line) == q[index]:
    #         list_of_posting.append(SetOfDocId(line))
    #         index += 1
    #         if(index >= len(q)):
    #             break
    #         stemmed = q[index]
    # f.close()
    
    top_five = translate_ids(docIds,mergePostings(list_of_posting)[:5]) # return the first 5 URLst
    print(top_five)
    print("--- %s seconds ---" % (time.time() - start_time))

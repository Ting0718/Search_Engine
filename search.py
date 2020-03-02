from nltk.stem import PorterStemmer
import os
import time

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

if __name__ == "__main__":

    outputFile = "output.txt"
    f = open(outputFile, 'r')

    queries = input("Enter Search: ").split()
    start_time = time.time()
    q = sorted(queries)
    list_of_posting = []

    index = 0
    try:
        stemmed = porterstemmer(queries[index])
        print(stemmed)
        for line in f:
            if getToken(line) == stemmed:
                list_of_posting.append(SetOfDocId(line))
                index += 1
                stemmed = porterstemmer(queries[index])
                print(stemmed)
    except IndexError:
        pass

    ''' retreive the first 5 URLs '''  # need to sort based on the tf-idf
    
    top_five = mergePostings(list_of_posting)[:5]  # return the first 5 URLst
    print(top_five)

    print("--- %s seconds ---" % (time.time() - start_time))
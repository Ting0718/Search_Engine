import os
import nltk
from nltk.stem import PorterStemmer
import json
from bs4 import BeautifulSoup
import tokenizer
from collections import defaultdict
import threading
import indexer
import simhash

blackList = ['[document]', 'noscript', 'head', 'header',
             'html', 'meta', 'input', 'script', 'style', 'b', 'button']
MAX_INDEX_LENGTH = 15000 #max length of indexes before merge
TOTAL_DOCUMENTS = 55392  # need to change
TOAL_TOKENS = 1256389
THREADS = 3 #how many threads will be used to scan documents


class DocID:
    '''
    class to keep track of document Id numbers
    Add to docs will add a document to a local dictionary of id:url and will return the id number used for that url
    '''
    def __init__(self):
        self.current_doc = 0
        self.doc_ids = dict()

    def add_to_docs(self, url: str):
        '''Assigns a doc_id to a url and adds it to the doc_ids dictionary then returns the id number assigned'''
        self.doc_ids[self.current_doc] = url
        self.current_doc += 1
        return self.current_doc - 1

    def write_doc_id(self,filename="docid.json"):
        '''writes the content of docId dictionary to a json file'''
        with open(filename,'w') as out:
            json.dump(self.doc_ids,out)



class IndexerManager:
    '''
    class to manage indexer threads, contains simhash manager, a list of partial indexes and a document id tracker
    also contains the current url numerically indexed
    '''
    def __init__(self, doc_id_track, files):
        self.current_url = 0
        self.doc_id_tracker = doc_id_track
        self.files = files
        self.partial_indexes = []
        self.simhashes = simhash.HashManager(0.95)

    def id_index(self, document):
        '''adds doc from a thread to the id tracker'''
        return self.doc_id_tracker.add_to_docs(document)

    def request_document(self):
        '''method to be called by thread to get a new url, returns the url content'''
        if self.current_url < len(self.files):
            self.current_url += 1
            page = self.files[self.current_url-1]
            return (page, self.doc_id_tracker.add_to_docs(page)) #returns (docContent,docID)
        else:
            return False

    def add_partial_index(self, index):
        ''' adds the filename of a written partial index to partial index list'''
        self.partial_indexes.append(index)

    def check_simhash(self, text):
        '''calculate and check whether there is a near duplicate of the text'''
        hashed_doc = simhash.calculate_hash(text)
        if self.simhashes.find_near_duplicate(hashed_doc):
            return True
        else:
            self.simhashes.add(hashed_doc)
            return False



def readFiles(mypath: str):
    '''parses through all files in the folder and returns a list of their file paths'''
    filepaths = []
    for root, dirs, files in os.walk(mypath, topdown=True):
        for name in files:
            filepaths.append(os.path.join(root, name))
    return filepaths


def parseFiles(filename: str):
    ''' Reads through the corpus '''
    f = open(filename, 'r', encoding="utf-8", errors="ignore")
    content = json.load(f)

    url = content["url"]
    html = content["content"] #splits the content fromurl

    output = " "
    soup = BeautifulSoup(html, "lxml")
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blackList: #removes blacklisted tags from the considered content
            output += '{} '.format(t)
    output = tokenizer.tokenize(output) #tokenizes the output
    return output


def writeFile(inverted_index: dict, filename: str):
    '''Writes parsed information into a disk'''
    f = open(filename, "w")
    for k, v in sorted(inverted_index.items()):
        f.write(k + "," + ",".join(str(x[0]) + " " + str(x[1])
                                   for x in sorted(v, key=lambda x: x[0])) + "\n")
    f.close()


def merge(list1, list2):
    answer = []
    c1, c2 = 0, 0
    while(c1 < len(list1) and c2 < len(list2)):
        if list1[c1] == list2[c2]:
            answer.append(list1[c1])
            c1 += 1
            c2 += 1
        elif list1[c1] < list2[c2]:
            answer.append(list1[c1])
            c1 += 1
        else:
            answer.append(list2[c2])
            c2 += 1
    return answer + list1[c1:] + list2[c2:]


def mergeFiles(partialIndexes: list):
    ''' Merging files '''
    Index = []  # The current line of the index corresponding to the partial index. "False" if line empty
    fileStorage = []
    for x in partialIndexes:
        files = open(x, 'r')
        # reads the first line for every file
        Index.append(files.readline().rstrip().split(","))
        fileStorage.append(files)
    #print(Index)
    #print(fileStorage)
    with open('output.txt', "w") as output:
        def allFalse():
            for x in Index:
                if x != False:
                    return True
            return False
        while(allFalse()):  # while there are still valid lines in the files
            #Find the smallest alphabetical index word
            smallest = "zzzzzzzzzzzzzzz"
            for x in Index:
                if(x):  # If x isn't False
                    smallest = smallest if smallest < x[0] else x[0]
            #If the thing is a smallest
            toWrite = []
            word = ""
            for i in range(len(Index)):
                if(Index[i] != False and Index[i][0] == smallest):
                    word = Index[i][0]
                    toWrite = merge(Index[i][1:], toWrite)
                    #Gets the next value
                    Index[i] = fileStorage[i].readline()
                    if(Index[i] == ""):
                        Index[i] = False
                    else:
                        Index[i] = Index[i].rstrip().split(",")
            #writing to file
            toWrite.insert(0, word)
            s = ",".join(toWrite) + '\n'
            output.write(s)

    for files in fileStorage:
        files.close()

# def splitFiles(output:str):
#     '''Splits the main output.txt into other smaller text files and puts those file names into a dictionary which it returns.'''



def tf(tokenized_file: [str]):
    ''' calculate the tf and return as a list of tuples of (term,frequency) '''
    terms = defaultdict(int)
    for t in tokenized_file:
        stemWord = porterstemmer(t)
        terms[stemWord] += 1
    to_ret = []
    for k, v in terms.items():
        to_ret.append((k, v))
    return to_ret

def idf(s: str):  # will do later
    '''IDF(t) = log_e(Total number of documents / Number of documents with term t in it).'''

if __name__ == "__main__":
    #path = "/Users/Scott/Desktop/DEV"
    #path = "/Users/shireenhsu/Desktop/121_Assignment3/DEV"
    #path = "/Users/jason/Desktop/ANALYST"


    '''Actually reading the JSON and merging the files into one output.txt'''
    path = input("Enter Path Name: ")

    files = readFiles(path)
    doc_id = DocID()
    manager = IndexerManager(doc_id, files)
    get_doc_lock = threading.Lock()
    simhash_lock = threading.Lock()
    indexers = [indexer.Indexer("partial(thread" + str(i) + ").txt", manager, #creates and instntiates indexers based on THREADS constant
                                get_doc_lock, simhash_lock, i) for i in range(1, THREADS+1)]
    for indexer in indexers:
        indexer.start() #starts all indexer threads
    for indexer in indexers:
        indexer.join() #waits for all indexer threads
    mergeFiles(manager.partial_indexes)
   
    

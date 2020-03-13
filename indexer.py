import main
import threading
from collections import defaultdict
import nltk
from nltk.corpus import stopwords

class Indexer(threading.Thread):
    '''class inhertis from thread, used to index with multiple threads'''
    def __init__(self,write_file:str,manager, request_document_lock,simhash_lock,thread):
        self.indexed = 0
        self.file_name = write_file
        self.request_document_lock = request_document_lock
        self.simhash_lock = simhash_lock
        self.manager = manager
        self.index = defaultdict(list)
        self.files_written = 0
        self.thread_id = thread
        super().__init__(daemon = True)


    def run(self):
        while True:
            if self.indexed == main.MAX_INDEX_LENGTH: #if it has indexed the max number of files in memory it dumps to a partial index
                self.dump_index()
            else:
                self.request_document_lock.acquire()
                page = self.manager.request_document()
                self.request_document_lock.release()
                if page == False:
                    self.dump_index()
                    return
                url,html,importants = main.parseFiles(page)
                list_of_tokens = main.tf(html,importants)
                self.simhash_lock.acquire()
                if len(list_of_tokens) > 25 and not self.manager.check_simhash(list_of_tokens): #if < 25 tokens or simhash found ignores page
                    index_num = self.manager.docid_file_to_url(url)
                    self.simhash_lock.release()
                    for token in list_of_tokens:
                        self.index[token[0]].append((index_num, token[1])) #appends this doc and tf to all tokens the doc has
                    self.indexed += 1
                    print("THREAD: " + str(self.thread_id) + " INDEXED: " + page + " " + str(index_num))
                else:
                    self.simhash_lock.release()
                    print("THREAD: " + str(self.thread_id) + " SIMHASH SKIPPED: " + page)


    def dump_index(self):
        '''writes what this indexer has into a partial index and adds it to the list of partials'''
        main.writeFile(self.index,self.file_name)
        self.manager.add_partial_index(self.file_name)
        self.index.clear()
        self.files_written += 1
        self.indexed = 0
        self.file_name = self.file_name.split(".")[0] + str(self.files_written) + ".txt"


import main
import threading
#create indexer class to put together it's own index on a separate thread
#to do: convert the url getter to be threadsafe
#change the __name__ in main.py to set up multiple threads
#set up a termination function in main for when out of pages
from collections import defaultdict
class Indexer(threading.Thread):
    def __init__(self,write_file:str,manager, request_document_lock,thread):
        self.indexed = 0
        self.file_name = write_file
        self.request_document_lock = request_document_lock
        self.manager = manager
        self.index = defaultdict(list)
        self.files_written = 0
        self.thread_id = thread
        super().__init__(daemon = True)


    def run(self):
        while True:
            if self.indexed == main.MAX_INDEX_LENGTH:
                self.dump_index()
            else:
                self.request_document_lock.acquire()
                page = self.manager.request_document()
                self.request_document_lock.release()
                if page == False:
                    self.dump_index()
                    return
                list_of_tokens = main.tf(main.parseFiles(page[0]))
                for token in list_of_tokens:
                    self.index[token[0]].append((page[1], token[1]))
                self.indexed += 1
                print("THREAD: " + str(self.thread_id) + " INDEXED: " + page[0] + " " + str(page[1]))


    def dump_index(self):
        main.writeFile(self.index,self.file_name)
        self.manager.add_partial_index(self.file_name)
        self.index.clear()
        self.files_written += 1
        self.indexed = 0
        self.file_name = self.file_name.split(".")[0] + str(self.files_written) + ".txt"



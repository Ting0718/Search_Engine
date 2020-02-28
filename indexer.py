import main
import threading
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

                if len(list_of_tokens) > 25 and not self.manager.check_simhash(list_of_tokens):
                    for token in list_of_tokens:
                        self.index[token[0]].append((page[1], token[1]))
                    self.indexed += 1
                    print("THREAD: " + str(self.thread_id) + " INDEXED: " + page[0] + " " + str(page[1]))
                else:
                    print("THREAD: " + str(self.thread_id) + " SIMHASH SKIPPED: " + page[0] + " " + str(page[1]))


    def dump_index(self):
        main.writeFile(self.index,self.file_name)
        self.manager.add_partial_index(self.file_name)
        self.index.clear()
        self.files_written += 1
        self.indexed = 0
        self.file_name = self.file_name.split(".")[0] + str(self.files_written) + ".txt"


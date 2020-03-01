import linecache
import time

print(linecache.getline("term_index.txt", 200000))
print(linecache.getline("term_index.txt", 1000000))

start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))

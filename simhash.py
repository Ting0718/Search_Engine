import hashlib


def calculate_hash(document):
    '''calculates the hash value for a document in 128 bits'''
    hash_freq = []
    for token in document:
        hashed = bin(int(hashlib.md5(token[0].encode("utf-8")).hexdigest(), 16))[2:]
        while len(hashed) != 128:
            hashed += "0"
        hash_freq.append ((hashed,token[1]))
    if len(hash_freq) > 0:
        doc_length = len(hash_freq[0][0])
    else:
        doc_length = 0
    output = ""
    for index in range(doc_length):
        sum = 0
        for term in hash_freq:
            if term[0][index] == "1":
                sum += term[1]
            else:
                sum -= term[1]
        if sum > 0:
            output += "1"
        else:
            output += "0"
    return int(output,2)

class HashManager:
    '''class to keep track of simhashes, and check for near duplicates'''
    def __init__(self,thresh = 0.75): #default threshold to 75%, threshold can be given as int or as float
        self.hashes = set()
        if thresh > 0.99:
            self.threshold = thresh/100
        else:
            self.threshold = thresh

    def add(self,simhash):
        self.hashes.add(simhash)

    def find_near_duplicate(self,simhash):
        '''returns true if a near duplicate exists'''
        most = 0
        for h in self.hashes:
            most = max(most,self.compare(simhash,h))
            if most > self.threshold:
                return True
        return most > self.threshold

    def compare(self,simhash1,simhash2):
        '''helper for finding duplicates, returns the number of bits that are the same'''
        combined = -1*~(simhash1^simhash2) #sets bits to 1 if they are both 1 or both 0 in both hashes
        count = 0
        while (combined): #this section of code found https://www.geeksforgeeks.org/count-set-bits-in-an-integer/, finds number of active bits
            combined &= (combined - 1)
            count += 1
        return count/128




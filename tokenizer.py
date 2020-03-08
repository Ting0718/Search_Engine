import re
import sys
from collections import defaultdict

def tokenize(text: str) -> [str]:
    """
    Accepts a string representing a file path as input and returns a list of all lowercase, alphanumeric tokens that
    are separated by spaces or non-alphanumeric characters in the original text.
    if the file path does not exist returns an empty list
    """
    text = re.sub(r"[^a-zA-Z0-9]+"," ",text)
    text = text.strip()
    #text = re.sub(r"[\w]+"," ",text)
    text = text.lower()
    return text.split()

def computeWordFrequencies(tokens:[str]) -> {str:int}:
    """
     converts a list of tokens into a dictionary that maps token:frequency
    """
    freq = defaultdict(int)
    for t in tokens:
        freq[t] += 1
    return dict(freq)

def print_tokens(tokens:{str:int}):
    """
    prints the frequency dictionary using the format <token> -> <frequency> from greatest frequency to lowest
    """
    for t,f in sorted(tokens.items(),key = lambda x: x[1],reverse = True):
        print(str(t)+" -> "+str(f))




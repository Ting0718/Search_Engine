import re
import sys
from collections import defaultdict

stopwords = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with',
             'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's',
             'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through',
             'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to',
             'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
             'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself',
             'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom',
             't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}


def tokenize_remove_stopwords(text: str) -> [str]:
    '''tokenize removing all the stop words'''
    text_tokens = tokenize(text)
    return [token for token in text_tokens if token not in stopwords]

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




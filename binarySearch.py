import math

def search(content:list,item, max = 26):
    ''' searches content, a list which is assumed to be sorted, for item. if item is not found after the max iterations
    it returns the location of the closest item to value, if it is found returns the location of item
    '''
    iterations = 0
    left = 0
    right = len(content)-1
    mid = left + int((right - left) / 2)
    while iterations <= max and content[mid] != item:
        if left == right:
            return left
        elif content[mid] < item:
            left = mid+1
            mid = left+int((right-left)/2)
        else:
            right = mid-1
            mid = left + int((right - left) / 2)
        iterations += 1
    if content[mid] == item:
        return mid
    return mid-1


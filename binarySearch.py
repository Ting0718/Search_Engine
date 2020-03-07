import math

def search(content:list,item, max_iterations = 26):
    ''' searches content, a list which is assumed to be sorted, for item. if item is not found after the max iterations
    it returns the location of the closest item to value, if it is found returns the location of item
    '''
    iterations = 0
    left = 0
    right = len(content)-1
    mid = left + int((right - left) / 2)
    while iterations <= max_iterations and content[mid] != item:
        if content[mid] == item:
            return mid
        if left == right:
            return left
        elif item < content[mid]:
            right = mid
            mid = left+int((right-left)/2)
        else:
            left = mid
            mid = left + int((right - left) / 2)
        iterations += 1
    if item < content[mid]:
        return mid+1
    return mid


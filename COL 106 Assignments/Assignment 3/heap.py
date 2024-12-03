'''
Python Code to implement a heap with general comparison function
'''

class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value


def comp(node1, node2):
    if node1.key<node2.key:
        return True
    return False

class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        self.compare = comparison_function
        self.heap = []
        for i in init_array:
            self.heap.append(i)

        for i in range(len(self.heap)//2-1, -1, -1):
            left = 2*i+1
            right = 2*i+2
            j = len(self.heap)
            if right<len(self.heap):
                if self.compare(self.heap[right], self.heap[left]):
                    if self.compare(self.heap[right], self.heap[i]):
                        self.heap[right], self.heap[i] = self.heap[i], self.heap[right]
                        j = right

                else:
                    if self.compare(self.heap[left], self.heap[i]):
                        self.heap[left], self.heap[i] = self.heap[i], self.heap[left]
                        j = left
            else:
                if left<len(self.heap):
                    if self.compare(self.heap[left], self.heap[i]):
                        self.heap[left], self.heap[i] = self.heap[i], self.heap[left]
                        j = left


            while j<len(self.heap):
                left = 2*j+1
                right = 2*j+2
                if right<len(self.heap):
                    if self.compare(self.heap[right], self.heap[left]):
                        if self.compare(self.heap[right], self.heap[j]):
                            self.heap[right], self.heap[j] = self.heap[j], self.heap[right]
                            j = right
                            continue

                    else:
                        if self.compare(self.heap[left], self.heap[j]):
                            self.heap[left], self.heap[j] = self.heap[j], self.heap[left]
                            j = left
                            continue
                else:
                    if left<len(self.heap):
                        if self.compare(self.heap[left], self.heap[j]):
                            self.heap[left], self.heap[j] = self.heap[j], self.heap[left]
                            j = left
                            continue
                j = len(self.heap)
        # Write your code here


    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.heap.append(value)
        i = len(self.heap)-1
        while i>0:
            parent = (i-1)//2
            if self.compare(self.heap[i], self.heap[parent]):
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''

        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        # Swap the root with the last element and remove the last element
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        value = self.heap.pop()

        # Heapify down from the root
        i = 0
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < len(self.heap) and self.compare(self.heap[left], self.heap[smallest]):
                smallest = left
            if right < len(self.heap) and self.compare(self.heap[right], self.heap[smallest]):
                smallest = right

            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break

        return value




    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        # Write your code here
        if len(self.heap)==0:
            return None
        return self.heap[0]
    def size(self):
        return len(self.heap)

    
    # You can add more functions if you want to
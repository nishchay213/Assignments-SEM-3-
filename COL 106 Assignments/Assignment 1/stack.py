
class Stack:
    
    def __init__(self) -> None:
        #YOU CAN (AND SHOULD!) MODIFY THIS FUNCTION
        self.data = []
        
        pass
    def is_empty(self):
        return len(self.data)==0
        
    def push(self, e):
        self.data.append(e)
    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self.data.pop()
    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self.data[-1]
    def con_to_list(self):
        return self.data
    # You can implement this class however you like
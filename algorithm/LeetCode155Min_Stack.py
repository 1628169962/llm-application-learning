class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val):
        self.stack.append(val)
        if len(self.min_stack) == 0:
            self.min_stack.append(val)
        else:
            current_min = self.min_stack[-1]
            if val <= current_min:
                self.min_stack.append(val)
            else:
                self.min_stack.append(current_min)
    def pop(self):
        self.stack.pop()
        self.min_stack.pop()
    def top(self):
        return self.stack[-1]
    def getMin(self):
        return self.min_stack[-1]

stack = MinStack()
stack.push(-2)
stack.push(0)
stack.push(-3)

print(stack.getMin())

stack.pop()

print(stack.top())

print(stack.getMin())
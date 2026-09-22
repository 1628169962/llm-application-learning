def is_valid(s):
    stack = []
    for x in s:
        if x == "{" or  x == "[" or x == "(":
            stack.append(x)
        elif x == "}" :
            top = len(stack)
            if top == 0:
                return False
            if stack[top - 1] == "{":
                stack.pop()
            else:
                return False
        elif x == "]" :
            top = len(stack)
            if top == 0:
                return False
            if stack[top - 1] == "[":
                stack.pop()
            else:
                return False        
        elif x == ")" :
            top = len(stack)
            if top == 0:
                return False
            if stack[top - 1] == "(":
                stack.pop()
            else:
                return False 
    if len(stack) != 0:
        return False
    return True


print(is_valid("()"))
print(is_valid("()[]{}"))
print(is_valid("(]"))
print(is_valid("([)]"))
print(is_valid("{[]}"))
print(is_valid("]"))
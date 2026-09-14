s = "A man, a plan, a canal: Panama"
clean =""
for char in s:
    if char.isalnum():
        clean = clean + char
print(clean)
clean = clean.lower()
reversed_clean = clean[::-1]
if clean == reversed_clean:
    print(True)
else:
    print(False)

def is_palindrome(s):
    clean = ""
    for char in s:
        if char.isalnum():
            clean = clean + char
    clean = clean.lower()

    left = 0
    right = len(clean) - 1
    while left < right:
        if clean[left] != clean[right]:
            return False
        else:
            left +=1
            right -=1
    return True
def is_palindrome(s):
    left = 0
    right = len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left +=1
        elif not s[right].isalnum():
            right -=1
        elif s[left].isalnum() and s[right].isalnum():
            if s[left].lower() != s[right].lower():
                return False
            else:
                left +=1
                right -=1
    return True

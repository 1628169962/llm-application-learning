s = "anagram"
t = "nagaram"
def is_anagram(s, t):
    count_s = {}
    count_t = {}
    for c in s:
        count_s[c] = count_s.get(c,0) + 1
    for c in t:
        count_t[c] = count_t.get(c,0) + 1
    if count_s == count_t:
        return True
    else:
        return False

print(is_anagram("anagram", "nagaram"))
print(is_anagram("rat", "car"))
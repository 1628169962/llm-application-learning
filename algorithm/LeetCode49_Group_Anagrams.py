strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
def group_anagrams(strs):
    groups = {}
    for s in strs:
        key = "".join(sorted(s))
        groups.setdefault(key,[]).append(s)

    return list(groups.values())
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
def group_anagrams(strs):

    groups = {}
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord("a")] += 1
        key = tuple(counts)
        groups.setdefault(key,[]).append(s)

    return list(groups.values())
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

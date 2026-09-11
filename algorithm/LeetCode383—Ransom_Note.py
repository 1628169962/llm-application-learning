magazine = "baaac"
ransomNote = "aab"
def can_construct(ransomNote, magazine):
    counts_magazine ={}
    for x in magazine:
        counts_magazine[x] = counts_magazine.get(x,0) + 1
    for x in ransomNote:
        if counts_magazine.get(x,0) == 0:
            return False
        else:
            counts_magazine[x] -=1
    return True

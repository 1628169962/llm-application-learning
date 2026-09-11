nums = [1, 2, 3, 1]
# def contains_duplicate(nums):
#     dic = {}
#     for x in nums:
#         dic[x] = dic.get(x,0) + 1
#         if dic[x] == 2:
#             return True
#     return False
# print(contains_duplicate(nums))


# def contains_duplicate(nums):
#     temp = set()
#     for x in nums:
#         if x not in temp:
#             temp.add(x)
#         else:
#             return True
#     return False
# print(contains_duplicate(nums))
def contains_duplicate(nums):
    ans = set(nums)
    if len(ans) < len(nums):
        return True
    else:
        return False

print(contains_duplicate(nums))

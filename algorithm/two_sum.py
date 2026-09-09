# Day 1 - Two Sum


# =========================
# 1. 暴力解法 O(n^2)
# =========================

nums = [2, 7, 11, 15]
target = 9

length = len(nums)

for i in range(length):
    for j in range(i + 1, length):
        if nums[i] + nums[j] == target:
            print(i, j)


# =========================
# 2. dict / 哈希表解法 O(n)
# =========================

nums = [3, 2, 4]
target = 6

seen = {}

for i in range(len(nums)):
    need = target - nums[i]

    if need in seen:
        print(seen[need], i)
        break

    seen[nums[i]] = i
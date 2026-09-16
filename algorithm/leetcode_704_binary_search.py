
def search(nums,target):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        else:
            return mid
    return -1
nums = [-1, 0, 3, 5, 9, 12]

print(search(nums, 9))    # 4
print(search(nums, 12))   # 5
print(search(nums, -1))   # 0
print(search(nums, 100))  # -1

def search_insert(nums,target):
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
    return left


nums = [1, 3, 5, 6]

print(search_insert(nums, 5))  # 2
print(search_insert(nums, 2))  # 1
print(search_insert(nums, 7))  # 4
print(search_insert(nums, 0))  # 0
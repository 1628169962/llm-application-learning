*args = 多个位置参数 → tuple
**kwargs = 多个关键字参数 → dict
lambda x: x["score"] 是“取出 score”，不是“专门排序”
sorted(..., key=lambda..., reverse=True) 才是按字段降序排序
with open() 会自动关闭文件
json.load()：JSON 文件 → Python
json.dump()：Python → JSON 文件
ensure_ascii=False：中文正常保存
indent=2：JSON 格式更易读
默认参数可被关键字参数覆盖
工程里注意变量命名准确
核心代码结构：load → process/filter → save
LeetCode 242：dict.get(ch, 0) + 1 做计数，复杂度 O(n+m)
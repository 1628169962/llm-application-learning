# Day 1 - Python Basics
# 大模型应用开发实习学习记录


# =========================
# 1. Python 基础数据类型
# =========================

model_name = "DeepSeek"   # str
max_tokens = 4096         # int
score = 0.95              # float
stream = True             # bool
response = None           # None

print(model_name)
print(type(model_name))


# =========================
# 2. list
# =========================

models = ["Qwen", "DeepSeek", "GPT"]

# 读取
print(models[0])

# 修改
models[1] = "GLM"

# 添加
models.append("Claude")

# 删除
models.remove("GPT")

# 长度
print(len(models))

# 判断元素是否存在
print("Qwen" in models)

# 遍历
for model in models:
    print(model)


# =========================
# 3. tuple
# =========================

model_info = ("DeepSeek", 0.95, 2.1)

print(model_info[0])
print(model_info[1])

# tuple 创建后不能直接修改元素


# =========================
# 4. set
# =========================

models_with_duplicates = [
    "Qwen",
    "DeepSeek",
    "Qwen",
    "GPT",
    "DeepSeek"
]

unique_models = set(models_with_duplicates)

print(unique_models)


# =========================
# 5. dict
# =========================

model = {
    "name": "DeepSeek",
    "score": 0.95,
    "latency": 2.1
}

# 读取
print(model["name"])

# get 安全读取
score = model.get("score", 0.0)
print(score)

# 修改
model["score"] = 0.96

# 新增
model["status"] = "online"

# 删除
del model["status"]

# 遍历 key / value
for key, value in model.items():
    print(key, value)


# =========================
# 6. if / for / range
# =========================

models = ["Qwen", "DeepSeek", "GPT"]

if "GPT" in models:
    print("模型可用")

for model in models:
    print(model)

for i in range(len(models)):
    print(i, models[i])


# =========================
# 7. list + dict 数据处理
# =========================

results = [
    {"model": "qwen", "score": 0.91, "latency": 1.2},
    {"model": "deepseek", "score": 0.95, "latency": 2.1},
    {"model": "demo", "score": 0.72, "latency": 0.8},
]

# 读取 list 中 dict 的字段
print(results[0]["model"])
print(results[1]["score"])


# =========================
# 8. 条件过滤
# =========================

selected_results = []

for result in results:
    if result["score"] >= 0.9:
        selected_results.append(result)

print(selected_results)


# =========================
# 9. 字段提取
# =========================

model_names = []

for result in selected_results:
    model_names.append(result["model"])

print(model_names)


# =========================
# 10. 平均 score
# =========================

total_score = 0

for result in results:
    total_score += result["score"]

average_score = total_score / len(results)

print(average_score)


# =========================
# 11. 函数封装
# =========================

def filter_models(results: list) -> list:
    selected_results = []

    for result in results:
        if result["score"] >= 0.9:
            selected_results.append(result)

    return selected_results


selected = filter_models(results)

print(selected)


# =========================
# 12. 返回模型名称的函数
# =========================

def get_passed_models(records: list) -> list:
    passed_models = []

    for record in records:
        if record["score"] >= 0.9:
            passed_models.append(record["model"])

    return passed_models


passed = get_passed_models(results)

print(passed)
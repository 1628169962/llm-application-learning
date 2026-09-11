# def add_log(func):
#     # 在这里定义 wrapper
#     def wrapper():
#         print("开始执行")
#         func()
#         print("执行结束")
#     return wrapper
# @add_log
# def ask_llm():
#     print("正在调用 Qwen")
# ask_llm()
# new_func = add_log(ask_llm)
# new_func()
#
#
# def search_documents():
#     print("正在检索文档")
# def run(func):
#     print("开始执行")
#     func()
#     print("执行结束")
#
# run(ask_llm)
# run(search_documents)
#
# def create_func():
#     def hello():
#         print("hello")
#     return hello
# func = create_func()
# func()
#
# import time
#
# def timer(func):
#     def wrapper(*args,**kwargs):
#         start = time.perf_counter()
#         result = func(*args,**kwargs)
#         end = time.perf_counter()
#         ans = end - start
#         print(f"耗时：{ans}秒")
#         return result
#     return wrapper
#
#
# @timer
# def ask_llm():
#     time.sleep(1)
#     print("正在调用 Qwen")
#
#
# ask_llm()
#
# def generate_models():
#     yield "qwen"
#     yield "deepseek"
#     yield "demo"
#
# for model in generate_models():
#     print(model)
#
#
#
# import csv
#
# with open("models.csv", "r", encoding="utf-8") as f:
#     reader = csv.reader(f)
#
#     for row in reader:
#         print(row)
#
# import csv
# with open("models.csv", "r", encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#
#     for row in reader:
#         row["score"] = float(row["score"])
#         row["latency"] = float(row["latency"])
#         print(row)
#         print(type(row["score"]))
#
# text = "   DeepSeek 是一个大模型。   \n"
# clean_text = text.strip()
#
# print(repr(clean_text))
#
# text = "qwen|deepseek|demo"
# parts = text.split("|")
# print(parts)
#
# text = "LLM---RAG---Agent"
# text = text.replace("---","|")
# print(text)
# text = "QWEN and DeepSeek are LLM Models"
# clean_text = text.lower()
# print(clean_text)
# text = "   ### RAG Is Useful   \n"
# clean_text = text.strip().replace("### ","").lower()
# print(clean_text)
#
# nums = [1, 2, 3, 4, 5, 6]
# def even_numbers(nums):
#     for x in nums:
#         if x %2 == 0:
#             yield x
# for x in even_numbers(nums):
#     print(x)

# import csv
# with open("servers.csv","r",encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         row["load"] = float(row["load"])
#         print(row)
#         print(type(row["load"]))

from model_processor import timer
models = [
    {"name": "qwen", "score": 0.91},
    {"name": "deepseek", "score": 0.95},
    {"name": "demo", "score": 0.72}
]

def get_good_models(models):
    for model in models:
        if model["score"] >= 0.9:
            yield model
@timer
def work(models):
    for model in get_good_models(models):
        print(model)
work(models)
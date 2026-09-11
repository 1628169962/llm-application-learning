# Day 4 学习笔记：Decorator / Generator / CSV / 文本处理 / venv / pip

## 一、Decorator 装饰器

### 1. 为什么需要装饰器

很多函数可能都需要重复增加一些功能，例如：

```python
开始执行
真正业务代码
执行结束
```

或者：

```python
记录开始时间
执行函数
记录结束时间
打印耗时
```

如果每个函数都重复写，会产生大量重复代码。

装饰器的作用：

> 在不直接修改原函数内部代码的情况下，为函数增加日志、计时等额外功能。

典型场景：

- LLM 请求日志
- API 调用日志
- 函数耗时统计
- 权限检查
- 重试
- 缓存

---

### 2. 函数也是对象

函数不仅可以调用：

```python
hello()
```

函数本身也可以被保存、传递：

```python
hello
```

区别：

```python
hello      # 函数本身
hello()    # 执行函数
```

函数可以作为参数：

```python
def run(func):
    func()
```

调用：

```python
run(hello)
```

---

### 3. 函数也可以作为返回值

```python
def create_func():
    def hello():
        print("hello")

    return hello
```

注意：

```python
return hello
```

返回的是函数本身。

而：

```python
return hello()
```

返回的是函数执行后的结果。

---

### 4. wrapper 是什么

`wrapper` 可以理解成：

> 包裹原函数的新函数。

例如：

```python
def add_log(func):
    def wrapper():
        print("开始执行")
        func()
        print("执行结束")

    return wrapper
```

结构：

```text
原函数
↓
传给 decorator
↓
创建 wrapper
↓
wrapper 内执行原函数 + 新功能
↓
返回 wrapper
```

---

### 5. `@decorator` 的本质

```python
@add_log
def ask_llm():
    print("正在调用 Qwen")
```

本质相当于：

```python
ask_llm = add_log(ask_llm)
```

所以以后调用：

```python
ask_llm()
```

实际上先执行的是 `wrapper()`。

---

### 6. `@timer` 装饰器

今天自己完成的基础结构：

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        cost = end - start
        print(f"耗时：{cost}秒")

        return result

    return wrapper
```

使用：

```python
@timer
def ask_llm():
    ...
```

重要细节：

```python
wrapper(*args, **kwargs)
```

是为了让装饰器能够包装带任意参数的函数。

```python
result = func(*args, **kwargs)
return result
```

是为了保留原函数的返回值。

---

## 二、Generator 生成器

### 1. generator 的核心思想

普通 list：

```text
先准备全部结果
↓
全部放入 list
↓
再使用
```

generator：

```text
产生一个
↓
使用一个
↓
再产生一个
↓
再使用一个
```

核心思想：

> 逐步产生结果，而不是一次性准备全部结果。

---

### 2. `yield`

最简单的 generator：

```python
def generate_models():
    yield "qwen"
    yield "deepseek"
    yield "demo"
```

使用：

```python
for model in generate_models():
    print(model)
```

---

### 3. `return` 和 `yield`

`return`：

```text
返回结果
↓
函数结束
```

`yield`：

```text
产生一个结果
↓
函数暂停
↓
下次继续从暂停位置执行
```

例如：

```python
def numbers():
    for x in range(1, 4):
        yield x
```

---

### 4. generator 不是 list

```python
result = numbers()
print(result)
```

不会得到：

```python
[1, 2, 3]
```

而是类似：

```text
<generator object numbers at ...>
```

它只是保存了：

> 怎样继续产生下一个数据。

可以使用：

```python
for x in result:
    print(x)
```

也可以简单知道：

```python
next(result)
```

表示获取下一个值。

---

### 5. 筛选型 generator

```python
def filter_models(models):
    for model in models:
        if model["score"] >= 0.9:
            yield model
```

使用：

```python
for model in filter_models(models):
    print(model)
```

---

### 6. generator 和 LLM Streaming

普通 LLM 返回：

```text
整个回答生成完成
↓
一次性返回
```

Streaming：

```text
产生一小段
↓
返回一小段
↓
继续产生
↓
继续返回
```

和 generator 的共同思想：

> 逐步产生、逐步消费。

---

### 7. 今天遇到的重要坑

普通 `@timer` 直接装饰 generator：

```python
@timer
def get_good_models(models):
    yield ...
```

此时：

```python
func(*args, **kwargs)
```

只是创建了 generator 对象，并没有真正执行完整 generator。

所以可能先输出：

```text
耗时：0.000001秒
```

然后才开始打印 generator 中的数据。

说明统计到的只是：

> generator 对象创建时间。

更适合当前阶段的方式：

```python
def get_good_models(models):
    for model in models:
        if model["score"] >= 0.9:
            yield model


@timer
def work(models):
    for model in get_good_models(models):
        print(model)
```

这样 `@timer` 才覆盖完整遍历过程。

---

# 三、CSV

## 1. CSV 是什么

CSV：

> Comma-Separated Values

即：

> 逗号分隔值。

例如：

```csv
model,score,latency
qwen,0.91,1.2
deepseek,0.95,2.1
demo,0.72,0.8
```

本质上仍然是文本文件。

---

## 2. `csv.reader`

```python
import csv

with open("models.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)

    for row in reader:
        print(row)
```

结果：

```python
['model', 'score', 'latency']
['qwen', '0.91', '1.2']
```

每一行是一个 `list`。

---

## 3. `csv.DictReader`

今天重点：

```python
with open("models.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(row)
```

结果类似：

```python
{
    "model": "qwen",
    "score": "0.91",
    "latency": "1.2"
}
```

优点：

```python
row["model"]
row["score"]
row["latency"]
```

比：

```python
row[0]
row[1]
row[2]
```

更清楚。

---

## 4. CSV 读取出来默认是字符串

即使 CSV 里写：

```text
0.91
```

读取出来仍然是：

```python
"0.91"
```

类型：

```python
str
```

需要手动：

```python
row["score"] = float(row["score"])
row["latency"] = float(row["latency"])
```

转换后：

```python
{
    "model": "qwen",
    "score": 0.91,
    "latency": 1.2
}
```

---

# 四、文本处理

今天只学习了 RAG 中最常用的几个基础方法。

## 1. `strip()`

去掉字符串两端空白：

```python
text = "   RAG   \n"
clean_text = text.strip()
```

结果：

```text
RAG
```

---

## 2. `repr()`

用于观察字符串真实内容：

```python
text = "hello\n"

print(text)
print(repr(text))
```

`repr()` 可以看到：

```python
'hello\n'
```

适合检查：

- `\n`
- `\t`
- 多余空格

---

## 3. `split()`

按指定字符切割：

```python
text = "qwen|deepseek|demo"

parts = text.split("|")
```

结果：

```python
["qwen", "deepseek", "demo"]
```

---

## 4. `replace()`

替换字符串内容：

```python
text = "LLM---RAG---Agent"

text = text.replace("---", "|")
```

结果：

```text
LLM|RAG|Agent
```

---

## 5. `lower()`

英文统一转小写：

```python
text = "QWEN DeepSeek RAG"

text = text.lower()
```

结果：

```text
qwen deepseek rag
```

---

## 6. 链式调用

今天已经会：

```python
text = "   ### RAG Is Useful   \n"

clean_text = text.strip().replace("### ", "").lower()
```

处理过程：

```text
原文本
↓ strip()
去两端空白
↓ replace()
去掉 ###
↓ lower()
统一成小写
```

---

# 五、虚拟环境 `.venv`

## 1. 为什么需要虚拟环境

核心：

> 隔离不同项目的 Python 依赖，防止版本冲突。

例如：

```text
项目 A
└── 自己的 .venv

项目 B
└── 自己的 .venv
```

不同项目可以安装不同版本的库。

---

## 2. 创建虚拟环境

在项目根目录：

```cmd
python -m venv .venv
```

---

## 3. CMD 激活

Windows CMD：

```cmd
.venv\Scripts\activate
```

成功后：

```text
(.venv) D:\llm-application-learning>
```

---

# 六、pip

`pip`：

> Python 的包管理工具。

主要用来：

- 安装包
- 查看包
- 管理依赖
- 导出依赖

今天实际执行：

```cmd
pip list
```

查看当前环境已有的包。

```cmd
pip install requests
```

安装：

```text
requests
```

以及它需要的依赖。

```cmd
pip show requests
```

查看：

- Name
- Version
- Location
- Requires

其中今天确认：

```text
Location:
D:\llm-application-learning\.venv\Lib\site-packages
```

说明包确实安装在项目自己的 `.venv` 中。

---

## requirements.txt

执行：

```cmd
pip freeze > requirements.txt
```

可以把当前依赖和版本保存下来：

```text
certifi==...
charset-normalizer==...
idna==...
requests==...
urllib3==...
```

核心命令总结：

```text
pip install xxx
→ 安装包

pip show xxx
→ 查看某个包

pip list
→ 查看环境中的包

pip freeze
→ 输出依赖和版本

pip freeze > requirements.txt
→ 保存项目依赖
```

---

# 七、综合任务

目录：

```text
python/day04/
├── models.csv
├── model_processor.py
└── requirements.txt
```

今天拆出了几个职责不同的函数。

### `load_models`

职责：

> 读取 CSV。

```python
def load_models(file_path):
    models = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ...
```

### `clean_model`

职责：

> 一次清洗一条模型数据。

```python
def clean_model(model):
    model["model"] = model["model"].strip()
    model["score"] = float(model["score"])
    model["latency"] = float(model["latency"])

    return model
```

### `filter_models`

职责：

> 使用 generator 筛选高分模型。

```python
def filter_models(models):
    for model in models:
        if model["score"] >= 0.9:
            yield model
```

### `process_models`

职责：

> 组织整个处理流程。

```text
CSV
↓
读取
↓
清洗
↓
类型转换
↓
generator 筛选
↓
打印
```

并使用：

```python
@timer
```

统计完整处理过程。

---

# 八、LeetCode 383 — Ransom Note

核心问题：

> `magazine` 中的字符数量，够不够组成 `ransomNote`。

使用：

```python
dict
```

保存：

```text
key
→ 字符

value
→ 字符出现次数
```

统计：

```python
counts[x] = counts.get(x, 0) + 1
```

消费字符：

```python
if counts.get(x, 0) == 0:
    return False

counts[x] -= 1
```

最终：

```python
return True
```

复杂度：

```text
m = magazine 长度
n = ransomNote 长度

时间复杂度：
O(m + n)

一般字符串分析下空间复杂度：
O(m)
```

如果严格按照 LeetCode 原题只有 26 个小写字母，也可以认为额外空间为：

```text
O(1)
```

---

# Day 4 易忘点

今天明天最值得快速复习的是：

```text
1. @timer
≈ 原函数 = timer(原函数)

2. wrapper 要透传：
*args, **kwargs

3. wrapper 不要忘记：
return 原函数返回值

4. yield：
产生一个值后暂停，不是函数结束

5. DictReader 读取出的数字默认仍是 str

6. str → float：
float(row["score"])

7. 函数传了 file_path，
内部不要重新写死 "models.csv"

8. 普通 @timer 直接包装 generator，
通常只能测 generator 对象创建时间

9. pip freeze > requirements.txt
用于记录项目依赖
```

**Day 4 评级：A。核心内容已经达到今天的学习标准。**
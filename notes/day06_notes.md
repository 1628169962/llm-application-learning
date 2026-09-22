
可以。下面这份你可以直接保存成 `notes/day06_notes.md`，我把“今天学习内容”和“今天你问过/卡住过的问题”分开整理了。

# Day 6：Python 第一阶段收尾

## 一、Python 第一阶段知识地图

Python 第一阶段可以串成这样：

```text
Python 数据
→ 控制逻辑
→ 函数
→ 文件 / JSON
→ 模块
→ class
→ 异常处理
→ HTTP API
```

各部分解决的问题：

- `list / dict / tuple / set`：保存和组织数据
- `if / for / while`：决定程序怎么执行
- `def`：封装重复逻辑
- 文件 / JSON：保存和读取数据
- 模块：把代码拆到不同 `.py` 文件
- class：组织一类对象的数据和行为
- `try / except`：处理程序可能出现的异常
- HTTP API：让 Python 程序和外部服务通信

完整的数据处理链：

```text
服务器
↓
HTTP Response
↓
JSON
↓
Python list / dict
↓
if / for / sorted / lambda
↓
筛选 / 排序
↓
函数 / class 封装
↓
不同 .py 文件
↓
import
↓
main.py
```

---

# 二、同步执行

## 1. 什么是同步？

同步执行就是：

> 前一个任务没有完成，后一个任务不会开始。

例如：

```text
request-1
↓
等待
↓
完成
↓
request-2
↓
等待
↓
完成
↓
request-3
```

今天写了同步实验：

```python
import time

def request(name):
    print(name + "开始")
    time.sleep(2)
    print(name + "结束")

start = time.perf_counter()

request("request-1")
request("request-2")
request("request-3")

end = time.perf_counter()

print(end - start)
```

实际结果约为：

```text
6 秒
```

原因：

```text
request-1 等 2 秒
+
request-2 等 2 秒
+
request-3 等 2 秒
≈ 6 秒
```

---

## 2. `time.sleep(2)` 今天代表什么？

今天的 `sleep(2)` 不是单纯为了让程序变慢。

它是在模拟：

```text
等待网络
等待数据库
等待文件 IO
```

这些都属于 I/O 等待。

---

# 三、为什么需要异步

同步程序的问题：

```text
request-1 正在等待网络
↓
程序也一直等待
↓
request-2 无法开始
```

但是等待网络的时候，CPU 不一定有事情做。

于是可以产生这样的思想：

```text
request-1 等待 I/O
→ 程序先处理 request-2
→ request-2 也等待
→ 程序继续处理其他任务
→ request-1 返回后再继续处理
```

这就是异步最重要的直觉：

> 一个任务等待 I/O 时，可以把执行机会让给其他任务。

今天只建立异步直觉，没有正式学习：

```python
async
await
asyncio.gather()
```

这些放到下一阶段继续学习。

---

# 四、API 数据处理项目

今天完成了一个小型 API 数据处理程序：

```text
python/day06/

├── api_client.py
├── processor.py
├── main.py
└── requirements.txt
```

整个程序流程：

```text
HTTP API
↓
requests
↓
JSON
↓
Python list / dict
↓
清洗
↓
类型转换
↓
筛选
↓
排序
↓
输出结果
```

---

# 五、模块职责

## `api_client.py`

负责：

```text
HTTP 请求
GET / POST
timeout
检查 HTTP 状态
处理网络异常
返回 JSON 数据
```

核心思想：

> `api_client.py` 只负责“拿数据”。

---

## `processor.py`

负责：

```text
清洗数据
类型转换
条件筛选
排序
返回处理后的数据
```

核心思想：

> `processor.py` 只负责“处理数据”。

---

## `main.py`

负责：

```text
创建 APIClient
↓
请求数据
↓
调用 processor
↓
输出最终结果
```

核心思想：

> `main.py` 负责组织整个程序流程，而不是自己写大量业务逻辑。

---

# 六、默认参数

正确：

```python
def process_products(
    products,
    min_rating=4.5,
    min_stock=10
):
    ...
```

这样：

```python
process_products(products)
```

会使用默认值。

也可以：

```python
process_products(
    products,
    min_rating=4.8,
    min_stock=20
)
```

覆盖默认值。

容易犯的错误：

```python
min_rating = 4.5

def process_products(products):
```

这种写法是全局变量，不是函数默认参数。

---

# 七、`dict.get()` 的重要用法

今天重点遇到了：

```python
products.get("products", [])
```

意思：

```text
如果存在 "products"
→ 返回对应的数据

如果不存在
→ 返回 []
```

为什么这里使用：

```python
[]
```

而不是：

```python
0
None
```

因为后面马上要：

```python
for product in ...
```

空列表可以安全遍历：

```python
for product in []:
    ...
```

不会报错。

而：

```python
for product in 0:
```

会报错，因为整数不能遍历。

因此一个重要原则：

> `dict.get()` 的默认值，要根据后面的代码需要选择合适的数据类型。

---

# 八、数据清洗与类型转换

今天的数据处理包括：

```python
title = product["title"].strip()
rating = float(product["rating"])
price = float(product["price"])
stock = int(product["stock"])
```

作用：

```text
strip()
→ 删除字符串首尾空格

float()
→ 转换成浮点数

int()
→ 转换成整数
```

这样后面的比较和排序才可靠。

---

# 九、条件筛选

例如：

```python
if rating >= min_rating and stock >= min_stock:
```

表示必须同时满足：

```text
rating 达标
并且
stock 达标
```

才保留数据。

---

# 十、lambda 排序

今天继续使用：

```python
sorted(
    products,
    key=lambda x: x["rating"],
    reverse=True
)
```

含义：

```text
lambda x: x["rating"]
```

表示：

> 给我一个商品 `x`，我返回它的 `rating`。

`sorted()` 再根据这个值进行排序。

```python
reverse=True
```

表示：

```text
从高到低排序
```

需要继续记住：

> `lambda` 本身不是“排序语法”，它只是一个很小的函数。

---

# 十一、异常处理

API 请求：

```python
try:
    response = requests.get(...)
    response.raise_for_status()
except requests.RequestException:
    ...
```

主要为了处理：

```text
网络断开
请求超时
HTTP 请求失败
服务器异常
```

重点：

> `try / except` 不是为了隐藏报错，而是为了处理程序中预期可能发生的问题。

---

# 十二、`requirements.txt`

今天再次确认：

```text
time
→ Python 标准库
→ 不需要安装
→ 不写 requirements.txt

requests
→ 第三方库
→ 需要 pip 安装
→ 应该写入 requirements.txt
```

`requirements.txt` 的作用：

> 记录项目需要安装的第三方 Python 库。

别人拿到项目以后可以：

```bash
pip install -r requirements.txt
```

安装依赖。

---

# 十三、LeetCode 344：Reverse String

题目：

```python
["h", "e", "l", "l", "o"]
```

原地修改成：

```python
["o", "l", "l", "e", "h"]
```

使用双指针：

```python
def reverse_string(s):
    left = 0
    right = len(s) - 1

    while left < right:
        temp = s[left]
        s[left] = s[right]
        s[right] = temp

        left += 1
        right -= 1
```

---

## `left += 1`

表示：

```text
左指针向右移动一格
```

## `right -= 1`

表示：

```text
右指针向左移动一格
```

最终两个指针不断向中间靠近。

---

# 十四、为什么叫原地修改？

因为没有重新创建一个长度为 `n` 的新列表。

而是直接：

```python
s[left] = ...
s[right] = ...
```

修改原来的列表。

所以额外空间没有随着输入规模增加。

---

# 十五、复杂度

Reverse String：

```text
时间复杂度：O(n)

空间复杂度：O(1)
```

时间 O(n)：

因为所有元素最多处理一次左右。

空间 O(1)：

因为只额外使用了：

```text
left
right
temp
```

无论数组有多长，额外变量数量基本不变。

---

# 十六、今天最重要的知识链

今天应该真正记住：

```text
HTTP API
↓
requests
↓
JSON
↓
list / dict
↓
for
↓
if
↓
类型转换 / 清洗
↓
lambda 排序
↓
函数
↓
class
↓
模块拆分
↓
main.py
```

这说明 Python 第一阶段学习的知识已经开始连成完整程序，而不是孤立的语法。

---

# 十七、今天我卡住 / 重点问过的问题

## 1. `processor.py` 到底负责什么？

最终理解：

```text
api_client.py
→ 获取数据

processor.py
→ 清洗、类型转换、筛选、排序

main.py
→ 组织程序流程
```

重点：

> 模块拆分的核心是职责分离。

---

## 2. 默认参数应该写在哪里？

一开始容易写成：

```python
min_rating = 4.5
min_stock = 10
```

后来明确：

```python
def process_products(
    products,
    min_rating=4.5,
    min_stock=10
):
```

才是真正默认参数。

---

## 3. `dict.get()` 第二个参数为什么用 `[]`？

重点理解：

```python
products.get("products", [])
```

因为后面需要：

```python
for product in ...
```

空列表可以安全遍历。

默认值不能随便写，要考虑后续代码需要的数据类型。

---

## 4. 为什么同步 3 个任务需要约 6 秒？

因为三个：

```python
time.sleep(2)
```

是顺序执行：

```text
2 + 2 + 2 ≈ 6 秒
```

同步程序中，前一个任务没完成，后一个不会开始。

---

## 5. 异步解决什么问题？

重点不是“让所有东西同时运行”。

而是：

> 一个任务等待网络、数据库、文件等 I/O 时，可以先处理其他任务。

---

## 6. 为什么 `requests` 写 requirements，但 `time` 不写？

因为：

```text
time
→ Python 自带标准库

requests
→ 第三方包
```

---

# 十八、今天最容易忘记的内容

建议后续重点复习：

```text
1. 默认参数写在函数参数列表中

2. dict.get() 默认值要考虑后续数据类型

3. api_client / processor / main 职责不要混

4. lambda 只是一个小函数，不是排序专用语法

5. requests 请求成功后应该 return 数据，
   而不是只 print 数据

6. 同步任务等待时，后面的任务不能执行

7. 异步最核心的价值之一是利用 I/O 等待时间
```

---

# 十九、Day 6 阶段结论

Day 6 评级：

```text
B
```

Python 第一阶段评级：

```text
B
```

目前已经可以进入：

```text
asyncio
↓
FastAPI
↓
LLM API
↓
RAG
↓
Agent
```

后续不需要停下来继续大量刷 Python 基础，而应该：

> 在工程学习过程中继续穿插复习 Python。

你今天最值得反复看的其实是三块：**同步与异步的区别、模块职责拆分、`dict.get()` 默认值为什么要根据后续操作选择**。这三点都属于从“会语法”向“会写程序”过渡的关键。

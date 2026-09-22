
可以，下面我按“今天学了什么 + 你今天最容易卡住的问题 + 复习清单”给你整理成一份适合直接放进 `notes/day05_notes.md` 的版本。

# Day 5：HTTP / REST / requests / API 调用

## 一、今天的核心主线

今天最重要的是建立这条链：

```text
Python 程序
→ HTTP Request
→ API Server
→ HTTP Response
→ Python 程序
```

以后调用 Qwen、DeepSeek、OpenAI-compatible API，本质上仍然是这条链。

常见形式：

```text
Python
→ POST
→ Headers
→ JSON Body
→ LLM Server
→ JSON Response
→ Python
```

---

# 二、HTTP 基础概念

## 1. Client

Client 是主动发起请求的一方。

例如：

```text
Python 程序
→ 请求 API
```

这里 Python 程序就是 Client。

---

## 2. Server

Server 是接收请求并返回结果的一方。

例如：

```text
Python 程序
→ API Server
→ 返回数据
```

---

## 3. HTTP

HTTP 是客户端和服务器之间进行通信的一套规则。

核心作用：

```text
规范 Request 怎么发送
规范 Response 怎么返回
```

不需要深入 TCP/IP、OSI。

---

## 4. URL

URL 是访问某个资源或 API 的地址。

例如：

```text
https://api.example.com/models
```

可以理解成：

```text
我要去哪里请求
```

---

## 5. API

API 是服务器开放给程序调用的功能入口。

例如：

```text
GET /models
POST /chat
```

分别可能代表：

```text
查询模型
提交聊天请求
```

---

## 6. Request

Request 是 Client 发给 Server 的请求信息。

常见包含：

```text
Method
URL
Headers
Body
```

---

## 7. Response

Response 是 Server 处理完请求后返回给 Client 的结果。

常见包含：

```text
status code
headers
body
```

---

# 三、GET 和 POST

## GET

GET 通常用于查询已有信息。

例如：

```text
GET /models
```

表示查询支持哪些模型。

```text
GET /tasks/123
```

表示查询任务状态。

核心理解：

```text
GET
→ 查询、获取已有信息
```

---

## POST

POST 通常用于提交数据，让服务器处理。

例如：

```text
POST /chat
```

Body：

```json
{
  "model": "qwen",
  "prompt": "什么是 RAG？"
}
```

服务器收到后：

```text
接收 prompt
→ 调用模型
→ 生成答案
→ 返回结果
```

核心理解：

```text
POST
→ 提交数据
→ 让服务器执行处理
```

---

# 四、HTTP Request 结构

一个典型请求：

```text
POST /chat

Headers:
Content-Type: application/json

Body:
{
  "model": "qwen",
  "prompt": "什么是 RAG？"
}
```

## 1. URL

决定请求哪个 API。

---

## 2. Query Parameters

Query Parameters 是 URL 上附带的查询条件。

例如：

```text
GET /comments?postId=1
```

这里：

```text
postId=1
```

就是 Query Parameter。

requests 中使用：

```python
params = {
    "postId": 1
}

response = requests.get(url, params=params)
```

requests 会自动拼成：

```text
...?postId=1
```

---

## 3. Headers

Headers 是请求的附加说明信息。

不要只理解成 Body 格式。

常见作用包括：

```text
说明数据格式
身份认证
其他请求元数据
```

例如：

```text
Content-Type: application/json
```

表示请求 Body 是 JSON。

```text
Authorization: Bearer xxx
```

表示携带认证信息。

---

## 4. Body

Body 是真正提交给服务器处理的主要数据。

大模型 API 里可能包含：

```text
model
prompt
messages
temperature
max_tokens
```

---

## 5. JSON Body

如果 Body 使用 JSON 格式，就是 JSON Body。

例如：

```json
{
  "model": "qwen",
  "prompt": "你好"
}
```

---

# 五、HTTP Response

## 1. status code

状态码表示服务器处理请求的结果。

最重要的是先理解大类：

```text
2xx → 成功
4xx → 客户端请求存在问题
5xx → 服务器存在问题
```

常见状态码：

```text
200 → 请求成功
201 → 成功创建资源
400 → 请求参数或格式有问题
401 → 身份认证失败
403 → 已认证，但没有权限
404 → 找不到接口或资源
429 → 请求过于频繁，被限流
500 → 服务器内部错误
```

---

## 2. Response Headers

服务器返回的附加说明。

例如：

```text
Content-Type: application/json
```

表示返回的 Body 是 JSON。

---

## 3. Response Body

服务器真正返回的数据。

例如：

```json
{
  "answer": "RAG 是检索增强生成"
}
```

---

# 六、requests 基础

导入：

```python
import requests
```

---

## 1. GET

基本形式：

```python
response = requests.get(url)
```

常用属性：

```python
response.status_code
response.text
response.json()
response.headers
response.url
```

---

## 2. response.text

```python
response.text
```

把 Response Body 当普通字符串读取。

类型通常是：

```python
str
```

---

## 3. response.json()

```python
data = response.json()
```

把 JSON Response Body 解析成 Python 数据。

例如 JSON 对象通常会变成：

```python
dict
```

JSON 数组通常会变成：

```python
list
```

---

## 4. response.headers

查看 Response Headers。

例如：

```python
print(response.headers["Content-Type"])
```

---

# 七、requests 重要参数

## params=

作用：

```text
添加 Query Parameters
```

例如：

```python
params = {
    "postId": 1
}

requests.get(url, params=params)
```

---

## headers=

作用：

```text
添加 Request Headers
```

例如：

```python
headers = {
    "X-Client-Name": "llm-intern"
}
```

---

## json=

作用：

```text
把 Python 数据作为 JSON Body 发送
```

例如：

```python
data = {
    "title": "learn http"
}

requests.post(url, json=data)
```

这里 `data` 是 Python `dict`。

requests 会帮助把它按 JSON 请求体发送。

---

## timeout=

作用：

```text
限制网络请求等待时间
避免程序无限等待
```

例如：

```python
requests.get(url, timeout=5)
```

工程里建议养成加 timeout 的习惯。

---

# 八、POST 请求

基本形式：

```python
response = requests.post(
    url,
    json=data,
    headers=headers,
    timeout=5
)
```

典型流程：

```text
Python dict
→ json=data
→ JSON Body
→ Server
→ JSON Response
→ response.json()
→ Python dict
```

---

# 九、网络请求异常处理

网络请求一定可能失败。

常见问题：

```text
请求超时
服务器连接失败
HTTP 返回 4xx / 5xx
JSON 解析失败
```

---

## 1. Timeout

```python
except requests.Timeout:
    print("请求超时")
```

含义：

```text
请求等太久
```

---

## 2. ConnectionError

```python
except requests.ConnectionError:
    print("连接失败")
```

含义：

```text
服务器根本连不上
```

---

## 3. raise_for_status()

```python
response.raise_for_status()
```

作用：

```text
2xx
→ 一般继续执行

4xx / 5xx
→ 抛出 HTTPError
```

---

## 4. HTTPError

```python
except requests.HTTPError:
    print("HTTP 请求错误")
```

适合处理：

```text
400
401
403
404
429
500
...
```

---

## 5. RequestException

```python
except requests.RequestException:
    print("请求失败")
```

可以作为 requests 网络请求异常的统一兜底。

通常：

```text
先捕获具体异常
最后 RequestException 兜底
```

---

## 6. JSON 解析失败

即使状态码是 200，也不代表一定能：

```python
response.json()
```

如果服务器返回：

```text
hello world
```

这种普通文本，JSON 解析就可能失败。

可以：

```python
try:
    data = response.json()
except ValueError:
    print("JSON 解析失败")
```

---

# 十、APIClient 综合实战

目录：

```text
python/day05/

├── api_client.py
├── main.py
└── requirements.txt
```

---

## api_client.py 设计

核心结构：

```text
APIClient
├── __init__
├── get
└── post
```

### __init__

作用：

```text
保存 base_url
```

例如：

```text
https://jsonplaceholder.typicode.com
```

以后请求时只需要传：

```text
/posts
/comments
/users
```

---

## get()

需要支持：

```text
path
headers
timeout
HTTP 错误处理
请求异常处理
```

核心流程：

```text
base_url + path
→ requests.get()
→ raise_for_status()
→ return response
```

---

## post()

需要支持：

```text
path
json
headers
timeout
HTTP 错误处理
请求异常处理
```

核心流程：

```text
base_url + path
→ requests.post()
→ raise_for_status()
→ return response
```

---

## main.py

作用：

```text
导入 APIClient
→ 创建 client
→ 调用 get/post
→ 判断 response 是否为 None
→ 读取 JSON
```

如果请求失败，APIClient 当前版本可能返回：

```python
None
```

所以调用后可以判断：

```python
if response is not None:
    print(response.json())
```

---

## requirements.txt

今天最核心的依赖：

```text
requests
```

---

# 十一、HTTP 和 LLM API 的关系

这是今天必须记住的重点。

以后调用：

```text
Qwen
DeepSeek
OpenAI-compatible API
```

本质仍然是：

```text
Python
→ HTTP Request
→ LLM Server
→ HTTP Response
→ Python
```

常见请求：

```text
POST
Headers
JSON Body
```

Body 里的业务数据可能换成：

```text
model
messages
prompt
temperature
max_tokens
```

但 HTTP 主线没有变。

---

# 十二、LeetCode 125：Valid Palindrome

## 题目要求

忽略：

```text
大小写
非字母数字字符
```

判断字符串是否为回文。

---

## 方法一：清洗 + 反转

流程：

```text
过滤非字母数字
→ lower()
→ clean[::-1]
→ 比较
```

例如：

```python
reversed_clean = clean[::-1]
```

### 切片

格式：

```python
text[start:end:step]
```

常见：

```python
text[1:4]
text[::2]
text[::-1]
```

其中：

```python
[::-1]
```

表示：

```text
从后往前
每次移动 1 个字符
```

用于反转字符串。

### 复杂度

```text
时间：O(n)
空间：O(n)
```

因为创建了：

```text
clean
reversed_clean
```

---

## 方法二：双指针

核心：

```text
left 从左向右
right 从右向左
```

初始化：

```python
left = 0
right = len(s) - 1
```

如果左边不是字母数字：

```python
left += 1
```

如果右边不是字母数字：

```python
right -= 1
```

如果左右都是有效字符：

```python
s[left].lower()
s[right].lower()
```

进行比较。

不同：

```python
return False
```

相同：

```python
left += 1
right -= 1
```

循环结束：

```python
return True
```

### 复杂度

```text
时间：O(n)
空间：O(1)
```

这是今天最终完成的优化版本。

---

# 十三、今天容易混淆 / 需要复习的点

## 1. Headers 不是只用来规定 Body 格式

更准确：

```text
Headers
= 请求或响应的附加说明信息
```

`Content-Type` 和 `Authorization` 只是常见例子。

---

## 2. response.text 和 response.json()

```text
response.text
→ str

response.json()
→ 把 JSON 解析成 Python 对象
```

---

## 3. params 和 json 不一样

```text
params=
→ URL 后面的查询参数

json=
→ Request Body
```

---

## 4. HTTP 成功收到响应，不代表业务请求成功

例如：

```text
404
500
```

服务器都已经成功返回 Response。

所以需要：

```python
response.raise_for_status()
```

检查 HTTP 状态。

---

## 5. timeout 很重要

真实项目不要默认无限等待。

要逐渐养成：

```python
timeout=5
```

这样的习惯。

---

## 6. lower 和 lower()

```python
.lower
```

是方法本身。

```python
.lower()
```

才是真正执行方法。

---

## 7. 双指针比较的是字符，不是下标

错误思路：

```python
if left != right:
```

正确思路：

```python
if s[left].lower() != s[right].lower():
```

---

# 十四、Day 5 验收结果

## Day 5 评级：B，接近 A

### 已掌握

- HTTP Client / Server
- Request / Response
- GET / POST
- URL / params / headers / body
- JSON 请求与响应
- HTTP status code
- 2xx / 4xx / 5xx
- requests GET / POST
- timeout
- raise_for_status()
- requests 基础异常处理
- APIClient 封装
- HTTP 与 LLM API 的关系
- LeetCode 125 双指针

### 不熟练

- Headers 的完整定义
- LLM API 与 HTTP 的关系还需要形成条件反射
- 独立写请求时容易漏 timeout
- Python 方法调用的 `()` 偶尔容易忘

### 是否达标

达标。

### 是否可以进入下一阶段

可以进入下一阶段 Python 工程能力学习。

你今天问的问题里，最值得单独记住的是这几个，因为它们暴露的是“真正需要复习的理解点”，不是简单语法：

1. **“我不会反转字符串”**重点学会了切片结构 `text[start:end:step]`，尤其是 `text[::-1]` 表示从后往前每次走一步。
2. **为什么双指针不能写 `if left != right`**因为 `left`、`right` 是下标，真正要比较的是 `s[left]` 和 `s[right]`。
3. **`.lower` 和 `.lower()` 的区别**`.lower` 是方法对象，`.lower()` 才是执行方法并得到小写结果。
4. **为什么 APIClient 里不能把 URL 写死**`__init__(base_url)` 的意义就是把外部传进来的 `base_url` 保存到 `self.base_url`，这样类才能复用。
5. **为什么 URL 不用 `Path`**`Path` 是本地文件路径工具；HTTP URL 本质上是字符串，不能把文件路径拼接思路直接搬过来。
6. **为什么请求失败后要判断 `response is not None`**因为当前 `APIClient` 捕获异常后没有显式返回值，会默认返回 `None`，此时直接 `response.json()` 会再次报错。
7. **为什么 `raise_for_status()` 很重要**“成功收到服务器 Response”和“HTTP 请求成功”不是一回事。服务器返回 `404`、`500` 时同样有 Response，`raise_for_status()` 用来把 4xx / 5xx 转成异常处理。
8. **大模型 API 到底和今天学的 HTTP 有什么关系**
   以后调用 Qwen、DeepSeek、OpenAI-compatible API，本质仍然是：
   `Python → HTTP Request → LLM Server → HTTP Response → Python`。

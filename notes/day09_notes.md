
当然可以。下面我按你之后方便直接放进 `notes/day09_notes.md` 的形式整理。今天内容很多，但主线其实非常清楚：**从“我去请求别人的 API”正式走到了“别人通过 HTTP 请求我的 Python 程序”。**

# Day 9 笔记总结：FastAPI + Pydantic + HTTP API Server

## 1. 今日核心目标

今天最终完成了一个：

```text
LLM API Server V0.1
```

包含：

```text
GET  /health
POST /chat
POST /embedding
POST /batch_chat
```

项目完整链路：

```text
client.py
↓
httpx.AsyncClient
↓
HTTP Request
↓
FastAPI
↓
Pydantic
↓
Route
↓
Service
↓
HTTP Response
↓
client.py
```

---

# 2. Client 与 Server

以前主要学习的是：

```text
Python
↓
requests / httpx
↓
请求别人的 API
```

此时：

```text
Python 程序 = Client
```

今天反过来：

```text
别人
↓
HTTP Request
↓
我的 FastAPI
↓
Python 处理
↓
HTTP Response
```

此时：

```text
FastAPI 程序 = Server
```

最重要的一句话：

```text
Client：主动发起请求
Server：接收请求、处理请求、返回结果
```

在今天项目里：

```text
client.py → Client
FastAPI app → Server
```

---

# 3. FastAPI 是什么

FastAPI 是一个：

```text
Python Web Framework
```

现阶段可以理解为：

> 帮助我们把 Python 函数变成可以通过 HTTP 访问的 API。

例如普通函数：

```python
def chat(message):
    ...
```

只能在 Python 代码内部调用。

通过 FastAPI：

```python
@app.post("/chat")
async def chat(...):
    ...
```

就可以让别人通过：

```text
POST /chat
```

调用它。

---

# 4. FastAPI 应用和 Server 启动

创建应用：

```python
from fastapi import FastAPI

app = FastAPI()
```

注意：

```text
app = FastAPI()
```

只是：

> 创建 FastAPI 应用对象。

并没有真正开始监听 HTTP 请求。

开发环境启动：

```bash
fastapi dev app/main.py
```

它会真正启动 Server。

开发阶段：

```text
fastapi dev
```

主要作用：

```text
启动 FastAPI
监听 HTTP 请求
开发模式运行
修改代码后方便重新加载
```

---

# 5. Uvicorn

今天问到：

> Uvicorn 是什么？

可以理解为：

```text
FastAPI
→ 负责 API、路由、数据处理

Uvicorn
→ 真正负责运行 Server、监听网络请求
```

整体：

```text
Client
↓
HTTP
↓
Uvicorn
↓
FastAPI
↓
Python 函数
```

目前不用深入 ASGI、Worker 等底层概念。

---

# 6. 地址、端口、路径

今天容易混淆：

```text
http://127.0.0.1:8000/health
```

分别表示：

```text
127.0.0.1 → 地址
8000      → 端口
/health   → 路径
```

不要把 `/health` 叫做端口。

---

# 7. Route（路由）

今天问到：

> 路由是什么意思？

最通俗的理解：

> 路由就是“某种请求来了以后，应该交给哪个 Python 函数处理”的规则。

例如：

```python
@app.get("/health")
async def health():
    ...
```

表示：

```text
GET /health
↓
执行 health()
```

再比如：

```text
POST /chat
↓
chat()

POST /embedding
↓
embedding()
```

可以把 Route 想成：

```text
服务器里的路牌
```

---

# 8. GET 与 POST

今天不重新深入 HTTP，只记：

```text
GET
→ 通常用于获取 / 查询信息

POST
→ 通常用于提交数据给 Server 处理
```

例如：

```text
GET /health
```

只是询问：

> Server 正常吗？

而：

```text
POST /chat
```

需要提交：

```json
{
  "message": "什么是 RAG？"
}
```

---

# 9. Request 和 requests/httpx 的区别

今天重点问过：

> FastAPI 的 `Request` 和以前的 `requests` 有什么区别？

区别非常重要：

```text
requests / httpx
→ Client 工具
→ 我去请求别人

FastAPI Request
→ Server 收到的一次 HTTP Request
→ 别人来请求我
```

例如：

```python
import requests
requests.get(...)
```

是：

```text
我的 Python → 别人的 Server
```

而：

```python
from fastapi import Request
```

表示：

```text
别人的请求 → 我的 FastAPI
```

---

# 10. 没有 Pydantic 时读取 JSON

最开始 `/chat` 使用：

```python
data = await request.json()
```

客户端：

```json
{
  "message": "什么是 RAG？"
}
```

得到 Python：

```python
{
    "message": "什么是 RAG？"
}
```

所以可以：

```python
data["message"]
```

但问题是：

```json
{}
```

或者：

```json
{
  "message": 123
}
```

Server 不能默认相信客户端数据。

因此引出 Pydantic。

---

# 11. Pydantic 是什么

今天你的总结很准确：

> Pydantic 用来做数据校验，拦截不符合要求的数据。

例如：

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
```

表示：

```text
必须有 message
message 应该是字符串
```

Pydantic 可以检查：

```text
字段有没有
类型对不对
数据是否符合要求
```

所以可以把它记成：

```text
Pydantic = API 数据门卫
```

---

# 12. BaseModel

`BaseModel`：

```python
class ChatRequest(BaseModel):
```

表示：

> `ChatRequest` 继承 Pydantic 的数据模型能力。

例如：

```python
class EmbeddingRequest(BaseModel):
    text: str
```

表示请求应该类似：

```json
{
  "text": "RAG 是什么"
}
```

今天还独立写出了：

```python
class BatchChatRequest(BaseModel):
    messages: list[str]
```

以及验收中的：

```python
class SummarizeRequest(BaseModel):
    text: str
    max_length: int
```

---

# 13. Pydantic 对象和 dict 的区别

这是今天容易混的一个点。

没有 Pydantic：

```python
data = await request.json()
```

得到的是：

```text
dict
```

所以：

```python
data["message"]
```

用了 Pydantic：

```python
request: ChatRequest
```

此时：

```text
request 是 ChatRequest 对象
```

所以：

```python
request.message
```

不是：

```python
request["message"]
```

---

# 14. `await` 什么时候用

今天曾经写过：

```python
await request.message
```

这里不需要 `await`。

因为：

```python
request.message
```

只是普通属性读取。

`await` 应该用于异步操作，例如：

```python
await client.get(...)
await client.post(...)
await request.json()
```

简单记：

```text
异步操作 / 协程
→ await

普通变量 / 普通属性
→ 不 await
```

---

# 15. 三个基础 API

## GET `/health`

返回：

```json
{
  "status": "ok"
}
```

作用：

```text
检查 Server 是否正常
```

---

## POST `/chat`

Request：

```json
{
  "message": "什么是 RAG？"
}
```

模拟 Response：

```json
{
  "answer": "模拟回答：什么是 RAG？"
}
```

链路：

```text
JSON
↓
ChatRequest
↓
request.message
↓
generate_chat_answer()
↓
Response
```

---

## POST `/embedding`

Request：

```json
{
  "text": "RAG 是什么"
}
```

模拟 Response：

```json
{
  "embedding": [0.1, 0.2, 0.3]
}
```

暂时没有调用真正的 Embedding Model。

---

# 16. Swagger UI

访问：

```text
http://127.0.0.1:8000/docs
```

Swagger UI 可以：

```text
查看有哪些接口
填写请求数据
直接调用 API
查看状态码
查看 Response
```

今天你的理解：

> 是一个很方便的接口测试页面。

这是正确的。

---

# 17. 项目结构拆分

最终项目结构：

```text
python/day09/

app/
├── __init__.py
├── main.py
├── schemas.py
└── services.py

client.py
requirements.txt
```

三层职责：

```text
main.py
→ FastAPI
→ Route
→ 串接整体流程

schemas.py
→ Pydantic Models
→ 规范请求数据

services.py
→ 真正业务逻辑
```

很好记的一版：

```text
main.py
→ 接客

schemas.py
→ 检查客人带的数据

services.py
→ 真正干活
```

---

# 18. `__init__.py`

今天遇到了：

```text
ModuleNotFoundError: No module named 'app'
```

添加：

```text
app/__init__.py
```

后解决。

目前可以简单理解：

> `__init__.py` 可以帮助 Python 把这个目录作为一个包来组织和导入。

然后：

```python
from app.schemas import ChatRequest
```

就是：

```text
app/
↓
schemas.py
↓
ChatRequest
```

---

# 19. Service 复用

单条 Chat：

```text
generate_chat_answer(message)
```

批量 Chat：

```text
generate_batch_chat_answers(messages)
```

批量逻辑没有重新写：

```text
"模拟回答：" + message
```

而是复用：

```python
generate_chat_answer(message)
```

这样：

```text
单条逻辑修改
→ 批量逻辑自动复用
```

这是今天第一次真正接触一点工程代码复用。

---

# 20. `/batch_chat` 综合实战

Request：

```json
{
  "messages": [
    "什么是 RAG？",
    "什么是 Agent？",
    "什么是 Embedding？"
  ]
}
```

Schema：

```text
BatchChatRequest
messages: list[str]
```

Service：

```text
遍历 messages
↓
调用 generate_chat_answer()
↓
保存多个答案
```

Response：

```json
{
  "answers": [
    "模拟回答：什么是 RAG？",
    "模拟回答：什么是 Agent？",
    "模拟回答：什么是 Embedding？"
  ]
}
```

这证明你已经开始能够把：

```text
Schema
Service
Route
```

迁移到一个新需求。

---

# 21. httpx Client 联调

最终 `client.py` 调用了：

```text
GET  /health
POST /chat
POST /embedding
```

使用：

```text
httpx.AsyncClient
asyncio.gather
```

并发发送。

最终实际返回：

```python
{'status': 'ok'}

{'answer': '模拟回答：什么是 RAG？'}

{'embedding': [0.1, 0.2, 0.3]}
```

完整链路：

```text
client.py
↓
httpx
↓
HTTP Request
↓
FastAPI
↓
Pydantic
↓
Service
↓
HTTP Response
↓
response.json()
↓
client.py
```

---

# 22. 今天学到的 4 类错误

这是今天工程部分非常重要的一块。

```text
ConnectError
→ Client 连 Server 都没连上

404
→ Server 存在，但请求的 Route 不存在

422
→ Route 存在，但请求数据不符合 Schema

500
→ 请求进入 Server，但 Server 内部 Python 代码报错
```

排查顺序可以记：

```text
能不能连接？
↓
路由对不对？
↓
请求数据对不对？
↓
服务器内部代码有没有报错？
```

---

# 23. JSONDecodeError 与 502

今天额外遇到了：

```text
JSONDecodeError
```

原因：

```python
response.json()
```

要求 Response 内容必须是合法 JSON。

如果内容为空：

```text
''
```

或者不是 JSON，就会解析失败。

调试习惯：

```text
.json() 报错
↓
先看 status_code
↓
再看 response.text
```

今天还因为本机代理遇到过：

```text
502
```

而不是预期的 `ConnectError`。

后来使用：

```python
httpx.AsyncClient(trust_env=False)
```

不使用环境代理，成功观察到了：

```text
httpx.ConnectError
```

所以：

```text
502
→ 已经收到 HTTP Response
→ 常见于代理 / 网关与后端连接失败

ConnectError
→ HTTP 连接本身没建立起来
```

---

# 24. LeetCode 20：Valid Parentheses

今天开始正式学习：

```text
Stack
```

核心：

```text
LIFO
Last In First Out
后进先出
```

Python 用：

```python
stack = []
```

入栈：

```python
stack.append(x)
```

出栈：

```python
stack.pop()
```

看栈顶：

```python
stack[-1]
```

括号题思路：

```text
左括号
→ 入栈

右括号
→ 检查栈是否为空
→ 和栈顶比较

匹配
→ pop

不匹配
→ False
```

最后：

```text
stack 为空
→ True

stack 不为空
→ False
```

测试通过：

```text
()       → True
()[]{}   → True
(]       → False
([)]     → False
{[]}     → True
]        → False
```

复杂度：

```text
时间：O(n)
空间：O(n)
```

这里今天最终验收时把时间误说成了 `O(1)`，要重点复习。

---

# 25. LeetCode 155：Min Stack

普通 stack：

```text
push
pop
top
```

要求额外：

```text
getMin()
```

你自己推导出了核心问题：

> 如果只维护一个 `min`，最小值被 pop 后，就不知道以前的最小值是谁了。

所以：

```text
stack
→ 存真实数据

min_stack
→ 保存每一步对应的历史最小值
```

例如：

```text
stack:
[3, 5, 2, 4]

min_stack:
[3, 3, 2, 2]
```

因此：

```text
min_stack[-1]
```

始终是当前最小值。

`pop` 时：

```text
两个栈一起 pop
```

测试：

```text
push(-2)
push(0)
push(-3)

getMin() → -3

pop()

top() → 0

getMin() → -2
```

全部通过。

复杂度：

```text
push     O(1)
pop      O(1)
top      O(1)
getMin   O(1)

空间     O(n)
```

这里的重要思想：

> **用额外空间保存状态，换取更快的查询速度。**

---

# 今天你问的问题重点总结

1. **Uvicorn 是什么意思？**真正负责运行 FastAPI Server、监听网络请求的服务器程序。
2. **为什么 `fastapi dev app/main.py` 能启动？**`fastapi` 调用 FastAPI CLI；`dev` 表示开发模式；`app/main.py` 告诉它应用代码在哪里。
3. **Pydantic 是什么？**用来定义数据结构并校验请求数据是否合法。
4. **Route 路由是什么？**“什么请求应该交给哪个 Python 函数处理”的规则。
5. **FastAPI `Request` 和 `requests` 有什么区别？**`requests/httpx` 是 Client 主动请求别人；`Request` 是 Server 收到的别人发来的请求。
6. **为什么 `request.message` 不需要 await？**因为它只是普通对象属性，不是异步操作。
7. **为什么需要 `__init__.py`？**用于更清楚地组织 Python 包，解决 `app.schemas` 等导入问题。
8. **为什么 Server 停了却出现 502 而不是 ConnectError？**因为请求可能经过环境代理，代理返回了 502；关闭环境代理后才真正得到 ConnectError。
9. **怎么运行 FastAPI 的 main？**今天的项目使用：

   ```bash
   fastapi dev app/main.py
   ```
10. **Stack 怎么创建？**

```python
   stack = []
```

11. **为什么括号匹配使用栈？**最近出现、尚未匹配的左括号应该最先和右括号匹配，符合后进先出。
12. **MinStack 为什么需要第二个栈？**
    为了保存历史最小值，使 `getMin()` 可以做到 `O(1)`。

---

# 今天最容易混淆的 6 个点

```text
Request       ≠ requests
/health       ≠ 端口
request.message ≠ data["message"]
普通属性      ≠ await 操作
422           ≠ Server 崩溃
LeetCode 20 时间复杂度 O(n) ≠ O(1)
```

尤其明天一定再看一次：

```text
127.0.0.1 → 地址
8000      → 端口
/chat     → 路径
```

---

# Day 9 今日结果

**Day 9 评级：B，接近 A。**

已经达到：

```text
可以继续 FastAPI 工程化
```

今天真正完成了：

```text
Python Client
        ↕ HTTP
FastAPI Server
        ↓
Pydantic
        ↓
Service
        ↓
Response
```

下一阶段最需要提升的不是继续背 FastAPI 语法，而是：

> **减少提示依赖，把今天的结构逐渐练到可以从空目录独立搭出来。**

明天开始前建议只复习三个东西：

```text
Client → FastAPI → Pydantic → Service → Response

ConnectError / 404 / 422 / 500

LeetCode 20：O(n) / O(n)
MinStack：四个操作 O(1)，空间 O(n)
```

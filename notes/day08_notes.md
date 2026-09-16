
下面这份可以直接放进你的 Obsidian / `day08_notes.md`。

# Day 8｜httpx + 异步 HTTP + 并发 API 请求

## 1. 今日学习主线

今天把之前学过的 `asyncio` 真正接到了 HTTP 网络请求上：

```text
asyncio 基础
↓
requests 同步请求
↓
httpx.AsyncClient
↓
异步 GET / POST
↓
asyncio.gather 并发请求
↓
Timeout
↓
HTTP / 网络异常处理
↓
批量请求单个失败不影响其他任务
↓
AsyncAPIClient
↓
LLM / RAG / Agent 并发场景
```

今天最重要的不是记 API，而是建立：

> **网络请求大量时间都花在等待 I/O 上，异步可以利用这些等待时间去执行其他任务。**

---

# 2. asyncio 必要复习

### `async def`

定义异步函数：

```python
async def request():
    ...
```

但要特别注意：

> `async def` 只是让这个函数具备异步能力，不代表里面所有代码自动变成异步。

例如：

```python
async def request():
    requests.get(url)
```

`requests.get()` 依旧是同步阻塞请求。

---

### coroutine 协程

调用：

```python
request()
```

如果 `request` 是 `async def`，得到的是一个：

```text
coroutine
协程对象
```

它相当于一个“等待事件循环调度执行的异步任务描述”。

---

### `await`

例如：

```python
response = await client.get(url)
```

含义不是简单的“这里是异步代码”。

更准确是：

> 等待当前异步操作完成；等待 I/O 时，可以把执行机会让给事件循环，让它调度其他任务。

核心流程：

```text
任务 A 执行
↓
遇到 await，开始等待网络
↓
让出执行机会
↓
event loop 调度 B
↓
A 的网络请求完成
↓
恢复执行 A
```

---

# 3. Event Loop

`event loop` 中文：

> **事件循环**

可以简单理解成：

> **异步程序中的任务调度器。**

它不断判断：

```text
哪些任务现在可以执行
哪些任务正在等待
哪些任务已经完成
```

然后在这些任务之间进行调度。

例如：

```text
A 请求 → 等网络
          ↓
event loop 去运行 B

B 请求 → 等网络
          ↓
event loop 去运行 C
```

---

# 4. 今天重点问的问题：为什么连续 await 还是顺序执行？

这是今天最重要的问题之一。

如果写：

```python
await client.get(url1)
await client.get(url2)
await client.get(url3)
```

流程是：

```text
请求 A
↓
等待 A 完成
↓
请求 B 才开始
↓
等待 B 完成
↓
请求 C 才开始
```

虽然 `await` 会让出执行机会，但这时：

```text
B 还没有启动
C 也没有启动
```

所以 event loop 根本没有 B、C 可以切过去执行。

因此：

> **`await` 本身不等于开启并发。**

---

# 5. `asyncio.gather()`

今天最终建立的正确理解：

> `gather()` 把多个 coroutine 一起交给事件循环调度，并等待它们全部完成，然后统一收集结果。

例如逻辑：

```text
先创建 coroutine A
先创建 coroutine B
先创建 coroutine C
↓
await asyncio.gather(A, B, C)
↓
A/B/C 一起被调度
↓
等待网络的时间可以重叠
↓
统一得到结果
```

今天最重要的对比：

```text
await A
await B
await C

→ 顺序
```

而：

```text
A = request(...)
B = request(...)
C = request(...)

await asyncio.gather(A, B, C)
```

是：

```text
→ 并发
```

---

# 6. `create_task()` 和 `gather()`

并不是只有 `gather()` 才能并发。

例如：

```python
task1 = asyncio.create_task(request(url1))
task2 = asyncio.create_task(request(url2))
task3 = asyncio.create_task(request(url3))

await task1
await task2
await task3
```

也可以并发。

因为：

```text
create_task
→ 提前把任务加入 event loop
```

而今天主要使用：

```text
多个 coroutine
→ gather()
```

---

# 7. 为什么需要 httpx？

之前使用：

```python
requests.get(url)
```

`requests` 是同步 HTTP 客户端。

流程：

```text
发请求
↓
等待服务器
↓
服务器返回
↓
继续执行
```

如果 3 个请求分别需要 2 秒：

```text
2 + 2 + 2 ≈ 6 秒
```

即使写：

```python
async def request():
    requests.get(url)
```

也不会自动异步。

原因：

> `requests.get()` 本身就是同步阻塞调用。

---

# 8. httpx

`httpx` 是 Python HTTP 客户端。

它既可以同步：

```python
httpx.get(url)
```

也可以异步：

```python
await client.get(url)
```

今天主要学习：

```python
httpx.AsyncClient()
```

---

# 9. AsyncClient

基本结构：

```python
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

`AsyncClient()`：

> 创建支持异步 HTTP 请求的客户端。

---

# 10. `async with`

今天只需要理解：

> 管理异步资源，使用完成后正确关闭客户端。

类似以前：

```python
with open(...) as f:
```

今天：

```python
async with httpx.AsyncClient() as client:
```

好处：

```text
创建客户端
→ 使用
→ 自动正确关闭
```

不需要自己手动关闭。

---

# 11. 异步 GET

今天成功完成：

```text
AsyncClient
→ await client.get()
→ status_code
→ response.json()
```

核心：

```python
response = await client.get(url)
```

---

# 12. 异步 POST

POST 中使用：

```python
response = await client.post(
    url=url,
    json=data,
    headers=headers,
    timeout=5
)
```

重点复习：

```text
json=
→ 发送 JSON Body

headers=
→ 请求头

timeout=
→ 限制最大等待时间
```

---

# 13. 并发真实 HTTP 请求

今天实际完成了：

```text
3 个真实 HTTP 请求
→ asyncio.gather()
→ 并发执行
```

使用：

```python
time.perf_counter()
```

测量耗时。

实际观察到：

```text
[200, 200, 200]
约 4.37 秒
```

公开测试 API 时间并不稳定，所以不要求必须正好 2 秒。

真正需要观察的是：

> 多个请求的等待时间可以重叠。

后面的综合项目 4 个请求实际耗时约：

```text
1.79 秒
```

---

# 14. Timeout

现实问题：

```text
API 一直没有返回怎么办？
```

如果不限制：

```text
请求一直等待
→ 对应任务迟迟不能完成
→ 整个业务流程可能长期卡住
```

因此需要：

```python
timeout=5
```

今天为了主动制造错误还设置过：

```python
timeout=0.1
```

并实际看到：

```text
httpx.ConnectTimeout
```

---

# 15. TimeoutException

统一处理超时：

```python
except httpx.TimeoutException:
    ...
```

今天认识到：

```text
ConnectTimeout
ReadTimeout
...
```

都属于超时体系。

实际工程中不必背全部子类。

---

# 16. HTTP 4xx / 5xx

今天重点问过：

> 为什么 `client.get()` 成功返回后还需要 `raise_for_status()`？

因为：

```python
response = await client.get(url)
```

即使返回：

```text
404
500
```

也可能正常得到一个 `Response` 对象。

所以要：

```python
response.raise_for_status()
```

逻辑：

```text
2xx
→ 正常继续

4xx / 5xx
→ 抛出 HTTPStatusError
```

因此：

```python
except httpx.HTTPStatusError:
```

才能处理 HTTP 状态错误。

一句话记忆：

> `client.get()` 负责拿响应，`raise_for_status()` 负责判断 HTTP 状态是不是失败。

---

# 17. RequestError

今天还主动制造了：

```text
httpx.ConnectError
```

例如：

```text
getaddrinfo failed
```

说明域名解析 / 网络连接失败。

工程里可以统一用：

```python
except httpx.RequestError:
```

处理这类网络请求异常。

今天三类异常需要重点记：

```text
TimeoutException
→ 请求超时

HTTPStatusError
→ 4xx / 5xx

RequestError
→ DNS、连接失败、网络中断等网络层问题
```

---

# 18. 为什么每个 request 自己捕获异常？

今天你的回答核心是：

> 一个请求失败，不应该让整个批量任务都被打断。

例如：

```text
请求 A → success
请求 B → failed
请求 C → success
```

我们希望最后仍然得到：

```python
["success", "failed", "success"]
```

所以每个 `request()` 自己：

```text
try
→ 请求

except
→ 转换成失败结果
```

而不是让异常一直往外抛。

更准确地说：

> 某个 coroutine 的异常如果没有处理，`gather()` 默认会把异常继续抛给外层，使批量处理流程被打断。

---

# 19. 统一返回结果

最开始：

```python
return "success"
```

存在问题：

> 成功了，但真正的 API 数据丢了。

所以后来升级成统一字典：

```python
{
    "code_status": "success",
    "data": response.json()
}
```

失败：

```python
{
    "code_status": "failed",
    "url": url,
    "reason": str(e)
}
```

这样后续可以：

```text
判断成功/失败
保存返回数据
记录失败 URL
记录错误原因
```

---

# 20. 今天真实遇到的 JSONDecodeError

这是今天很有价值的真实工程问题。

访问：

```text
/status/200
```

服务器确实返回：

```text
200
```

但是响应体可能为空。

代码却写：

```python
response.json()
```

于是：

```text
JSONDecodeError
```

这里建立了一个重要认识：

> **HTTP 200 不代表响应一定是 JSON。**

后来解决：

```python
content_type = response.headers.get("content-type", "")

if "application/json" in content_type:
    data = response.json()
else:
    data = response.text
```

这让客户端同时可以处理：

```text
JSON 响应
普通文本响应
空响应
```

---

# 21. AsyncAPIClient 综合项目

今天设计：

```python
class AsyncAPIClient:
```

自身保存：

```text
base_url
timeout
```

能力：

```text
async get(path)
async post(path, data)
```

最终 GET / POST 都支持：

```text
AsyncClient
GET
POST
JSON
timeout
raise_for_status
TimeoutException
HTTPStatusError
RequestError
JSON / 非 JSON 响应
```

---

# 22. 批量客户端

使用：

```python
results = await asyncio.gather(...)
```

收集结果。

然后：

```text
success_results
failed_results
```

分别保存。

实际完成过：

```text
成功数量：2
失败数量：1
```

说明：

> 单个 404 没有影响另外两个请求。

---

# 23. LLM 应用里的联系

今天的：

```text
async
+
httpx
+
gather
```

以后会直接用于：

```text
同时请求多个 LLM

批量 Embedding

RAG：
向量检索
关键词检索
外部搜索
并行执行

Agent：
多个 Tool 同时调用
```

关键前提：

> 多个任务之间互不依赖，而且主要是在等待 I/O。

---

# 24. 今天问得最重要的问题总结

你今天真正卡住、也最值得复习的问题集中在这些：

- **为什么不用 `gather()` 时会顺序执行？**因为连续 `await A → await B → await C` 时，B、C 还没有启动；虽然 A 等待时会让出执行权，但没有 B、C 可以调度。
- **`event loop` 是什么？**中文是“事件循环”，可以理解为异步任务调度器。某个任务等待 I/O 时，它会去运行其他可执行任务。
- **为什么 `requests` 放进 `async def` 也不异步？**因为 `requests.get()` 本身就是同步阻塞操作，`async def` 不会自动改变内部函数的性质。
- **`await` 到底是什么意思？**不只是“标记异步代码”，而是等待异步操作，同时在等待期间允许把执行机会交给 event loop。
- **`gather()` 到底是干什么？**将多个 coroutine 一起调度，等待全部完成，并收集它们的结果。
- **为什么还要 `raise_for_status()`？**因为 `404 / 500` 仍可能正常得到 `Response`；`raise_for_status()` 才会把它们转换成 `HTTPStatusError`。
- **为什么要 Timeout？**防止某个请求迟迟不返回，让任务长期卡住。
- **为什么异常要在每个请求里处理？**为了实现“一个请求失败 ≠ 整个批量任务失败”。
- **为什么 200 也可能报错？**`200` 只代表 HTTP 状态成功，不代表响应体一定是 JSON；直接 `response.json()` 可能产生 `JSONDecodeError`。
- **RAG 三个任务怎么并发？**
  不是先分别 `await` 三次；应该先得到多个 coroutine，再统一 `await asyncio.gather(...)`。

---

# 25. 算法题

### LeetCode 704 Binary Search

你已经能脱离答案独立写出。

核心：

```text
[left, right] 闭区间
while left <= right

nums[mid] < target
→ left = mid + 1

nums[mid] > target
→ right = mid - 1

相等
→ return mid

不存在
→ return -1
```

复杂度：

```text
时间：O(log n)
空间：O(1)
```

---

### LeetCode 35 Search Insert Position

你通过手动模拟：

```text
[1, 3, 5, 6]

2 → 1
5 → 2
7 → 4
0 → 0
```

自己发现：

> target 不存在时，二分结束后的 `left` 就是正确插入位置。

因此：

```text
找到
→ return mid

没找到
→ return left
```

复杂度：

```text
时间：O(log n)
空间：O(1)
```

---

# 26. Day 8 最终结论

**Day 8 评级：B，接近 A。**

你已经真正掌握：

```text
httpx.AsyncClient
异步 GET / POST
JSON Body
timeout
HTTP 状态处理
网络异常处理
gather 并发
批量结果收集
单请求失败隔离
基础 AsyncAPIClient
LeetCode 704
LeetCode 35
```

目前最需要巩固的是：

```text
await ≠ 开启并发

async def ≠ 内部所有操作自动异步

gather = 多个 coroutine 一起调度 + 等待 + 收集结果

event loop = 事件循环 / 异步任务调度器
```

## 明天 FastAPI 前必须快速复习

只复习这一条主线就够：

```text
创建多个 coroutine
↓
gather 一起调度
↓
coroutine 内部遇到 await I/O
↓
让出执行机会
↓
event loop 调度其他任务
↓
I/O 完成
↓
恢复对应任务
↓
gather 收集全部结果
```

**Day 8：达标，可以进入 FastAPI。**

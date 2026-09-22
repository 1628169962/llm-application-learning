
可以。我给你整理成一份适合直接放进 `notes/day07_notes.md` 的版本，同时把**今天你实际问过、容易卡住的点**单独总结出来。

# Day 7 学习笔记：async / await / asyncio

## 一、今天的核心目标

今天正式进入 Python 工程能力阶段，主题是：

```text
async / await / asyncio
```

重点不是背语法，而是建立一个核心模型：

> 异步不是让单个任务本身变快，而是让程序在等待 I/O 的时候，可以去处理其他任务。

典型适用场景：

```text
HTTP API
LLM API
数据库
网络请求
部分文件 I/O
```

---

## 二、同步执行与 I/O 等待

同步执行的特点：

```text
任务 A
→ 等待
→ 完成
→ 任务 B
→ 等待
→ 完成
```

例如：

```python
import time

def task(name):
    print(name + " 开始请求")
    time.sleep(2)
    print(name + " 请求完成")

task("A")
task("B")
task("C")
```

三个任务每个等待 2 秒，总时间大约：

```text
6 秒
```

原因：

```text
A 等 2 秒
→ B 才能开始

B 等 2 秒
→ C 才能开始
```

这些等待时间被串起来了。

---

## 三、`time.perf_counter()`

用于测量一段代码实际运行经过的时间。

```python
start = time.perf_counter()

# 程序

end = time.perf_counter()

print(end - start)
```

今天同步实验结果：

```text
约 6.00 秒
```

异步实验结果：

```text
约 2.01 秒
```

---

# 四、`async def`

普通函数：

```python
def hello():
    print("hello")
```

调用：

```python
hello()
```

会直接执行函数体。

异步函数：

```python
async def hello():
    print("hello async")
```

直接调用：

```python
hello()
```

并不会像普通函数一样直接执行完。

它会产生：

```text
coroutine
```

也就是：

> 协程对象。

最简单的理解：

```text
async def 定义异步函数

调用异步函数
→ 得到 coroutine

coroutine
→ 需要交给事件循环执行
```

今天实际看到：

```text
<coroutine object hello at ...>
```

---

# 五、`coroutine was never awaited`

直接写：

```python
async def hello():
    print("hello")

hello()
```

可能出现：

```text
RuntimeWarning: coroutine 'hello' was never awaited
```

原因：

```text
创建了 coroutine
↓
但是没有真正让它执行
↓
程序结束
↓
Python 发出警告
```

所以：

```python
hello()
```

不等于：

```text
hello 已经执行完成
```

---

# 六、`asyncio.run()`

作用：

> 启动事件循环，执行最外层 coroutine。

基本结构：

```python
import asyncio

async def main():
    print("hello async")

asyncio.run(main())
```

可以理解为：

```text
main()
→ coroutine
→ asyncio.run()
→ 启动事件循环
→ 执行 coroutine
```

所以异步程序常见入口：

```python
asyncio.run(main())
```

---

# 七、`await`

这是今天最重要的知识点之一。

例如：

```python
async def request(name):
    print(name + " 开始请求")
    await asyncio.sleep(2)
    print(name + " 请求完成")
```

程序运行到：

```python
await asyncio.sleep(2)
```

发生的是：

```text
当前协程暂时暂停
↓
把控制权交回事件循环
↓
事件循环可以运行其他任务
↓
等待结束
↓
当前协程恢复
↓
继续执行后面的代码
```

所以 `await` 不能简单理解成：

```text
等一下
```

更准确地说：

> 当前协程需要等待，因此把执行机会交出去。

---

# 八、`time.sleep()` 和 `asyncio.sleep()`

## `time.sleep(2)`

```python
time.sleep(2)
```

特点：

> 阻塞当前线程。

如果事件循环就在这个线程上，也会一起被卡住。

可以理解成：

```text
当前线程
→ 停 2 秒
→ 其他协程不能靠这个事件循环继续执行
```

---

## `await asyncio.sleep(2)`

```python
await asyncio.sleep(2)
```

特点：

> 暂停当前协程，但不会阻塞整个事件循环。

过程：

```text
A 等待
↓
把控制权交出去
↓
事件循环可以执行 B
↓
B 等待
↓
再执行 C
```

今天你的理解总结得很好：

```text
time.sleep()
→ 强制当前线程停住

await asyncio.sleep()
→ 当前协程暂停
→ 控制权可以交给其他任务
```

---

# 九、`asyncio.create_task()`

作用：

> 把 coroutine 注册成 Task，交给事件循环调度。

例如：

```python
task_a = asyncio.create_task(request("A"))
task_b = asyncio.create_task(request("B"))
task_c = asyncio.create_task(request("C"))
```

注意：

```text
create_task()
≠ 创建线程
```

它只是把协程变成：

```text
事件循环可以调度的 Task
```

---

## 一个重要坑

你第一次写：

```python
async def main():
    task_a = asyncio.create_task(request("A"))
    task_b = asyncio.create_task(request("B"))
    task_c = asyncio.create_task(request("C"))

asyncio.run(main())
```

输出只有：

```text
A 开始请求
B 开始请求
C 开始请求
```

没有：

```text
A 请求完成
B 请求完成
C 请求完成
```

原因：

```text
创建三个 Task
↓
main() 已经结束
↓
asyncio.run(main()) 准备关闭事件循环
↓
三个任务还没有等完
```

所以：

> `create_task()` 只是创建任务，不代表程序会自动等它完成。

---

# 十、等待 Task 完成

可以：

```python
await task_a
await task_b
await task_c
```

虽然代码是一行一行 `await`：

```python
await task_a
await task_b
await task_c
```

但由于 A、B、C 已经提前通过：

```python
create_task()
```

全部注册到事件循环里，所以它们仍然可以并发进行等待。

---

# 十一、`asyncio.gather()`

作用有两个：

```text
1. 等待多个任务全部完成
2. 收集它们的返回值
```

例如：

```python
results = await asyncio.gather(
    task_a,
    task_b,
    task_c
)
```

如果每个任务：

```python
return "A 的返回结果"
```

最后：

```python
print(results)
```

可以得到：

```python
[
    "A 的返回结果",
    "B 的返回结果",
    "C 的返回结果"
]
```

可以记成：

```text
create_task()
→ 创建可调度任务

gather()
→ 等待多个任务
→ 收集结果
```

---

# 十二、同步 vs 异步计时实验

## 同步版本

三个任务：

```text
A 等 2 秒
B 等 2 秒
C 等 2 秒
```

结果：

```text
约 6 秒
```

因为等待时间：

```text
2 + 2 + 2
```

---

## 异步版本

A、B、C 都执行：

```python
await asyncio.sleep(2)
```

过程：

```text
0 秒附近：

A 开始 → 等待
B 开始 → 等待
C 开始 → 等待

约 2 秒：

A 完成
B 完成
C 完成
```

结果：

```text
约 2 秒
```

原因：

> 三个任务的 I/O 等待时间重叠了。

最重要的一句话：

```text
异步没有把 2 秒变短。

异步只是避免了：
2 + 2 + 2

而变成多个任务一起等待。
```

---

# 十三、模拟 LLM 并发请求

今天写了类似：

```python
async def call_llm(name, prompt):
    print("模型" + name + "开始处理：" + prompt)

    await asyncio.sleep(2)

    return "已经处理模型：" + name + "\n已经处理提示词：" + prompt
```

然后：

```python
task_a = asyncio.create_task(...)
task_b = asyncio.create_task(...)
task_c = asyncio.create_task(...)

result = await asyncio.gather(
    task_a,
    task_b,
    task_c
)
```

这已经非常接近以后真实的大模型调用结构：

```text
Python
↓
并发调用多个 LLM / API
↓
等待网络返回
↓
收集结果
```

真实项目中只是把：

```python
await asyncio.sleep(2)
```

换成真正的异步 HTTP 请求。

---

# 十四、异步常见误区

## 1. async 会让 CPU 计算变快吗？

不会。

```text
大量数学计算
图像处理
CPU 密集任务
```

单纯加 `async` 并不会变快。

---

## 2. async 等于多线程吗？

不等于。

异步可以：

```text
一个线程
+
一个事件循环
+
多个 coroutine
```

通过：

```text
某任务等待
→ 切去执行另一个任务
```

实现并发。

---

## 3. async 函数调用后会立刻执行吗？

不会。

```python
hello()
```

得到：

```text
coroutine
```

---

## 4. `await asyncio.sleep()` 等于 `time.sleep()` 吗？

不等于。

```text
time.sleep()
→ 阻塞当前线程

await asyncio.sleep()
→ 暂停当前协程
→ 控制权交给事件循环
```

---

## 5. 所有函数都应该改成 async 吗？

不是。

更适合：

```text
大量 I/O 等待
HTTP
LLM API
数据库
网络请求
```

---

## 6. 异步一定比同步快吗？

不一定。

如果任务本身：

```text
很短
几乎没有 I/O 等待
```

异步还会增加：

```text
事件循环
任务调度
协程管理
```

这些额外开销。

---

# 十五、LeetCode 704：Binary Search

数组：

```python
nums = [-1, 0, 3, 5, 9, 12]
```

因为数组已经有序，所以不需要从头一个一个找。

核心思想：

> 每次看中间值，然后直接排除一半搜索范围。

三个变量：

```python
left
right
mid
```

初始：

```python
left = 0
right = len(nums) - 1
```

中点：

```python
mid = (left + right) // 2
```

三种情况：

```python
nums[mid] == target
→ return mid
```

```python
nums[mid] < target
→ left = mid + 1
```

```python
nums[mid] > target
→ right = mid - 1
```

完整结构：

```python
def search(nums, target):
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
```

---

# 十六、今天二分查找最容易错的点

你第一次写的是：

```python
while left < right:
```

问题：

当：

```text
left == right
```

时，搜索范围里仍然还有最后一个元素没有检查。

例如：

```text
left = 5
right = 5
```

索引 5 依然可能就是答案。

所以这里需要：

```python
while left <= right:
```

---

# 十七、为什么二分查找是 `O(log n)`

因为每次搜索范围都减半：

```text
n
→ n/2
→ n/4
→ n/8
→ ...
→ 1
```

所以需要的次数大约是：

```text
log₂ n
```

因此：

```text
时间复杂度：O(log n)
```

---

# 今天你问的问题 / 卡住的重点

今天真正值得你以后回看的，不是所有代码，而是下面这些问题。

### 1. 为什么异步函数调用后打印的是 coroutine？

因为：

```python
async def hello():
```

定义的是异步函数。

调用：

```python
hello()
```

只会创建：

```text
coroutine
```

不会像普通函数一样直接执行完。

---

### 2. `coroutine was never awaited` 是什么意思？

意思是：

```text
你创建了协程
但是没有让它真正执行
```

所以需要通过：

```python
asyncio.run()
```

或在异步环境里：

```python
await
```

执行它。

---

### 3. 为什么 `create_task()` 后只出现“开始”，没有“完成”？

因为：

```text
Task 创建出来了
但 main() 提前结束了
```

`create_task()` 不会自动保证程序一直等任务完成。

必须：

```python
await task
```

或者：

```python
await asyncio.gather(...)
```

---

### 4. 为什么连续 `await task_a / task_b / task_c` 仍然可以并发？

因为三个 Task 已经提前：

```python
create_task()
```

了。

所以：

```text
A / B / C 都已经进入事件循环
```

`await task_a` 只是保证 `main()` 不提前结束，并不意味着 B、C 现在才开始创建。

---

### 5. 为什么同步约 6 秒，异步约 2 秒？

同步：

```text
A 等 2 秒
→ B 等 2 秒
→ C 等 2 秒
```

约：

```text
6 秒
```

异步：

```text
A 等待
B 同时等待
C 同时等待
```

等待时间发生重叠。

所以接近：

```text
2 秒
```

---

### 6. `time.sleep` 和 `asyncio.sleep` 最本质区别是什么？

```text
time.sleep
→ 阻塞当前线程
```

```text
await asyncio.sleep
→ 当前协程暂停
→ 控制权交回事件循环
```

这是今天最需要记牢的区别。

---

### 7. coroutine 这个词容易忘

你当时回答：

> “得到的是一个 co 什么”

所以这个词明天一定快速复习：

```text
coroutine
中文：协程 / 协程对象
```

核心关联：

```text
async def
→ 调用
→ coroutine
→ 事件循环执行
```

---

### 8. async 是否等于多线程？

不等于。

今天先记：

```text
asyncio
→ 可以单线程
→ 依靠事件循环
→ 在任务等待时切换协程
```

而：

```text
多线程
→ 多个线程
→ 由操作系统调度
```

---

### 9. 异步是否能让 CPU 运算变快？

不能。

它最适合：

```text
I/O 密集
```

而不是单纯：

```text
CPU 密集
```

---

### 10. 二分查找为什么不是 `while left < right`？

因为：

```text
left == right
```

时仍有一个元素需要检查。

所以你当前这套写法必须使用：

```python
while left <= right:
```

---

# Day 7 最后建议你记住的 8 句话

如果明天只复习 5 分钟，就复习这几句：

```text
1. async def 定义异步函数。

2. 调用 async 函数会产生 coroutine。

3. asyncio.run() 可以启动最外层异步程序。

4. await 会暂停当前协程，并把控制权交回事件循环。

5. time.sleep 会阻塞当前线程。

6. asyncio.sleep 不会阻塞整个事件循环。

7. create_task 创建可调度 Task，gather 等待多个任务并收集结果。

8. 异步不是让单个任务变快，而是减少多个 I/O 任务之间无意义的等待。
```

今天 Day 7 的内容已经可以和下一步的 **`httpx` 异步 HTTP 请求**直接衔接了。

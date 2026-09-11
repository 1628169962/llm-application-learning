
# Day 3｜Python OOP、异常处理、模块与包、LeetCode 217

## 一、今日学习内容

今天主要学习了四部分：

1. Python 面向对象 OOP
2. 异常处理
3. 模块与包
4. LeetCode 217：存在重复元素

今日评级：**B**

今日状态：**达标**

---

# 二、OOP 面向对象

## 1. class

`class` 是一个模板 / 设计图，用来定义一种对象应该具有什么数据和功能。

```python
class ModelConfig:
    pass
```

这里的 `ModelConfig` 是一个类。

记忆：

> class = 模板

---

## 2. object / instance

根据类创建出来的具体对象叫：

- object
- instance

现阶段可以把两者理解成一回事。

```python
config = ModelConfig()
```

这里：

```text
ModelConfig → 类
config      → 实例 / 对象
```

记忆：

> class 是模板，object 是具体实例。

---

## 3. `__init__`

`__init__` 是对象创建时自动执行的初始化方法。

主要作用：

> 给实例设置初始数据。

例如：

```python
class ModelConfig:
    def __init__(self, model):
        self.model = model
```

创建：

```python
config = ModelConfig("qwen-plus")
```

创建对象时 `"qwen-plus"` 会传给 `model`。

记忆：

> `__init__` 用来给实例初始化。

---

## 4. self

`self` 表示：

> 当前实例本身。

例如：

```python
self.model = model
```

含义：

> 给当前对象保存一个叫 `model` 的属性。

其中：

```text
model       → 传入的参数
self.model  → 当前对象自己的属性
```

记忆：

> self = 当前实例本身。

---

## 5. 实例属性

属于某个具体对象的数据叫实例属性。

例如：

```python
self.model = model
```

这里的：

```python
self.model
```

就是实例属性。

不同对象可以拥有不同的数据：

```python
qwen.model
deepseek.model
```

---

## 6. 实例方法

定义在类里面，用来描述对象可以做什么的方法叫实例方法。

例如：

```python
def chat(self, prompt):
    return "Qwen response: " + prompt
```

调用：

```python
qwen.chat("你好")
```

调用实例方法时，不需要手动传 `self`。

---

# 三、继承

继承可以让子类复用父类已有的属性和方法，避免重复编写代码。

例如：

```python
class BaseLLM:
    pass

class QwenLLM(BaseLLM):
    pass
```

这里：

```python
QwenLLM(BaseLLM)
```

表示：

> QwenLLM 继承 BaseLLM。

记忆：

> 继承可以使用父类已有功能，避免重复性工作。

工程中可以设计成：

```text
BaseLLM
├── QwenLLM
├── DeepSeekLLM
└── GPTLLM
```

把公共逻辑放到 `BaseLLM`。

---

# 四、方法重写

如果父类已经有一个方法，子类重新定义同名方法，就是方法重写。

例如：

```python
class BaseLLM:
    def chat(self, prompt):
        return "Base response"

class QwenLLM(BaseLLM):
    def chat(self, prompt):
        return "Qwen response"
```

调用：

```python
qwen.chat("hello")
```

会执行 `QwenLLM` 自己的 `chat()`。

记忆：

> 方法重写 = 子类针对父类已有方法实现自己的专属逻辑。

---

# 五、多态

多态现阶段理解直观含义即可。

例如：

```text
QwenLLM.chat()
DeepSeekLLM.chat()
```

虽然都调用：

```python
llm.chat()
```

但是不同对象执行自己的实现。

记忆：

> 同一个调用方式，不同对象可以表现出不同的行为。

---

# 六、异常处理

## 1. try / except

`try` 放可能发生异常的代码。

`except` 用来捕获和处理异常。

```python
try:
    ...
except ValueError:
    ...
```

记忆：

```text
try     → 尝试执行
except  → 出错以后处理
```

作用：

> 避免某些可预期错误直接导致整个程序崩掉。

---

## 2. else

`try` 中没有发生异常时，执行 `else`。

```python
try:
    ans = qwen.chat("你好")
except ValueError:
    print("调用失败")
else:
    print(ans)
```

记忆：

> else = 没出错时执行。

---

## 3. finally

不管有没有出现异常，`finally` 都会执行。

```python
try:
    ...
except Exception:
    ...
finally:
    print("执行结束")
```

记忆：

> finally = 不管成功失败都会执行。

---

## 4. raise

`raise` 用来主动抛出异常。

例如用户传入空 prompt：

```python
if prompt == "":
    raise ValueError("prompt 不能为空")
```

记忆：

```text
raise   → 主动抛异常
except  → 捕获异常
```

---

# 七、LLM Client 综合逻辑

今天实现的核心结构：

```text
BaseLLM
   ↓ 继承
QwenLLM
   ↓
重写 chat()
   ↓
检查 prompt
   ↓
空 prompt
   ↓
raise ValueError
   ↓
main.py
   ↓
try / except 捕获
```

核心代码思想：

```python
class QwenLLM(BaseLLM):
    def chat(self, prompt):
        if prompt == "":
            raise ValueError("prompt 不能为空")

        return "Qwen response: " + prompt
```

调用：

```python
try:
    ans = qwen.chat("你好")
except ValueError:
    print("调用失败")
else:
    print(ans)
```

---

# 八、模块与包

## 1. 模块 module

一个 `.py` 文件通常就是一个 Python 模块。

例如：

```text
base.py
qwen.py
main.py
```

模块里面可以包含：

- 函数
- 类
- 变量

记忆：

> 模块通常就是一个 `.py` 文件。

---

## 2. 包 package

包是：

> 用来组织多个模块的文件夹。

例如：

```text
llm/
├── __init__.py
├── base.py
└── qwen.py
```

这里：

```text
llm      → 包
base.py  → 模块
qwen.py  → 模块
```

---

## 3. `__init__.py`

现阶段只需要知道：

> `__init__.py` 用于帮助组织 Python 包。

暂时不用深入研究其他功能。

---

# 九、import

## 从模块导入类

如果：

```text
qwen.py
```

里面有：

```python
class QwenLLM:
    pass
```

可以：

```python
from qwen import QwenLLM
```

注意：

> import 时不写 `.py`。

---

## 从包中的模块导入

目录：

```text
main.py
llm/
├── __init__.py
└── qwen.py
```

在 `main.py` 中：

```python
from llm.qwen import QwenLLM
```

理解：

```text
llm      → 包
qwen     → 模块
QwenLLM  → 类
```

---

## 包内部相对导入

如果：

```text
llm/
├── base.py
└── qwen.py
```

`qwen.py` 要导入 `base.py` 中的 `BaseLLM`：

```python
from .base import BaseLLM
```

其中：

```text
. = 当前包
```

所以：

```python
from .base import BaseLLM
```

表示：

> 从当前包里的 `base.py` 导入 `BaseLLM`。

---

# 十、ModuleNotFoundError

出现：

```text
ModuleNotFoundError
```

不要第一时间乱改代码。

应该先检查：

```text
当前运行的是哪个文件？
↓
当前文件在哪个目录？
↓
要导入的模块实际在哪？
↓
import 路径和目录结构是否对应？
```

今天建议的结构：

```text
python/day03/
├── main.py
└── llm/
    ├── __init__.py
    ├── base.py
    └── qwen.py
```

---

# 十一、LeetCode 217｜Contains Duplicate

题目：

给一个整数列表，判断里面是否存在重复元素。

例如：

```python
[1, 2, 3, 1]
```

返回：

```python
True
```

---

## 方法一：dict 统计

思路：

遍历列表，用字典记录每个数字出现的次数。

```python
dic[x] = dic.get(x, 0) + 1
```

如果某个数字出现第二次：

```python
if dic[x] == 2:
    return True
```

时间复杂度：

```text
O(n)
```

空间复杂度：

```text
O(n)
```

---

## 方法二：set 保存已经见过的数据

创建：

```python
temp = set()
```

遍历数字：

```text
没见过
↓
加入 set

已经在 set 中
↓
说明重复
↓
返回 True
```

时间复杂度平均：

```text
O(n)
```

空间复杂度：

```text
O(n)
```

---

## 方法三：list → set

`set` 会自动去除重复元素。

例如：

```python
nums = [1, 2, 3, 1]
```

那么：

```text
len(nums)      = 4
len(set(nums)) = 3
```

所以：

```python
len(set(nums)) < len(nums)
```

说明：

> 去重以后元素数量减少了，因此原列表中一定存在重复元素。

最终实现：

```python
def contains_duplicate(nums):
    ans = set(nums)

    if len(ans) < len(nums):
        return True
    else:
        return False
```

平均时间复杂度：

```text
O(n)
```

空间复杂度：

```text
O(n)
```

---

# 十二、今天自己能解释出来的概念

- class：模板
- object：具体实例
- `__init__`：给实例初始化
- self：当前实例本身
- 继承：复用父类已有功能，减少重复工作
- 方法重写：子类为父类已有方法实现自己的专属逻辑
- `try / except`：捕获并处理异常
- `raise`：主动抛出异常
- 模块：通常是一个 `.py` 文件
- 包：组织多个模块的文件夹

---

# 十三、今天还需要巩固

重点不是重新背概念，而是提升独立写代码的熟练度。

需要继续练：

- 从零独立写一个完整 class
- 独立写 `__init__`
- 独立写实例属性和实例方法
- 独立写继承和方法重写
- 判断什么时候使用 `try / except`
- 自己写 `raise ValueError`
- 多文件之间的 import
- 排查 `ModuleNotFoundError`

---

# 十四、明天开始前必须快速复习

重点复习：

```text
class
__init__
self
继承
方法重写
try / except
raise
import
```

最好不看答案重新写一次：

```text
BaseLLM
↓
QwenLLM
```

以及：

```text
prompt 为空
↓
raise ValueError
↓
try / except 捕获
```

---

# Day 3 总结

今天已经从单纯写函数，正式开始进入：

> **“用多个类、多个 Python 文件组织一个小型工程”**

这是从 Python 基础语法向“大模型应用开发工程代码”过渡的重要一步。

Day 3 评级：**B**

是否达标：**达标**

下一阶段重点：

> 少背定义，多独立写几遍，把 OOP、异常处理和模块导入写熟。
> 

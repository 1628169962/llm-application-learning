下一步整理 `notes/`，把今天的学习结论留下来。

创建：

```text
D:\llm-application-learning\notes\day01_notes.md
```

在 PowerShell 执行：

```powershell
New-Item notes\day01_notes.md
```

然后把下面内容复制进去：

```markdown
# Day 1 - Python Basics

## 今日目标

完成 Python 基础语法学习，并建立 GitHub 学习仓库。

## 已学习内容

### Python 基础类型

- `str`
- `int`
- `float`
- `bool`
- `None`

### 核心数据结构

- `list`
  - 下标读取
  - 修改
  - `append()`
  - `remove()`
- `tuple`
  - 有序
  - 创建后不可直接修改
- `set`
  - 元素不重复
  - 可用于去重
- `dict`
  - key / value
  - `get()`
  - `items()`
  - 新增、修改、删除字段

### Python 控制流程

- `if`
- `for`
- `in`
- `len()`
- `range()`

### 函数

- `def`
- 参数
- `return`
- 基础类型注解

## 数据处理实战

能够处理如下数据：

```python
results = [
    {"model": "qwen", "score": 0.91, "latency": 1.2},
    {"model": "deepseek", "score": 0.95, "latency": 2.1},
    {"model": "demo", "score": 0.72, "latency": 0.8},
]
```

已完成：

- 遍历 `list[dict]`
- 根据 `score` 条件筛选
- 提取 `model` 字段
- 计算平均 `score`
- 将筛选逻辑封装成函数

## Two Sum

掌握两种方法：

1. 两层循环暴力查找，时间复杂度 `O(n²)`
2. 使用 `dict` / 哈希表优化，时间复杂度 `O(n)`

核心思路：

```text
need = target - 当前数字
```

使用字典记录：

```text
数字 -> 下标
```

## Git / GitHub

今日完成：

- 安装并确认 Git
- 配置 Git 用户名和邮箱
- 创建 GitHub 仓库
- `git init`
- `git add`
- `git commit`
- 配置 `origin`
- `git push`
- 建立本地 `main` 与远程 `origin/main` 的跟踪关系

## Day 1 评级

A

## 需要继续巩固

- `dict.items()`
- 函数类型注解
- `tuple`
- `set`
- `bool`
- `None`

Day 2 开始前快速复习 10～15 分钟即可。
```

保存完成后，在仓库根目录执行：

```powershell
git status
```

先把 `git status` 输出发给我。

下一步我们再统一执行：

```text
git add .
→ git commit
→ git push
```

把 Day 1 正式提交到 GitHub。
# Eval 操作与局部变量设置

## 概述

`eval` 是 Python 的一个内置函数，用于动态执行字符串形式的 Python 表达式。在 `FactorStrategy` 模块中，我们使用 `eval` 来解析用户输入的表达式（如 `close + open` 或 `ts_rank(close, 5)`），并动态计算因子值。

为了实现直接输入 `close + open` 等表达式，我们通过局部变量设置将 DataFrame 的列名和自定义函数传递给 `eval`。本文将详细解释 `eval` 的操作和局部变量设置。

---

## 1. `eval` 的基本用法

`eval` 的语法如下：

```python
eval(expression, globals=None, locals=None)

# Eval 操作与局部变量设置

## 概述

`eval` 是 Python 的一个内置函数，用于动态执行字符串形式的 Python 表达式。在 `FactorStrategy` 模块中，我们使用 `eval` 来解析用户输入的表达式（如 `close + open` 或 `ts_rank(close, 5)`），并动态计算因子值。

为了实现直接输入 `close + open` 等表达式，我们通过局部变量设置将 DataFrame 的列名和自定义函数传递给 `eval`。本文将详细解释 `eval` 的操作和局部变量设置。

---

## 1. `eval` 的基本用法

`eval` 的语法如下：

```python
eval(expression, globals=None, locals=None)



---

### **`eval_explainer/eval_explainer.py`**

以下是一个简单的 Python 脚本，用于演示 `eval` 的操作和局部变量设置。

```python
import pandas as pd

class EvalExplainer:
    def __init__(self, data):
        """
        初始化 EvalExplainer 类。
        :param data: 包含股票数据的 DataFrame。
        """
        self.data = data

    def calculate_factor(self, expression):
        """
        使用 eval 计算因子值。
        :param expression: 用户输入的表达式（如 'close + open'）。
        :return: 计算得到的因子值。
        """
        # 定义常用函数
        def rank(series):
            """截面排名函数"""
            return series.rank(ascending=False)
        
        def ts_rank(series, window):
            """时间序列排名函数"""
            return series.rolling(window=window).apply(lambda x: x.rank(ascending=False).iloc[-1])
        
        # 将函数和 DataFrame 的列添加到局部变量
        local_vars = {
            'rank': rank,
            'ts_rank': ts_rank,
            **self.data.to_dict('list')  # 将 DataFrame 的列作为变量传递
        }
        
        # 使用 eval 计算因子值
        factor_value = eval(expression, {}, local_vars)
        return factor_value


# 示例用法
if __name__ == "__main__":
    # 示例数据
    data = {
        'stock': ['AAPL', 'GOOGL', 'MSFT'],
        'price': [150, 2800, 300],  # 假设当前价格
        'open': [145, 2750, 290],  # 假设开盘价
        'close': [155, 2850, 310]  # 假设收盘价
    }
    df = pd.DataFrame(data)

    # 初始化 EvalExplainer
    explainer = EvalExplainer(df)

    # 计算因子值
    expression = "close + open"
    factor_value = explainer.calculate_factor(expression)
    print("因子值：", factor_value)

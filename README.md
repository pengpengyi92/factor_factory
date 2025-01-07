# factor_factory
我的因子与回测研究开发工具


# FactorStrategy 模块

## 概述

`FactorStrategy` 是一个用于多因子选股的 Python 工具库，旨在帮助用户通过灵活的表达式计算因子值，并生成交易信号。该模块支持多种因子计算函数，包括截面数据函数和时间序列数据函数，用户可以直接输入列名（如 `close`、`open`）和函数（如 `rank`、`ts_rank`）来计算因子值。

## 核心功能

1. **因子计算**：
   - 支持用户通过表达式动态计算因子值。
   - 提供多种内置函数，包括截面数据函数和时间序列数据函数。

2. **交易信号生成**：
   - 根据因子值对股票进行排序。
   - 生成买入信号（因子值最高的前三名）和卖出信号（因子值最低的后三名）。

3. **回测功能**：
   - 支持简单的回测，计算投资组合的最终价值。

## 核心设计思想

### 1. **动态表达式解析**

`FactorStrategy` 模块的核心是通过 `eval` 函数动态解析用户输入的表达式。为了实现这一点，我们做了以下操作：

- **将 DataFrame 的列添加到局部变量**：
  通过 `self.data.to_dict('list')`，将 DataFrame 的所有列名和列数据作为局部变量传递给 `eval`。这样，用户可以直接在表达式中使用列名（如 `close`、`open`），而不需要写成 `data['close']` 或 `data['open']`。

- **将自定义函数添加到局部变量**：
  我们将常用的因子计算函数（如 `rank`、`ts_rank`）添加到局部变量中，用户可以在表达式中直接调用这些函数。

### 2. **支持的函数**

`FactorStrategy` 模块支持以下常用函数：

#### 截面数据函数
- **`rank(series)`**：对当前截面数据进行排名。
- **`zscore(series)`**：对当前截面数据进行标准化（Z-score）。
- **`scale(series)`**：将当前截面数据缩放到 [0, 1] 范围。
- **`decile(series)`**：将当前截面数据分为 10 个分位数（decile）。
- **`quantile(series, q)`**：将当前截面数据分为指定分位数（如 `quantile(close, 0.25)` 表示 25% 分位数）。

#### 时间序列数据函数
- **`ts_rank(series, window)`**：计算过去 `window` 天内的排名。
- **`ts_zscore(series, window)`**：计算过去 `window` 天内的 Z-score。
- **`ts_mean(series, window)`**：计算过去 `window` 天内的均值。
- **`ts_std_dev(series, window)`**：计算过去 `window` 天内的标准差。
- **`ts_max(series, window)`**：计算过去 `window` 天内的最大值。
- **`ts_min(series, window)`**：计算过去 `window` 天内的最小值。
- **`ts_sum(series, window)`**：计算过去 `window` 天内的总和。
- **`ts_delta(series, window)`**：计算过去 `window` 天内的变化量（当前值减去 `window` 天前的值）。
- **`ts_returns(series, window)`**：计算过去 `window` 天内的收益率。

#### 其他函数
- **`correlation(x, y, window)`**：计算 `x` 和 `y` 在过去 `window` 天内的相关系数。
- **`covariance(x, y, window)`**：计算 `x` 和 `y` 在过去 `window` 天内的协方差。
- **`residual(x, y)`**：计算 `x` 对 `y` 的回归残差（用于 alpha 因子）。

### 3. **表达式示例**

用户可以直接输入以下表达式来计算因子值：

1. **简单表达式**：
   - `close + open`：计算收盘价和开盘价的和。
   - `close - open`：计算收盘价和开盘价的差。

2. **使用函数**：
   - `rank(close)`：对收盘价进行排名。
   - `ts_rank(close, 5)`：计算过去 5 天的收盘价排名。
   - `correlation(close, open, 10)`：计算过去 10 天内收盘价和开盘价的相关系数。

### 4. **使用示例**

以下是一个完整的使用示例：

```python
# 示例数据
data = {
    'stock': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA'],
    'price': [150, 2800, 300, 3400, 700, 600],  # 假设当前价格
    'open': [145, 2750, 290, 3350, 680, 590],  # 假设开盘价
    'close': [155, 2850, 310, 3450, 720, 610]  # 假设收盘价
}
df = pd.DataFrame(data)

# 初始化因子选股策略
factor_expression = "ts_rank(close, 3)"  # 用户输入的表达式
strategy = FactorStrategy(df, factor_expression)

# 计算因子值
strategy.calculate_factor()

# 对股票进行排序
strategy.rank_stocks()

# 生成交易信号
strategy.generate_signals()

# 回测策略
strategy.backtest(initial_capital=100000)

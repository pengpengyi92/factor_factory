# 金融股票市场因子特征选择与预测模型

## 项目简介
本项目旨在探索和实现金融市场中常见的**因子特征选择**和**收益率预测**模型，结合传统统计方法与机器学习方法，帮助优化投资策略。

---

## 目录
1. [数据准备](#数据准备)
2. [特征选择方法](#特征选择方法)
3. [模型选择](#模型选择)
4. [模型评估](#模型评估)
5. [未来改进方向](#未来改进方向)
6. [环境依赖](#环境依赖)
7. [运行示例](#运行示例)
8. [参考资料](#参考资料)

---

## 数据准备
### 1. 数据来源
- 股票历史数据（Yahoo Finance、Wind、Quandl）
- 交易量、财务指标（市盈率PE、市净率PB、ROE等）
- 技术指标（均线、MACD、RSI等）

### 2. 数据处理
- 缺失值填充（均值、中位数、前向填充）
- 异常值处理（Winsorize 去极值）
- 数据归一化（MinMaxScaler、StandardScaler）

---

## 特征选择方法

### 1. 过滤法（Filter Methods）
```python
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.preprocessing import StandardScaler

# 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 选择最相关的K个特征
selector = SelectKBest(score_func=f_regression, k=10)
X_selected = selector.fit_transform(X_scaled, y)

# 输出所选特征
print(selector.get_support(indices=True))
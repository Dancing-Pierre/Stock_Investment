import pandas as pd

# 读取股票日收盘数据
data = pd.read_csv('stock_data.csv', index_col=0, parse_dates=True)
# 读取权重数据
weights = pd.read_csv('strategy1_weights.csv', index_col=0, parse_dates=True)

# 初始化组合价值 DataFrame
portfolio_values = pd.DataFrame(index=data.index, columns=['Strategy1', 'Benchmark'])

# 初始资金
initial_capital = 1.0

# 基准策略
# 假设以市值占比建仓
market_caps = data.iloc[0]
# 计算基准组合的权重，即按市值占比分配
benchmark_weights = market_caps / market_caps.sum()
# 计算基准组合的持仓股数
benchmark_shares = initial_capital * benchmark_weights / data.iloc[0]
# 计算基准组合每日价值并存储在DataFrame中。
portfolio_values['Benchmark'] = (data * benchmark_shares).sum(axis=1)

# 策略1
# 初始化持仓
strategy1_shares = initial_capital * weights.iloc[0] / data.loc[weights.index[0]]
# 计算策略1在第一个调仓日前的每日价值并存储在DataFrame中
portfolio_values.loc[:weights.index[0], 'Strategy1'] = (data.loc[:weights.index[0]] * strategy1_shares).sum(axis=1)

# 调仓日的处理
for i in range(1, len(weights)):
    # 获取当前调仓日期
    rebalance_date = weights.index[i]
    # 获取上一个调仓日期
    prev_date = weights.index[i - 1]
    # 获取策略1在上一个调仓日期的价值
    strategy1_value = portfolio_values['Strategy1'].loc[prev_date]
    # 根据新的权重计算策略1的持仓股数
    strategy1_shares = strategy1_value * weights.iloc[i] / data.loc[rebalance_date]
    # 计算策略1在调仓期间的每日价值并存储在DataFrame中
    portfolio_values.loc[prev_date:rebalance_date, 'Strategy1'] = (
            data.loc[prev_date:rebalance_date] * strategy1_shares).sum(axis=1)

# 最后一个调仓日之后的持仓
portfolio_values.loc[rebalance_date:, 'Strategy1'] = (data.loc[rebalance_date:] * strategy1_shares).sum(axis=1)

# 保存组合每日价值为CSV文件
portfolio_values.to_csv('portfolio_values.csv')

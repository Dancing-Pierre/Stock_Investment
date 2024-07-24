"""
计算投资策略 1 每个调仓日的权重
"""
import pandas as pd
import numpy as np

# 读取数据
data = pd.read_csv('stock_data.csv', index_col=0, parse_dates=True)

# 计算每日收益率
returns = data.pct_change().dropna()

# 计算调仓日列表
data = data.reset_index()
# 转换日期列为datetime类型
data['date'] = pd.to_datetime(data['date'])
# 筛选出双数月份的日期
df = data[data['date'].dt.month % 2 == 0]
# 找到每个年份每个双数月份的最大交易日期
rebalancing_dates = df.groupby([df['date'].dt.year, df['date'].dt.month])['date'].max().tolist()

# 初始化权重 DataFrame
weights = pd.DataFrame(columns=['date'] + data.columns)

# 计算每个调仓日的权重
for date in rebalancing_dates:
    # 获取过去6个月的收益数据，并去除缺失值
    past_returns = returns[date - pd.DateOffset(months=6):date].dropna()
    # 如果过去6个月没有数据，则跳过
    if past_returns.empty:
        continue
    # 计算过去6个月收益数据的协方差矩阵
    cov_matrix = past_returns.cov()
    # 从协方差矩阵中提取两个资产的方差
    var_1, var_2 = np.diag(cov_matrix)
    # 提取两个资产之间的协方差
    cov_12 = cov_matrix.iloc[0, 1]
    # 根据公式计算第一个资产的权重
    w1 = (var_2 - cov_12) / (var_1 + var_2 - 2 * cov_12)
    # 确保权重在0到1之间
    w1 = max(0, min(1, w1))
    # 计算第二个资产的权重。
    w2 = 1 - w1
    # 将计算出的权重存储在权重数据框中，以调仓日期作为索引
    weights.loc[date] = [date, w1, w2]

# 重命名列名
weights.rename(columns={'datedate': 'date', 'date600030': '600030', 'date600036': '600036'}, inplace=True)
# 保存权重为CSV文件
weights.to_csv('strategy1_weights.csv', index=False)

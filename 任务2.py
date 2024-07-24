"""
读取两只股票历史数据，合并成一个文件 stock_data.csv
"""
import pandas as pd

# 读取中信证券数据
a = pd.read_csv('data/600030.csv')
# 读取招商银行数据
b = pd.read_csv('data/600036.csv')
# 合并数据
result = pd.concat([a, b])
# 按照股票代码、交易日从大到小排序
result.sort_values(by=['code', 'date'], ascending=True, inplace=True)
# 转化为透视表
result = result.pivot(index='date', columns='code', values='close')
# 保存文件
result.to_csv('stock_data.csv')

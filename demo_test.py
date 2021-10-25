import pandas as pd
import numpy as np

"""
s1 = pd.Series(['maktub', 'bob', 'frebudd'])
print(s1)


# 创建DataFrame

# 1
a = pd.DataFrame([(1, 2), (3, 4), (6, 7)], columns=['date', 'score'], index=['A', 'B', 'C'])
print(a)

# 2
b = pd.DataFrame()
date = [1, 2, 3]
score = [4, 5, 7]
b['score'] = score
b['date'] = date
print(b)
# .T 转换行列
print(b.T)

# 3 字典创建
c1 = {'a': [1, 2, 3], 'b': [3, 4, 5]}
c = pd.DataFrame.from_dict(c1, orient='index')
print(c)

# 二维数组创建
d = pd.DataFrame(np.arange(12).reshape(3, 4), index=['A', 'B', 'C'], columns=['1', '2', '3', '4'])
print('d:\n', d)

# 修改行列头
dd = d.rename(index={'A': 'Al', 'B': 'BD', 'C': 'CD'}, columns={'1': 'a', '2': 'b', '3': 'c', '4': 'd'})
print("dd:\n", dd)

# 把行头改成d列的内容
ddd = dd.set_index('d')
print('ddd:\n', ddd)

# 重新建立数字索引
dddd = ddd.reset_index()
print('dddd:\n', dddd)

"""

"""
# pandas文件读写操作

data = pd.read_excel('./read_hot.xlsx')
print(data)
# head 选取前五行
print(data.head(5))

# 输出excel表格
data.to_excel('./tocsvdemo.xlsx', index=False)

"""

"""
# 数据的选取与处理

data = pd.DataFrame(np.arange(12).reshape(3, 4), index=['R1', 'R2', 'R3'], columns=['C1', 'C2', 'C3', 'C4'])
print(data)

# 选取列
c = data[['C1', 'C3']]
print(c)

# 选取行
r = data[1:3]
print(r)

# iloc选取行(根据行序列)

rr = data.iloc[-1]
print('rr:\n', rr)

# loc选取行(根据行名称)

rrr = data.loc[['R1', 'R3']]
print('rrr:\n: ', rrr)

# 根据行列获取数据
rc = data.loc[['R1', 'R3']][['C1', 'C3']]
print(rc)

# 筛选数据
drc = data[(data['C1'] > 1) & (data['C1'] < 8)]
print(drc)

print('shape: \n', data.shape)

print('describe:\n', data.describe())

# 值出现的次数
print(data['C2'].value_counts())

# 通过计算添加新列
data['C5'] = data['C3'] - data['C2']
print('data:\n', data.head())

# 排序
sort_d = data.sort_values('C3', ascending=False)
print(sort_d)

# 删除行列数据 
delete_data = data.drop(index=['R2'], columns=['C5'], inplace=False)
print(delete_data)
"""

"""
# 数据表拼接

data_1 = pd.DataFrame({'学生': ['maktub', 'frebudd', 'eillot'], '分数': [99, 88, 77]})
data_2 = pd.DataFrame({'学生': ['maktub', 'frebudd', 'mercer'], '课程': ['语文', '数学', '英语']})

# merge how[inner, outer, left,right],on=合并key
# sum_data = pd.merge(data_1, data_2, on='学生')
sum_data = pd.merge(data_1, data_2, how='outer')
print(sum_data)

#  concat全连接 axis=0 纵向连接，1 横向连接。
concat_data = pd.concat([data_1, data_2], axis=0)
# concat_data = pd.concat([data_1, data_2], axis=1)
print(concat_data)

# append 添加新行 ignore_index 重新赋值索引
append_data = data_1.append(data_2, ignore_index=True)
append_data = append_data.append([{'学生': 'append_student', '分数': '100', '课程': '物理'}])
print(append_data)
"""
"""
# 数组和列表的区别：分隔符不同 空格和逗号，数组支持运算
# 数组创建

# 一维
n1 = np.array([1, 2, 3, 4])

# 二维
n2 = np.array([[1], [2], [3]])

print(n1)
print(n2)

n3 = np.arange(5, 15, 2)
print(n3)

# 随机9个正态分布
n4 = np.random.randn(9)
print(n4)

# 随机 0-1
n5 = np.random.rand(9).reshape(3, 3)
print(n5)

# 随机0-9
n6 = np.random.randint(0, 9, (3, 3))
print(n6)
"""

import matplotlib as plt



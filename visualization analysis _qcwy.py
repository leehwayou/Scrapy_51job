import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyecharts import Geo
from collections import Counter
# -*- coding: utf-8 -*-

qcwy = pd.read_csv(r'C:\Users\leehwayou\Documents\WeChat Files\sunshiningdawn\FileStorage\File\2019-06\info333(1).csv', encoding='utf-8')
# 企业类型
CompanyNature_Count = qcwy.CompanyNature.value_counts()
# 设置中文字体
font = {'family': 'SimHei'}
matplotlib.rc('font', **font)
fig = plt.figure(figsize=(8, 8))

# 绘制饼图'各类型企业所占比例'，参数pctdistance表示饼图内部字体的离中心距离，labeldistance则是label的距离，radius指饼图的半径
patches, l_text, p_text = plt.pie(CompanyNature_Count, autopct='%.2f%%', pctdistance=0.6, labels=CompanyNature_Count.index, labeldistance=1.1, radius=1)
m, n = 0.04, 0.04
for t in l_text[7:11]:
    t.set_size(10)
    t.set_y(m)
    m += 0.1
for p in p_text[7:11]:
    p.set_size(10)
    p.set_y(n)
    n += 0.1
plt.title('.net岗位中各类型企业所占比例', fontsize=24)

# 绘制条形图，企业规模
CompanySize_Count = qcwy.CompanySize.value_counts()
index, bar_width = np.arange(len(CompanySize_Count)), 0.6
fig = plt.figure(figsize=(8, 6))
plt.barh(index*(-1)+bar_width, CompanySize_Count, tick_label=CompanySize_Count.index, height=bar_width)
# 添加数据标签
for x, y in enumerate(CompanySize_Count):
    plt.text(y+0.1, x*(-1)+bar_width, '%s' % y, va='center')
plt.title('.net岗位各公司规模总数分布条形图', fontsize=24)


# 绘制地图，岗位地区需求
# 统计各地区出现次数，并转换为元组的形式
# data = Counter(qcwy.Workplace).most_common()
# # 生成地理坐标图
# geo = Geo('数据分析岗位各地区需求量', title_color='#fff', title_pos='center', width=1200, height=600, background_color='#404a59')
# attr, value = geo.cast(data)
# # 添加数据点
# geo.add('', attr, value, visual_range=[0, 100], visual_text_color='#fff', symbol_size=5, is_visualmap=True, is_piecewise=True)
# geo.show_config()
# geo.render(path='java岗位地区需求.html')

# 学历和工作经验
fig, ax = plt.subplots(1, 2, figsize=(18, 8))
Education_Count = qcwy.Education.value_counts()
Workyear_Count = qcwy.Workyear.value_counts()
patches, l_text, p_text = ax[0].pie(Education_Count, autopct='%.2f%%', labels=Education_Count.index )
m = -0.01
for t in l_text[6:]:
    t.set_y(m)
    m += 0.1
    print(t)
for p in p_text[6:]:
    p.set_y(m)
    m += 0.1
ax[0].set_title('.net岗位各学历要求所占比例', fontsize=24)
index, bar_width = np.arange(len(Workyear_Count)), 0.6
ax[1].barh(index*(-1) + bar_width, Workyear_Count, tick_label=Workyear_Count.index, height=bar_width)
ax[1].set_title('.net岗位工作经验要求', fontsize=24)
plt.show()

# 薪资与岗位需求关系
fig = plt.figure(figsize=(9, 7))
# 转换类型为浮点型
qcwy.LowSalary, qcwy.HighSalary = qcwy.LowSalary.astype(float), qcwy.HighSalary.astype(float)
# 分别求各地区平均最高薪资，平均最低薪资
Salary = qcwy.groupby('Workplace', as_index=False)['LowSalary', 'HighSalary'].mean() # 求平均薪资
Workplace = qcwy.groupby('Workplace', as_index=False)['JobTitle'].count().sort_values('JobTitle', ascending=False) # 分别求各地区的python岗位数量，并降序排列
Workplace = pd.merge(Workplace, Salary, how='left', on='Workplace') # 合并数据表
Workplace = Workplace.head(20)
plt.bar(Workplace.Workplace, Workplace.JobTitle, width=0.8, alpha=0.8)
plt.plot(Workplace.Workplace, Workplace.HighSalary*1000, '--', color='g', alpha=0.9, label='平均最高薪资')
plt.plot(Workplace.Workplace, Workplace.LowSalary*1000, '-.', color='r', alpha=0.9, label='平均最低薪资')

# 添加数据标签
for x, y in enumerate(Workplace.HighSalary*1000):
    plt.text(x, y, '%.0f' % y, ha='left', va='bottom')
for x, y in enumerate(Workplace.LowSalary*1000):
    plt.text(x, y, '%.0f' % y, ha='right', va='bottom')
for x, y in enumerate(Workplace.JobTitle):
    plt.text(x, y, '%s' % y, ha='center', va='bottom')
plt.legend()
plt.title('.net岗位需求量排名前20地区的薪资水平状况', fontsize=20)
plt.show()

# 薪资与经验关系
# 1.求出各工作经验对应的平均最高平均最低工资
Salary_Year = qcwy.groupby('Workyear', as_index=False)['LowSalary', 'HighSalary'].mean()
# 求平均薪资
Salary_Year['Salary'] = (Salary_Year.LowSalary.add(Salary_Year.HighSalary)).div(2)
# 绘制条形图
plt.barh(Salary_Year.Workyear, Salary_Year.Salary, height=0.6)
for x, y in enumerate(Salary_Year.Salary):
    plt.text(y+0.1, x, '%.2f' % y, va='center')
plt.title('各工作经验对应的平均薪资水平(单位:千/月)', fontsize=20)
plt.show()

# 薪资与学历的要求
# 计算平均薪资
Salary_Education = qcwy.groupby('Education', as_index=False)['LowSalary', 'HighSalary'].mean()
Salary_Education['Salary'] = Salary_Education.LowSalary.add(Salary_Education.HighSalary).div(2)
Salary_Education = Salary_Education.sort_values('Salary', ascending=True)
# 绘制柱形图
plt.bar(Salary_Education.Education, Salary_Education.Salary, width=0.6)
for x,y in enumerate(Salary_Education.Salary):
    plt.text(x, y, '%.2f' % y, ha='center', va='bottom')
plt.title('各学历对应的平均工资水平(单位:千/月)', fontsize=20)
plt.show()
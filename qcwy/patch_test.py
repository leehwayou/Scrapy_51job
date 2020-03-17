import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# -*- coding: utf-8 -*-

qcwy = pd.read_csv(r'D:\python学习\Py文件\Scrapy前程无忧\qcwy\招聘数据(Python)(改1).csv', encoding='utf-8')
# 企业类型
CompanyNature_Count = qcwy.CompanyNature.value_counts()
# 设置中文字体
font = {'family': 'SimHei', 'size': 18}
matplotlib.rc('font', **font)
fig = plt.figure(figsize=(7, 7))

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
ax[0].set_title('Python岗位各学历要求所占比例', fontsize=24)
index, bar_width = np.arange(len(Workyear_Count)), 0.6
ax[1].barh(index*(-1) + bar_width, Workyear_Count, tick_label=Workyear_Count.index, height=bar_width)
ax[1].set_title('Python岗位工作经验要求', fontsize=20)
plt.show()
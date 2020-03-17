import pandas as pd
import re
import numpy as np
from IPython.display import display
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)
pd.set_option('display.width', 50)

df = pd.read_csv(r'D:\python学习\Py文件\Scrapy前程无忧\qcwy\info333.csv')
df.columns = ['JobTitle', 'CompanyName', 'CompanyNature', 'CompanySize', 'IndustryField', 'Salary', 'Workplace', 'Workyear', 'Education', 'RecruitNumbers', 'PositionAdvantage']
# df.info()
# display(df.describe(include=['O']))
# print(df.JobTitle.unique())
# print(df.shape)
qcwy = df.drop_duplicates(inplace=False)  #inplace是true的话就是对原数据进行修改
qcwy = qcwy[df.JobTitle.str.contains('.*?net.*?|.*?NET.*?')]  #保留有效的数据

qcwy.Education.fillna('不限学历', inplace=True)
qcwy.PositionAdvantage.fillna(qcwy.PositionAdvantage.mode()[0], inplace=True)


# qcwy.to_csv(r'D:\python学习\Py文件\Scrapy前程无忧\qcwy\

# 将5种单元进行编号
qcwy['Standard'] = np.where(qcwy.Salary.str.contains('元.*?小时'), 0,
                               np.where(qcwy.Salary.str.contains('元.*?天'), 1,
                                        np.where(qcwy.Salary.str.contains('千.*?月'), 2,
                                                 np.where(qcwy.Salary.str.contains('万.*?月'), 3,
                                                          4))))
# 用'-'将Salary分割为LowSalary和HighSalary
SalarySplit = qcwy.Salary.str.split('-', expand=True)
qcwy['LowSalary'], qcwy['HighSalary'] = SalarySplit[0], SalarySplit[1]
# Salary中包含'以上','以下',或者两者都不包含的进行编号
qcwy['HighOrLow'] = np.where(qcwy.LowSalary.str.contains('以.*?下'), 0,
                             np.where(qcwy.LowSalary.str.contains('以.*?上'), 2,
                                      1))
# 匹配LowSalary中的数字，并转换为浮点型
Lower = qcwy.LowSalary.apply(lambda x: re.search('(\d+\.?\d*)', x).group(1)).astype(float)
# 对LowSalary中HighOrLow为1的部分进行单位换算，全部转化为'千/月'
qcwy.LowSalary = np.where(((qcwy.Standard==0)&(qcwy.HighOrLow==1)), Lower*8*21/1000,
                             np.where(((qcwy.Standard==1)&(qcwy.HighOrLow==1)), Lower*21/1000,
                                      np.where(((qcwy.Standard==2)&(qcwy.HighOrLow==1)), Lower,
                                               np.where(((qcwy.Standard==3)&(qcwy.HighOrLow==1)), Lower*10,
                                                        np.where(((qcwy.Standard==4)&(qcwy.HighOrLow==1)), Lower/12*10,
                                                                 Lower)))))
# 对HighSalary中的缺失值进行填充, 可以有效避免匹配出错.
qcwy.HighSalary.fillna('0千/月', inplace=True)
# 匹配HighSalary中的数字, 并转为浮点型
Higher = qcwy.HighSalary.apply(lambda x: re.search('(\d+\.?\d*).*?', str(x)).group(1)).astype(float)
# 对HighSalary中HighOrLow为1的部分完成单位换算, 全部转为'千/月'
qcwy.HighSalary = np.where(((qcwy.Standard==0)&(qcwy.HighOrLow==1)), qcwy.LowSalary/21*26,
                              np.where(((qcwy.Standard==1)&(qcwy.HighOrLow==1)), qcwy.LowSalary/21*26,
                                       np.where(((qcwy.Standard==2)&(qcwy.HighOrLow==1)), Higher,
                                                np.where(((qcwy.Standard==3)&(qcwy.HighOrLow==1)), Higher*10,
                                                         np.where(((qcwy.Standard==4)&(qcwy.HighOrLow==1)), Higher/12*10,
                                                                  np.where(qcwy.HighOrLow==0, qcwy.LowSalary,
                                                                           qcwy.LowSalary))))))

#将地区统一到市级
qcwy['Workplace'] = qcwy.Workplace.str.split('-', expand=True)[0]
qcwy.to_csv(r'D:\python学习\Py文件\Scrapy前程无忧\qcwy\info333.csv')
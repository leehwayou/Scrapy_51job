import pandas as pd
import numpy as np

df = pd.read_csv(r'D:\python学习\Py文件\Scrapy前程无忧\qcwy\招聘数据(Python)(改1).csv')
Education = df.Education.astype(str)
indexes = Education[Education.str.contains('招')].index
for index in indexes:
    print(index)
    df.drop(index=index, inplace=True)
    print('删除成功')
df.to_csv(r'D:\python学习\Py文件\Scrapy前程无忧\qcwy\招聘数据(Python)(改1).csv')

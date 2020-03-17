# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class QcwyItem(scrapy.Item):
    JobTitle = Field()                      #职位名称
    CompanyName = Field()                   #公司名称
    CompanyNature = Field()                 #公司性质
    CompanySize = Field()                   #公司规模
    IndustryField = Field()                 #所属行业
    Salary = Field()                        #薪水
    Workplace = Field()                     #工作地点
    Workyear = Field()                      #要求工作经验
    Education = Field()                     #要求学历
    RecruitNumbers = Field()                #招聘人数
    ReleaseTime = Field()                   #发布时间
    Language = Field()                      #要求语言
    Specialty = Field()                     #要求专业
    PositionAdvantage = Field()             #职位福利
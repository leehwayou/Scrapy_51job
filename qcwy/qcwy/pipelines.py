# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QcwyPipeline(object):
    def process_item(self, item, spider):
        with open(r'D:\python学习\Py文件\Scrapy前程无忧\qcwy\招聘数据(Python).csv', 'a', encoding='gb18030') as f:
            job_info = [item['JobTitle'], item['CompanyName'], item['CompanyNature'], item['CompanySize'],
                        item['IndustryField'], item['Salary'], item['Workplace'], item['Workyear'],
                        item['Education'], item['RecruitNumbers'], item['ReleaseTime'], item['Language'],
                        item['Specialty'], item['PositionAdvantage'], '\n']
            f.write(",".join(job_info))
        return item

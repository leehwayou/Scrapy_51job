import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from qcwy.items import QcwyItem

class qcwy_spider(scrapy.Spider):
    name = 'qcwy_spider'
    allowed_domains = ['https://search.51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,{}.html?'.format(
            str(page)) for page in range(1, 50)]

    def parse(self, response):
        yield Request(
            url=response.url,
            callback=self.parse_job_url,
            meta={},
            dont_filter=True
        )

    def parse_job_url(self, response):
        selector = Selector(response)
        urls = selector.xpath('//div[@class="el"]/p/span')
        for url in urls:
            url = url.xpath('a/@href').extract()[0]
            yield Request(
                url=url,
                callback=self.parse_job_info,
                meta={},
                dont_filter=True)

    def parse_job_info(self, response):
        item = QcwyItem()
        selector = Selector(response)
        JobTitle = selector.xpath('//div[@class="cn"]/h1/text()').extract()[0].strip().replace(' ', '').replace(',',
                                                                                                                ';')
        CompanyName = selector.xpath('//div[@class="cn"]/p[1]/a[1]/text()').extract()[0].strip().replace(',', ';')
        CompanyNature = selector.xpath('//div[@class="tCompany_sidebar"]/div/div[2]/p[1]/text()').extract()[
            0].strip().replace(',', ';')
        CompanySize = selector.xpath('//div[@class="tCompany_sidebar"]/div/div[2]/p[2]/text()').extract()[
            0].strip().replace(',', ';')
        IndustryField = selector.xpath('//div[@class="tCompany_sidebar"]/div/div[2]/p[3]/a/text()').extract()[
            0].strip().replace(',', ';')
        Salary = selector.xpath('//div[@class="cn"]/strong/text()').extract()[0].strip().replace(',', ';')
        infos = selector.xpath('//div[@class="cn"]/p[2]/text()').extract()
        Workplace = infos[0].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
        Workyear = infos[1].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
        if len(infos) == 4:
            Education = ''
            RecruitNumbers = infos[2].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
            ReleaseTime = infos[3].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
        else:
            Education = infos[2].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
            RecruitNumbers = infos[3].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
            ReleaseTime = infos[4].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
        if len(infos) == 7:
            Language, Specialty = infos[5].strip().replace('&nbsp;&nbsp;', ''), infos[6].strip().replace('&nbsp;&nbsp;',
                                                                                                         '').replace(
                ',', ';')
        elif len(infos) == 6:
            if (('英语' in infos[5]) or ('话' in infos[5])):
                Language, Specialty = infos[5].strip().replace('&nbsp;&nbsp;', '').replace(',', ';'), ''
            else:
                Language, Specialty = '', infos[5].strip().replace('&nbsp;&nbsp;', '').replace(',', ';')
        else:
            Language, Specialty = '', ''
        Welfare = selector.xpath('//div[@class="t1"]/span/text()').extract()
        PositionAdvantage = ';'.join(Welfare).replace(',', ';')
        item['JobTitle'] = JobTitle
        item['CompanyName'] = CompanyName
        item['CompanyNature'] = CompanyNature
        item['CompanySize'] = CompanySize
        item['IndustryField'] = IndustryField
        item['Salary'] = Salary
        item['Workplace'] = Workplace
        item['Workyear'] = Workyear
        item['Education'] = Education
        item['RecruitNumbers'] = RecruitNumbers
        item['ReleaseTime'] = ReleaseTime
        item['Language'] = Language
        item['Specialty'] = Specialty
        item['PositionAdvantage'] = PositionAdvantage
        yield item
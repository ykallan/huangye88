# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import HuangyeItem


class HySpider(scrapy.Spider):
    name = 'hy'
    # allowed_domains = ['huangye88.com/']
    start_urls = ['http://b2b.huangye88.com/']

    def parse(self, response):
        lists = response.xpath('//ul[@class="qiyecont"]/li/a/@href').getall()
        for url in lists:
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_industry)

    def parse_industry(self, response):
        shengfen = response.xpath('//div[@class="main"]/div[1]//a/@href').getall()
        for url in shengfen:
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_company_list)

        chengshis = response.xpath('//div[@class="main"]/div[2]//a/@href').getall()
        for chengshi in chengshis:
            # print(chengshi)
            yield scrapy.Request(url=chengshi, callback=self.parse_company_list)

    def parse_company_list(self, response):
        companys = response.xpath('//a[@itemprop="name"]/@href').getall()
        for company in companys:
            # print(company)
            yield scrapy.Request(url=company, callback=self.parse_detail)
            # break
        next_page = response.xpath('//div[@class="page_tag Baidu_paging_indicator"]/a[last()-1]/@href').get()
        # print(next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_company_list)

    def parse_detail(self, response):
        meta_url = response.xpath('//meta[@name="mobile-agent"]/@content').get()
        # print(meta_url.split('=')[-1])
        yield scrapy.Request(url=meta_url.split('=')[-1], callback=self.parse_mobile)

    def parse_mobile(self, response):
        try:
            com_name = response.xpath('//span[@class="banner-text"]/a/text()').get().strip()
        except Exception as e:
            com_name = '空白'
        try:
            person_name = response.xpath('//section[@class="contact"]/ul/li[1]/a/text()').get().split('：')[-1].strip()
        except Exception as e:
            person_name = '空白'

        try:
            address = response.xpath('//section[@class="contact"]/ul/li[3]/a/text()').get().split('：')[-1].strip()
        except Exception as e:
            address = '空白'

        try:
            # phone = re.findall(r'：(1[0-9]{10})', response.text)
            phone = re.findall(r'tel:(\d{11})', response.text)
            print(phone)
        except AttributeError as e:
            phone = re.findall(r'：(1[0-9]{10})', response.text)

        if len(phone) == 1:
        # if len(phone) > 5:
            item = HuangyeItem()
            item['com_name'] = com_name
            item['person_name'] = person_name
            item['phone'] = phone[0]
            item['address'] = address
            yield item

